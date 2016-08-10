#!/usr/bin/env python

# file test_djangoextras/test_formfields.py
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

import re
import unittest

from django import forms
from django.conf import settings
from django.forms import ValidationError
from django.forms.formsets import BaseFormSet

from eulcommon.djangoextras.formfields import W3CDateWidget, DynamicSelect, DynamicChoiceField


class W3CDateWidgetTest(unittest.TestCase):

    def setUp(self):
        self.widget = W3CDateWidget()

    def test_value_from_datadict(self):
        name = 'date'
        data = {'date_year': '1999',
            'date_month': '01',
            'date_day': '31'
        }
        self.assertEqual('1999-01-31', self.widget.value_from_datadict(data, [], name))
        data['date_day'] = ''
        self.assertEqual('1999-01', self.widget.value_from_datadict(data, [], name))
        data['date_month'] = ''
        self.assertEqual('1999', self.widget.value_from_datadict(data, [], name))

        # if day is specified but no month,  day will be ignored
        data['date_day'] = '15'
        self.assertEqual('1999', self.widget.value_from_datadict(data, [], name))

        self.assertEqual(None, self.widget.value_from_datadict({}, [], name),
            'value_from_datadict returns None when expected inputs are not present')

    def test_create_textinput(self):
        input = self.widget.create_textinput('date', '%s_month', '22', title='foo')
        self.assert_(input.startswith('<input'))
        self.assert_('type="text"' in input)
        self.assert_('name="date_month"' in input)
        self.assert_('id="id_date_month"' in input)
        self.assert_('value="22"' in input)
        self.assert_('title="foo"' in input)

    def test_render(self):
        inputs = self.widget.render('date', '1999-12-31')
        re_flags = re.MULTILINE | re.DOTALL
        self.assert_(re.match(r'<input.*>.*\/.*<input.*>.*\/.*<input.*>', inputs,
            re_flags), 'render output has 3 inputs separated by /')

        self.assert_(re.match(r'<input.*maxlength="4".*name="date_year"', inputs, re_flags),
            'year input is in rendered widget output with max length of 4')
        self.assert_(re.match(r'<input.*maxlength="2".*name="date_month"', inputs, re_flags),
            'month input is in rendered widget output with max length of 2')
        self.assert_(re.match(r'<input.*maxlength="2".*name="date_day"', inputs, re_flags),
            'day input is in rendered widget output with max length of 2')

        # invalid initial value results in default MM DD YYYY placeholder values.
        inputs = self.widget.render('date', 'foo-bar-baz')
        self.assert_('value="MM"' in inputs,
            'Invalid intial value should result in a default MM in the month input')
        self.assert_('value="DD"' in inputs,
            'Invalid intial value should result in a default DD in the day input')
        self.assert_('value="YYYY"' in inputs,
            'Invalid intial value should result in a default YYYY in the year input')


class DynamicSelectTest(unittest.TestCase):
    def setUp(self):
        self.widget = DynamicSelect(choices=self.get_choices)
        self.choices = []

    def get_choices(self):
        return self.choices

    def test_render(self):
        self.choices = [('1', 'one'),
                        ('2', 'two'),
                        ('3', 'three')]
        html = self.widget.render('values', None)
        self.assert_('one' in html, 'render includes "one"')
        self.assert_('two' in html, 'render includes "two"')
        self.assert_('three' in html, 'render includes "three"')

        self.choices = [('a', 'alpha'),
                        ('b', 'beta'),
                        ('c', 'gamma')]
        html = self.widget.render('values', None)
        self.assert_('alpha' in html, 'render includes "alpha"')
        self.assert_('beta' in html, 'render includes "beta"')
        self.assert_('gamma' in html, 'render includes "gamma"')

class DynamicChoiceFieldTest(unittest.TestCase):
    def setUp(self):
        self.field = DynamicChoiceField(choices=self.get_choices)
        self.choices = []

    def get_choices(self):
        return self.choices

    def test_choices(self):
        self.choices = [('1', 'one'),
                        ('2', 'two'),
                        ('3', 'three')]
        self.assertEqual(self.choices, self.field.choices)

    def test_set_choices(self):
        def other_choices():
            return [('a', 'ay'), ('b', 'bee'), ('c', 'cee')]

        # should be able to set choices with a new callable
        self.field.choices = other_choices
        self.assertEqual(other_choices(), self.field.choices)
        # updating field choices also updates widget choices
        self.assertEqual(other_choices(), self.field.widget.choices)


if __name__ == '__main__':
    main()
