# file test_djangoextras/test_validators.py
#
#   Copyright 2012 Emory University Libraries
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
from django.forms import ValidationError
from mock import Mock
import os

from eulcommon.djangoextras.validators import FileTypeValidator


class TestFileTypeValidator(unittest.TestCase):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_filename = os.path.join(base_dir, 'fixtures', 'test.pdf')

    def setUp(self):
        self.text_val = FileTypeValidator(types=['text/plain'])

        self.pdf_val = FileTypeValidator(types=['application/pdf'],
                                     message='Bad file!')
        self.pdf_or_text_val = FileTypeValidator(types=['application/pdf', 'text/plain'],
                                     message='Bad file!')

    def test_temporary_file(self):
        mockfile = Mock()
        mockfile.temporary_file_path.return_value = self.pdf_filename

        # should not raise validation error as pdf
        self.pdf_val(mockfile)
        self.pdf_or_text_val(mockfile)
        # not valid as text
        self.assertRaises(ValidationError, self.text_val, mockfile)


    def test_memory_file(self):
        data = {'content': 'this looks like plain text'}
        # valid as text
        self.text_val(data)
        self.pdf_or_text_val(data)
        # not valid as pdf
        self.assertRaises(ValidationError, self.pdf_val, data)

        class TestDataObject:
            def __init__(self, content):
                self.content = content

            def read(self):
                return self.content

        data = TestDataObject('more text')
        # valid as text
        self.text_val(data)
        self.pdf_or_text_val(data)
        # not valid as pdf
        self.assertRaises(ValidationError, self.pdf_val, data)


if __name__ == '__main__':
    main()
