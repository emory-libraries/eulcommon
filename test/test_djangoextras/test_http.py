# file test_djangoextras/test_http.py
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


from unittest import TestCase
from django.http import HttpResponse, HttpRequest

from eulcommon.djangoextras.http import content_negotiation


def html_view(request):
    "a simple view for testing content negotiation"
    return HttpResponse("HTML")

def xml_view(request):
    return HttpResponse("XML")

def json_view(request):
    return HttpResponse("JSON")

class ContentNegotiationTest(TestCase):
    # known browser accept headers - taken from https://developer.mozilla.org/en/Content_negotiation
    FIREFOX = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    CHROME = 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
    # same Accept header used by both Safari and Google Chrome
    IE8 = 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*'

    def setUp(self):
        self.request = HttpRequest()

        # add content negotiation to test view defined above for testing
        decorator = content_negotiation({'application/xml': xml_view})
        self.negotiated_view = decorator(html_view)

    def test_default(self):
        # no accept header specified - should use default view
        response = self.negotiated_view(self.request)
        self.assertEqual("HTML", response.content)
        self.assertEqual('Accept', response['vary'],
            "response should have a 'Vary: Accept' header")

    def test_custom_default(self):
        # no accept header, should return user specified default view.
        decorator = content_negotiation({'application/xml': xml_view, 'text/html': html_view}, default_type="application/json")
        negotiated_view = decorator(json_view)
        response = negotiated_view(self.request)
        self.assertEqual("JSON", response.content)

    def test_html(self):
        self.request.META['HTTP_ACCEPT'] = 'text/html, application/xhtml+xml'
        response = self.negotiated_view(self.request)
        self.assertEqual("HTML", response.content)

    def test_xml(self):
        self.request.META['HTTP_ACCEPT'] = 'application/xml'
        response = self.negotiated_view(self.request)
        self.assertEqual("XML", response.content)

    def test_browsers(self):
        # some browsers request things oddly so they might not get what they actually want
        # confirm that these known browsers get the default text/html content instead of application/xml
        self.request.META['HTTP_ACCEPT'] = self.FIREFOX
        response = self.negotiated_view(self.request)
        self.assertEqual("HTML", response.content,
            "got HTML content with Firefox Accept header")

        self.request.META['HTTP_ACCEPT'] = self.CHROME
        response = self.negotiated_view(self.request)
        self.assertEqual("HTML", response.content,
            "got HTML content with Chrome/Safari Accept header")

        self.request.META['HTTP_ACCEPT'] = self.IE8
        response = self.negotiated_view(self.request)
        self.assertEqual("HTML", response.content,
            "got HTML content with IE8 Accept header")

    def test_function_wrapping(self):
        # make sure we play nice for documentation
        self.assertEqual(self.negotiated_view.__doc__, html_view.__doc__,
            "decorated method docstring matches original method docstring")
        self.assertEqual(self.negotiated_view.__name__, html_view.__name__,
            "decorated method name matches original method name")


if __name__ == '__main__':
    main()
