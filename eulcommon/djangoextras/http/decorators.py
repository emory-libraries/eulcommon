# file eulcommon/djangoextras/http/decorators.py
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

from functools import wraps
import mimeparse

from django.http import HttpResponse
from django.utils.cache import patch_vary_headers

def content_negotiation(formats, default_type='text/html'):
    """
    Provides basic content negotiation and returns a view method based on the
    best match of content types as indicated in formats.

    :param formats: dictionary of content types and corresponding methods
    :param default_type: string the decorated method is the return type for.

    Example usage::

        def rdf_view(request, arg):
            return RDF_RESPONSE

        @content_negotiation({'application/rdf+xml': rdf_view})
        def html_view(request, arg):
            return HTML_RESPONSE

    The above example would return the rdf_view on a request type of
    ``application/rdf+xml`` and the normal view for anything else.

    Any :class:`django.http.HttpResponse` returned by the view method chosen
    by content negotiation will have a 'Vary: Accept' HTTP header added.

    **NOTE:** Some web browsers do content negotiation poorly, requesting
    ``application/xml`` when what they really want is ``application/xhtml+xml`` or
    ``text/html``.  When this type of Accept request is detected, the default type
    will be returned rather than the best match that would be determined by parsing
    the Accept string properly (since in some cases the best match is
    ``application/xml``, which could return non-html content inappropriate for
    display in a web browser).
    """    
    def _decorator(view_method):
        @wraps(view_method)
        def _wrapped(request, *args, **kwargs):
            # Changed this to be a value passed as a method argument defaulting
            # to text/html instead so it's more flexible.
            # default_type = 'text/html'  # If not specificied assume HTML request.

            # Add text/html for the original method if not already included.
            if default_type not in formats:
                formats[default_type] = view_method

            try:
                req_type = request.META['HTTP_ACCEPT']
                
                # If this request is coming from a browser like that, just
                # give them our default type instead of honoring the actual best match
                # (see note above for more detail)
                if '*/*' in req_type:
                    req_type = default_type
                    
            except KeyError:
                req_type = default_type

            # Get the best match for the content type requested.
            content_type = mimeparse.best_match(formats.keys(),
                                                req_type)
                                                
            # Return the view matching content type or the original view
            # if no match.
            if not content_type or content_type not in formats:
                response = view_method(request, *args, **kwargs)
            else:
                response = formats[content_type](request, *args, **kwargs)

            # set a Vary header to indicate content may vary based on Accept header            
            if isinstance(response, HttpResponse):    # views should return HttpResponse objects, but check to be sure
                # note: using the same utility method used by django's vary_on_headers decorator
                patch_vary_headers(response, ['Accept'])
            return response
        return _wrapped
    return _decorator
