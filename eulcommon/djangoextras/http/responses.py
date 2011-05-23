# file eulcommon/djangoextras/http/responses.py
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


# custom HTTP Responses that Django doesn't provide

from django.http import HttpResponse, HttpResponseRedirect

class HttpResponseSeeOtherRedirect(HttpResponseRedirect):
    """Variant of Django's :class:`django.http.HttpResponseRedirect`.  Redirect
    with status code 303, 'See Other'.  This code indicates that the redirected
    content is not a replacement for the requested content, but a different resource.
    """
    status_code = 303
    
class HttpResponseUnauthorized(HttpResponse):
    '''Variant of Django's :class:`django.http.HttpResponse` for status code
    401 'Unauthorized'.  Takes a single required argument of expected
    authentication method (currently only supports one) to populate the
    WWW-Authenticate header that is required in a 401 response.  Example use::

        HttpResponseUnauthorized('my realm')

    '''
    status_code = 401

    def __init__(self, realm='Restricted Access'):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % realm

class HttpResponseUnsupportedMediaType(HttpResponse):
    """Variant of Django's :class:`django.http.HttpResponse` with status
    code 415 Unsupported Media Type.
    """
    status_code = 415
