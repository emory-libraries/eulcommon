# file test_binfile/test_outlookexpress.py
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

from email import message
import unittest
import os

from eulcommon.binfile import outlookexpress


TEST_ROOT = os.path.dirname(__file__)
# Outlook Express 4.5 Mac folder directory inside fixtures directory
FIXTURE_FOLDER = os.path.join(TEST_ROOT, 'fixtures', 'oemacfolder')

class TestMacIndex(unittest.TestCase):
    index_filename = os.path.join(FIXTURE_FOLDER, 'Index')
    data_filename = os.path.join(FIXTURE_FOLDER, 'Mail')

    def test_basic_properties(self):
        idx = outlookexpress.MacIndex(self.index_filename)

        self.assertEqual(2, idx.total_messages)
        self.assertTrue(idx.sanity_check())

        not_idx = outlookexpress.MacIndex(self.data_filename)
        self.assertFalse(not_idx.sanity_check())

    def test_messages(self):
        idx = outlookexpress.MacIndex(self.index_filename)
        messages = list(idx.messages)
        self.assertEqual(len(messages), 2)

        self.assertTrue(isinstance(messages[0], outlookexpress.MacIndexMessage))

        self.assertEqual(24, messages[0].offset)
        self.assertEqual(392, messages[0].size)


class TestMacIndex(unittest.TestCase):
    index_filename = os.path.join(FIXTURE_FOLDER, 'Index')
    data_filename = os.path.join(FIXTURE_FOLDER, 'Mail')

    def test_basic_properties(self):
        data = outlookexpress.MacMail(self.data_filename)

        self.assertTrue(data.sanity_check())

        not_data = outlookexpress.MacMail(self.index_filename)
        self.assertFalse(not_data.sanity_check())

    # NOTE: can't test get_message independently, since
    # it requires size + offset from the Index file

class TestMacFolder(unittest.TestCase):

    def setUp(self):
        self.folder = outlookexpress.MacFolder(FIXTURE_FOLDER)

    def test_init(self):
        self.assert_(isinstance(self.folder.index,
                                outlookexpress.MacIndex))
        self.assert_(isinstance(self.folder.data,
                                outlookexpress.MacMail))

        # non-folder dir should raise an exception
        self.assertRaises(RuntimeError, outlookexpress.MacFolder,
                          TEST_ROOT)

    def test_count(self):
        self.assertEqual(2, self.folder.count)

    def test_messages(self):
        msgs = list(self.folder.messages)
        self.assertEqual(self.folder.count, len(msgs))
        msg = msgs[0]
        self.assert_(isinstance(msg, message.Message))

        # check email content to test size & offset handling
        self.assertEqual('Hi!', msg['Subject'])
        self.assertEqual('"Somebody" <somebody@example.com>', msg['From'])
        self.assertEqual('someone@nowhere.org', msg['To'])
        self.assertEqual('This is a test email generated with Outlook Express 4.5 for Mac.',
                         msg.get_payload())
        msg2 = msgs[1]
        self.assertEqual('hello again', msg2['Subject'])

        # if data is not set/unavailable
        self.folder.data = None
        self.assertEqual([], list(self.folder.messages))

    def test_raw_messages(self):
        raw_msgs = list(self.folder.raw_messages)
        self.assertEqual(self.folder.count, len(raw_msgs))
        self.assert_(isinstance(raw_msgs[0], outlookexpress.MacMailMessage))
        self.assertFalse(raw_msgs[0].deleted)

        # skipped chunks should be populated now; 0 for fixture folder
        self.assertEqual(0, self.folder.skipped_chunks)



if __name__ == '__main__':
    main()
