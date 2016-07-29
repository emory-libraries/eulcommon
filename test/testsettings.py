# file testsettings.py
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

# django settings file for unit tests
import os

SECRET_KEY = 'not that secret but is now required!~'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'eulcommon-test.db'
    }
}

INSTALLED_APPS = [
    # errors on django 1.9 if contenttypes is not included here
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'eulcommon',
]


# suppress normal template context processing
# for tests that render templates
TEMPLATE_CONTEXT_PROCESSORS = []

