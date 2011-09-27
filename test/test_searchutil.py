#!/usr/bin/env python

# file test_searchutil.py
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

from eulcommon.searchutil import search_terms
from testcore import main

class SearchTermsTest(unittest.TestCase):

    def test_words(self):
        # search strings with single words
        self.assertEqual(['word'], search_terms('word'))
        self.assertEqual(['multiple', 'words'],
                         search_terms('multiple words'))
        self.assertEqual(["don't"], search_terms("don't"))

        self.assertEqual(['one', '2.5'], search_terms('one 2.5'))

        self.assertEqual(['extraneous', 'whitespace'],
                         search_terms('  extraneous      whitespace '))

    def test_phrases(self):
        # quoted phrases
        self.assertEqual(['exact phrase'], search_terms('"exact phrase"'))
        self.assertEqual(["'single", "quotes'"], search_terms("'single quotes'"))
        self.assertEqual(['exact phrase', 'with', 'keyword'],
                         search_terms('"exact phrase" with keyword'))
        # phrase with internal apostrophe
        self.assertEqual(["I don't", "know"], search_terms('"I don\'t" know'))
        # non-matching quotes ignored
        self.assertEqual(["non", "phrase'"], search_terms('"non phrase\''))

        self.assertEqual(["'hello'"], search_terms('"\'hello\'"'))
        self.assertEqual(["'Tis a beautiful day"],
                         search_terms('"\'Tis a beautiful day"'))

    def test_wildcards(self):
        # beginning of a word
        self.assertEqual(['*nd', 'to', 'mouth'], search_terms('*nd to mouth'))
        self.assertEqual(['?nd', 'or'], search_terms(' ?nd or'))
        # middle of a word
        self.assertEqual(['w*ther', 'or', 'not'],
                         search_terms('w*ther or not'))
        self.assertEqual(['wh?ther', 'thou', 'goest'],
                         search_terms('wh?ther thou goest'))
        # end of a word
        self.assertEqual(['th*'], search_terms('th*'))
        self.assertEqual(['th?'], search_terms('th?'))


if __name__ == '__main__':
    main()
