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
from django import VERSION as django_version

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'not that secret but is now required!~'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'eulcommon-test.db')
    }
}

INSTALLED_APPS = [
    # errors on django 1.9 if contenttypes is not included here
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'eulcommon',
    'eulcommon.djangoextras.taskresult',
    'djcelery',
]


# context processors required for taskresult tests
TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages"
]

# configure context processors in the correct location depending on
# version of django we're testing against
if django_version < (1, 8):
    TEMPLATE_CONTEXT_PROCESSORS.extend([
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
    ])
else:
    TEMPLATE_CONTEXT_PROCESSORS.extend([
        "django.template.context_processors.debug",
        "django.template.context_processors.i18n",
        "django.template.context_processors.media",
        "django.template.context_processors.static",
        "django.template.context_processors.tz",
    ])

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
    # includes 403.html template
    os.path.join(BASE_DIR, 'test_djangoextras', 'fixtures'),
]

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': TEMPLATE_DIRS
    },
]

ROOT_URLCONF = 'test_urls'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'eulcommon-test-cache',
    }
}

# celery config for taskresult
CELERY_ALWAYS_EAGER = True
CELERY_RESULT_BACKEND = 'djcelery.backends.cache:CacheBackend'
