# file eulcommon/djangoextras/auth/decorators.py
#
#   Copyright 2010,2011 Emory University Libraries
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# based on code from http://djangosnippets.org/snippets/254/
from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.http import urlquote

def user_passes_test_with_403(test_func, login_url=None):
    """
    View decorator that checks to see if the user passes the specified test.
    See :meth:`django.contrib.auth.decorators.user_passes_test`.

    Anonymous users will be redirected to login_url, while logged in users that
    fail the test will be given a 403 error.  In the case of a 403, the function
    will render the **403.html** template.
    """
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL
    def _dec(view_func):
        @wraps(view_func)
        def _checklogin(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            elif not request.user.is_authenticated():
                return HttpResponseRedirect('%s?%s=%s' % (login_url,
                            REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
            else:
                tpl = get_template('403.html')
                return HttpResponseForbidden(tpl.render(RequestContext(request)))
        return _checklogin
    return _dec

def permission_required_with_403(perm, login_url=None):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the login page or rendering a 403 as necessary.

    See :meth:`django.contrib.auth.decorators.permission_required`.
    """
    return user_passes_test_with_403(lambda u: u.has_perm(perm), login_url=login_url)

# ajax permissions decorators adapted from
# http://drpinkpony.wordpress.com/2010/02/02/django-ajax-authentication/

def user_passes_test_with_ajax(test_func, login_url=None,
                               redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.

    Returns special response to ajax calls instead of blindly redirecting.

    To use with class methods instead of functions, use :meth:`django.utils.decorators.method_decorator`.  See
    http://docs.djangoproject.com/en/dev/releases/1.2/#user-passes-test-login-required-and-permission-required

    Usage is the same as
    :meth:`django.contrib.auth.decorators.user_passes_test`::

        @user_passes_test_with_ajax(lambda u: u.has_perm('polls.can_vote'), login_url='/loginpage/')
        def my_view(request):
            ...

    """
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def decorator(view_func):
        @wraps(view_func)
        def _check_user_test(request, *args, **kwargs):
            try:
                test_result = test_func(request.user, request=request, *args, **kwargs)
            except TypeError:
                test_result = test_func(request.user)

            if test_result:
                return view_func(request, *args, **kwargs)
            path = urlquote(request.get_full_path())
            urlparts = login_url, redirect_field_name, path
            # check for ajax request
            if not request.is_ajax():
                return HttpResponseRedirect('%s?%s=%s' % urlparts)
            else:
                # In case of ajax we send 401 - unauthorized HTTP response
                return HttpResponse('%s?%s=%s' % urlparts, status=401)

        return _check_user_test
    return decorator


def login_required_with_ajax(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in,
    redirecting to the log-in page if necessary, but returns a special
    response for ajax requests.  See
    :meth:`eulcommon.djangoextras.auth.decorators.user_passes_test_with_ajax`.

    Example usage::

        @login_required_with_ajax()
        def my_view(request):
            ...

    """
    # NOTE: currently only this format works: @login_required_with_ajax()
    # But this format errors: @login_required_with_ajax
    if function is None:
        function = lambda u: u.is_authenticated()
    return user_passes_test_with_ajax(function, redirect_field_name=redirect_field_name)


def permission_required_with_ajax(perm, login_url=None):
    """
    Decorator for views that checks whether a user has a particular
    permission enabled, redirecting to the log-in page if necessary,
    but returns a special response for ajax requests.  See
    :meth:`eulcore.django.auth.decorators.user_passes_test_with_ajax`.

    Usage is the same as
    :meth:`django.contrib.auth.decorators.permission_required` ::

        @permission_required_with_ajax('polls.can_vote', login_url='/loginpage/')
        def my_view(request):
            ...

    """
    return user_passes_test_with_ajax(lambda u: u.has_perm(perm), login_url=login_url)
