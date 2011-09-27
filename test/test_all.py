#!/usr/bin/env python

# file test_all.py
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

import os
import unittest
import logging.config

from testcore import tests_from_modules, get_testsuite_runner

test_modules = (
    'test_binfile',
    'test_djangoextras', 
    'test_searchutil',
    )

if __name__ == '__main__':
    # load logging config, if any
    test_dir = os.path.dirname(os.path.abspath(__file__))
    LOGGING_CONF = os.path.join(test_dir, 'logging.conf')
    if os.path.exists(LOGGING_CONF):
        logging.config.fileConfig(LOGGING_CONF)

    # generate test suite from test modules
    alltests = unittest.TestSuite(
        (unittest.TestLoader().loadTestsFromName(mod) for mod in test_modules)
    )
    
    test_runner = get_testsuite_runner()
    # djangoextras code aren't django apps per-se, so just run them as extra tests
    test_runner.run_tests([], extra_tests=alltests)
