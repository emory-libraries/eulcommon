# file test_djangoextras/test_auth.py
#
#   Copyright 2011 Emory University Libraries
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

from mock import Mock
from os import path
from unittest import TestCase

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse, HttpRequest

from eulcommon.djangoextras.auth import user_passes_test_with_403, \
    permission_required_with_403, user_passes_test_with_ajax, \
    login_required_with_ajax


# mock users to simulate a staff user and a superuser
staff_user = Mock(spec=User, name='MockStaffUser')
staff_user.username = 'staff'
staff_user.is_authenticated.return_value = True
staff_user.has_perm.return_value = False

super_user = Mock(spec=User, name='MockSuperUser')
super_user.username = 'super'
super_user.is_authenticated.return_value = True
super_user.has_perm.return_value = True


def simple_view(request):
    "a simple view for testing custom auth decorators"
    return HttpResponse("Hello, World")

class PermissionRequired403_Test(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = AnonymousUser()


        self.staff_user = staff_user
        self.super_user = super_user

        self._template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            path.join(path.dirname(path.abspath(__file__)), 'fixtures'),
        )

        # decorate simple view above for testing
        self.login_url = '/my/login/page'
        decorator = permission_required_with_403('is_superuser', self.login_url)
        self.decorated = decorator(simple_view)

    def tearDown(self):
        # restore any configured template dirs
        settings.TEMPLATE_DIRS = self._template_dirs

    def test_anonymous(self):
        response = self.decorated(self.request)
        self.assert_(response['Location'].startswith(self.login_url),
                "decorated view redirects to login page for non-logged in user")
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with non-logged in user" \
                % (expected, got))

    def test_logged_in_notallowed(self):
        # set request to use staff user
        self.request.user = self.staff_user
        response = self.decorated(self.request)

        expected, got = 403, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with logged-in user without perms" \
                % (expected, got))
        self.assert_("permission denied" in response.content,
                "response should contain content from 403.html template fixture")

    def test_logged_in_allowed(self):
        # set request to use superuser account
        self.request.user = self.super_user
        response = self.decorated(self.request)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with superuser" \
                % (expected, got))
        self.assert_("Hello, World" in response.content,
                     "response should contain actual view content")


# test function for use with user_passes test methods
def is_staff(user):
    return user.username == 'staff'


class UserPassesTest403_Test(TestCase):
    fixtures =  ['users']

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = AnonymousUser()

        self.staff_user = staff_user
        self.super_user = super_user

        self._template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            path.join(path.dirname(path.abspath(__file__)), 'fixtures'),
        )

        # decorate simple view above for testing
        self.login_url = '/my/login/page'
        decorator = user_passes_test_with_403(is_staff)
        self.decorated = decorator(simple_view)

    def tearDown(self):
        # restore any configured template dirs
        settings.TEMPLATE_DIRS = self._template_dirs

    def test_function_wrapping(self):
        self.assertEqual(self.decorated.__doc__, simple_view.__doc__,
            "decorated method docstring matches original method docstring")
        self.assertEqual(self.decorated.__name__, simple_view.__name__,
            "decorated method name matches original method name")

    def test_logged_in_allowed(self):
        # set request to use staff account
        self.request.user = self.staff_user
        response = self.decorated(self.request)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with superuser" \
                % (expected, got))
        self.assert_("Hello, World" in response.content,
                     "response should contain actual view content")


class UserPassesTestWithAjaxTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = AnonymousUser()

        self.staff_user = staff_user
        self.super_user = super_user

        self._template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            path.join(path.dirname(path.abspath(__file__)), 'fixtures'),
        )

        # decorate simple view above for testing
        # - generic view
        decorator = user_passes_test_with_ajax(is_staff)
        self.decorated = decorator(simple_view)

        # login required variant
        decorator = login_required_with_ajax()
        self.login_required_view = decorator(simple_view)

    def tearDown(self):
        # restore any configured template dirs
        settings.TEMPLATE_DIRS = self._template_dirs

    def test_anonymous_human(self):
        response = self.decorated(self.request)
        self.assert_(response['Location'].startswith(settings.LOGIN_URL),
                "decorated view redirects to login page for anonymous user")
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with non-ajax anonymous request" \
                % (expected, got))

        response = self.login_required_view(self.request)
        self.assert_(response['Location'].startswith(settings.LOGIN_URL),
                "decorated view redirects to login page for anonymous user")
        expected, got = 302, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with non-ajax anonymous request" \
                % (expected, got))

    def test_anonymous_ajax(self):
        # simulate ajax request
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = self.decorated(self.request)
        expected, got = 401, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with anonymous ajax request" \
                % (expected, got))

        # login required variant
        response = self.login_required_view(self.request)
        expected, got = 401, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for login required decorated view with anonymous ajax request" \
                % (expected, got))

    def test_allowed(self):
        # set request to use staff account
        self.request.user = self.staff_user
        response = self.decorated(self.request)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with non-ajax request as staff" \
                % (expected, got))
        self.assert_("Hello, World" in response.content,
                     "response should contain actual view content")

        # ajax request should behave the same way
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = self.decorated(self.request)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with ajax request as staff" \
                % (expected, got))
        self.assert_("Hello, World" in response.content,
            "response should contain actual view content")

        # login required variant
        self.request.user = self.staff_user
        response = self.login_required_view(self.request)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with non-ajax request as staff" \
                % (expected, got))
        self.assert_("Hello, World" in response.content,
                     "response should contain actual view content")

        # ajax request should behave the same way
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = self.login_required_view(self.request)
        expected, got = 200, response.status_code
        self.assertEqual(expected, got,
                "expected status code %s but got %s for decorated view with ajax request as staff" \
                % (expected, got))
        self.assert_("Hello, World" in response.content,
                     "response contains actual view content")

    def test_function_wrapping(self):
        for decorated_view in [self.decorated, self.login_required_view]:
            self.assertEqual(decorated_view.__doc__, simple_view.__doc__,
                "decorated method docstring matches original method docstring")
            self.assertEqual(decorated_view.__name__, simple_view.__name__,
                "decorated method name matches original method name")

if __name__ == '__main__':
    main()
