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

"""This module contains utilities for searching. Currently it exports only a
single symbol, :func:`search_terms`.
"""

import logging
from ply import lex

__all__ = ('search_terms')

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
