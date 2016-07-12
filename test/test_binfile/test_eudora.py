# file test_binfile/test_eudora.py
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

from eulcommon.binfile import eudora

TEST_ROOT = os.path.dirname(__file__)
def fixture(fname):
    return os.path.join(TEST_ROOT, 'fixtures', fname)

class TestEudora(unittest.TestCase):
    def test_members(self):
        fname = fixture('In.toc')
        obj = eudora.Toc(fname)

        self.assertEqual(obj.version, 1)
        self.assertEqual(obj.name, 'In')

        messages = list(obj.messages)
        self.assertEqual(len(messages), 2)

        # note: we don't actually test all of the fields here. it's not
        # clear what a few of them actually are, so we only test the ones we
        # know how to interpret.

        self.assertTrue(isinstance(messages[0], eudora.Message))
        self.assertEqual(messages[0].offset, 0)
        self.assertEqual(messages[0].size, 1732)
        self.assertEqual(messages[0].body_offset, 955)
        self.assertEqual(messages[0].to, 'Somebody ')
        self.assertEqual(messages[0].subject, 'Welcome')

        # second message isn't *necessarily* immediately after first, but
        # in this case it is.
        self.assertEqual(messages[1].offset, 1732)


if __name__ == '__main__':
    main()
