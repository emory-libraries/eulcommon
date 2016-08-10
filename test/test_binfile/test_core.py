#!/usr/bin/env python

# file test_binfile/test_core.py
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
import mmap

from eulcommon import binfile


TEST_ROOT = os.path.dirname(__file__)
def fixture(fname):
    return os.path.join(TEST_ROOT, 'fixtures', fname)

class BinaryStructureTest(unittest.TestCase):
    def test_init_with_fname(self):
        fname = fixture('numbers.bin')
        obj = binfile.BinaryStructure(fname)
        self.assertEqual(obj.mmap[0], '\x00')
        self.assertEqual(obj.mmap[1], '\x01')

    def test_init_with_fd(self):
        fobj = open(fixture('numbers.bin'))
        obj = binfile.BinaryStructure(fobj)
        self.assertEqual(obj.mmap[0], '\x00')
        self.assertEqual(obj.mmap[1], '\x01')

    def test_init_with_mm(self):
        fobj = open(fixture('numbers.bin'))
        mm = mmap.mmap(fobj.fileno(), 0, prot=1)
        obj = binfile.BinaryStructure(mm=mm)
        self.assertEqual(obj.mmap[0], '\x00')
        self.assertEqual(obj.mmap[1], '\x01')

    # we test offset below: it's only used implicitly by fields


class TestObject(binfile.BinaryStructure):
    byte = binfile.ByteField(0, 2)
    str = binfile.LengthPrependedStringField(2)
    int = binfile.IntegerField(2, 4)


class FieldTest(unittest.TestCase):
    def setUp(self):
        fname = fixture('numbers.bin')
        self.obj = TestObject(fname)
        self.offset_obj = TestObject(fname, offset=1)

    def test_byte(self):
        self.assertEqual(self.obj.byte, '\x00\x01')
        self.assertEqual(self.offset_obj.byte, '\x01\x02')

    def test_str(self):
        # byte 2 has decimal value 2, so 2-byte string:
        self.assertEqual(self.obj.str, '\x03\x04')
        # byte 3 has decimal value 3, so 3-byte string:
        self.assertEqual(self.offset_obj.str, '\x04\x05\x06')

    def test_int(self):
        # 2*256 + 3
        self.assertEqual(self.obj.int, 515)
        # 3*256 + 4
        self.assertEqual(self.offset_obj.int, 772)


if __name__ == '__main__':
    main()
