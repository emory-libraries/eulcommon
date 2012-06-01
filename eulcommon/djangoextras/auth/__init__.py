# file eulcommon/djangoextras/auth/__init__.py
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

"""Customized decorators that enhance the default behavior of
:meth:`django.contrib.auth.decorators.permission_required`.

The default behavior of :meth:`django.contrib.auth.decorators.permission_required`
for any user does not meet the required permission level is to redirect them to
the login page-- even if that user is already logged in. For more discussion of 
this behavior and current status in Django, see:
http://code.djangoproject.com/ticket/4617

These decorators work the same way as the Django equivalents, with the added
feature that if the user is already logged in and does not have the required
permission, they will see 403 page instead of the login page.

The decorators should be used exactly the same as their django equivalents.

The code is based on the django snippet code at http://djangosnippets.org/snippets/254/
"""

from eulcommon.djangoextras.auth.decorators import *
