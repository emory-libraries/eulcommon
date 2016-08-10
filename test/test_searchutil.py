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
from django.core.paginator import Paginator
from eulcommon.searchutil import search_terms, parse_search_terms, \
     pages_to_show


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

        # search_terms should ignore colons
        self.assertEqual(['one', 'two:', 'three'],
                         search_terms(' one two: three'))
        # search_terms should ignore colons
        self.assertEqual(['one', 'two:three', 'four'],
                         search_terms(' one two:three four'))
        self.assertEqual(['one', 'two:"three\tfour"', 'five'],
                         search_terms(' one two:"three\tfour" five'))


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

class ParseSearchTermsTest(unittest.TestCase):

    def test_words(self):
        # search strings with single words
        self.assertEqual([(None, 'word')], parse_search_terms('word'))
        self.assertEqual([(None, 'multiple'), (None, 'words')],
                         parse_search_terms('multiple words'))
        self.assertEqual([(None, 'extraneous'), (None, 'whitespace')],
                         parse_search_terms('   extraneous      whitespace '))

    def test_phrases(self):
        # quoted phrases
        self.assertEqual([(None, 'exact phrase')],
                         parse_search_terms('"exact phrase"'))

    def test_fields(self):
        self.assertEqual([('title', 'willows')],
                         parse_search_terms('title:willows'))

        self.assertEqual([('title', 'willows'), ('title', 'wind')],
                         parse_search_terms('title:willows title:wind'))

        self.assertEqual([(None, 'frog'), (None, 'toad'), ('title', 'willows'),
                          ('title', 'wind')],
                         parse_search_terms('frog toad title:willows title:wind'))


class PagesToShowTest(unittest.TestCase):

    def test_pages_to_show(self):
        paginator = Paginator(range(300), 10)
        # range of pages at the beginning
        pages = pages_to_show(paginator, 1)
        self.assertEqual(7, len(pages), "show pages returns 7 items for first page")
        self.assert_(1 in pages, "show pages includes 1 for first page")
        self.assert_(6 in pages, "show pages includes 6 for first page")
        # default labels
        self.assertEqual('1', pages[1])
        self.assertEqual('6', pages[6])
        # custom labels
        pages = pages_to_show(paginator, 1, {1: 'one', 2: 'two'})
        self.assertEqual('one', pages[1])
        self.assertEqual('two', pages[2])
        self.assertEqual('6', pages[6])  # default because not specified

        pages = pages_to_show(paginator, 2)
        self.assert_(1 in pages, "show pages for page 2 includes 1")
        self.assert_(2 in pages, "show pages for page 2 includes 2")
        self.assert_(3 in pages, "show pages for page 2 includes 3")

        # range of pages in the middle
        pages = pages_to_show(paginator, 15)
        self.assertEqual(7, len(pages),
                         "show pages returns 7 items for middle of page result")
        self.assert_(15 in pages,
                     "show pages includes current page for middle of page result")
        self.assert_(12 in pages,
            "show pages includes third page before current page for middle of page result")
        self.assert_(18 in pages,
            "show pages includes third page after current page for middle of page result")

        # range of pages at the end
        pages = pages_to_show(paginator, 30)
        self.assertEqual(7, len(pages),
                         "show pages returns 7 items for last page")
        self.assert_(30 in pages,
                     "show pages includes last page for last page of results")
        self.assert_(24 in pages,
                     "show pages includes 6 pages before last page for last page of results")




if __name__ == '__main__':
    main()
