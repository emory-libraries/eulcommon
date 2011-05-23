# file testcore.py
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

import unittest

import os
# must be set before importing anything from django
os.environ['DJANGO_SETTINGS_MODULE'] = 'testsettings'

from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings

def tests_from_modules(modnames):
    return [ unittest.findTestCases(__import__(modname, fromlist=['*']))
             for modname in modnames ]

def get_test_runner(runner=unittest.TextTestRunner()):
    # use xmlrunner if available; otherwise, fall back to text runner
    try:
        import xmlrunner
        runner = xmlrunner.XMLTestRunner(output=settings.TEST_OUTPUT_DIR)
    except ImportError:
        pass
    return runner

def get_testsuite_runner(runner=DjangoTestSuiteRunner()):
    # use xmlrunner if available; otherwise, fall back to text runner

    try:
        import xmlrunner.extra.djangotestrunner
        runner = xmlrunner.extra.djangotestrunner.XMLTestRunner()
        # when running as a suite, output dir must be set in django settings
    except ImportError:
        pass
    return runner
    

def main(testRunner=None, *args, **kwargs):
    if testRunner is None:
        testRunner = get_test_runner()

    unittest.main(testRunner=testRunner, *args, **kwargs)
