#!/usr/bin/env python

# file eulcommon/searchutil.py
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

"""This module contains utilities for searching."""

import logging
from ply import lex

__all__ = ('search_terms', 'pages_to_show')

logger = logging.getLogger(__name__)

tokens = ('WORD', 'PHRASE')

t_WORD = r'[^\s"]+'

@lex.TOKEN(r'"[^"]*"')
def t_PHRASE(t):
    # strip off the outer quotes - we just want the text value
    t.value = t.value[1:-1]
    return t

def t_error(t):
    logger.debug('skipping illegal/unmatched character ' + repr(t.value[0]))
    t.lexer.skip(1)

def search_terms(q):
    '''Takes a search string and parses it into a list of keywords and
    phrases.'''
    lexer = lex.lex()
    lexer.input(q)
    # iterate through all the tokens and make a list of token values
    # (which are the actual words and phrases)
    return [ tok.value for tok in iter(lexer.token, None) ]


def pages_to_show(paginator, page, page_labels={}):
    """Generate a dictionary of pages to show around the current page. Show
    3 numbers on either side of the specified page, or more if close to end or
    beginning of available pages.

    :param paginator: django :class:`~django.core.paginator.Paginator`,
    	populated with objects
    :param page: number of the current page
    :param page_labels: optional dictionary of page labels, keyed on page number
    :rtype: dictionary; keys are page numbers, values are page labels
    """    
    show_pages = {} # FIXME; do we need OrderedDict here ? 
    def get_page_label(index):
        if index in page_labels:
            return page_labels[index]
        else:
            return unicode(index)
        
    if page != 1:
        before = 3      # default number of pages to show before the current page
        if page >= (paginator.num_pages - 3):   # current page is within 3 of end
            # increase number to show before current page based on distance to end
            before += (3 - (paginator.num_pages - page))
        for i in range(before, 0, -1):    # add pages from before away up to current page
            if (page - i) >= 1:
                # if there is a page label available, use that as dictionary value
                show_pages[page - i] = get_page_label(page - i)
                
    # show up to 3 to 7 numbers after the current number, depending on
    # how many we already have
    for i in range(7 - len(show_pages)):
        if (page + i) <= paginator.num_pages:
            # if there is a page label available, use that as dictionary value
            show_pages[page + i] = get_page_label(page + i)

    return show_pages
