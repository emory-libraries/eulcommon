# file eulcommon/binfile/outlookexpress.py
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

'''

Map binary email folder index and content files for Outlook Express
4.5 for Macintosh to Python objects.

What documentation is available suggests that Outlook Express stored
email in either .mbx or .dbx format, but in Outlook Express 4.5 for
Macintosh, each mail folder consists of a directory with an ``Index``
file and an optional ``Mail`` file (no Mail file is present when a
mail folder is empty).

'''

import email
from eulcommon import binfile
import logging
import os

logger = logging.getLogger(__name__)

class MacIndex(binfile.BinaryStructure):
    '''A :class:`~eulcommon.binfile.BinaryStructure` for the Index
    file of an Outlook Express 4.5 for Mac email folder.'''

    MAGIC_NUMBER = 'FMIn'  # data file is FMDF
    '''Magic Number for Outlook Express 4.5 Mac Index file'''
    _magic_num = binfile.ByteField(0, 4)
    # first four bytes should match magic number

    header_length = 28  # 28 bytes at beginning of header
    '''length of the binary header at the beginning of the Index file'''

    total_messages = binfile.IntegerField(13, 16)
    '''number of email messages in this folder'''
    # seems to be number of messages in the folder (or close, anyway)


    def sanity_check(self):
        if self._magic_num != self.MAGIC_NUMBER:
            logger.debug('Index file sanity check failed')

        return self._magic_num == self.MAGIC_NUMBER


    @property
    def messages(self):
        '''A generator yielding the :class:`MacIndexMessage`
        structures in this index file.'''

        # The file contains the fixed-size file header followed by
        # fixed-size message structures, followed by minimal message
        # information (subject, from, to).  Start after the file
        # header and then simply return the message structures in
        # sequence until we have returned the number of messages in
        # this folder, ignoring the minimal message information at the
        # end of the file.

        offset = self.header_length # initial offset
        # how much of the data in this file we expect to use, based on
        # the number of messages in this folder and the index message block size
        maxlen = self.header_length + self.total_messages * MacIndexMessage.LENGTH
        while offset < maxlen:
             yield MacIndexMessage(mm=self.mmap, offset=offset)
             offset += MacIndexMessage.LENGTH



class MacIndexMessage(binfile.BinaryStructure):
    '''Information about a single email message within the
    :class:`MacIndex`.'''

    LENGTH = 52
    '''size of a single message information block'''
    offset = binfile.IntegerField(13, 16)
    '''the offset of the raw email data in the folder data file'''
    size = binfile.IntegerField(17, 20)
    '''the size of the raw email data in the folder data file'''


class MacMail(binfile.BinaryStructure):
    '''A :class:`~eulcommon.binfile.BinaryStructure` for the Mail file
    of an Outlook Express 4.5 for Mac email folder.  The Mail file
    includes the actual contents of any email files in the folder,
    which must be accessed based on the message offset and size from
    the Index file.
    '''
    MAGIC_NUMBER = 'FMDF'  # data file (?)
    '''Magic Number for a mail content file within an Outlook Express
    4.5 for Macintosh folder'''
    _magic_num = binfile.ByteField(0, 4)  # should match magic number

    def sanity_check(self):
        if self._magic_num != self.MAGIC_NUMBER:
            logger.debug('Mail file sanity check failed')
        return self._magic_num == self.MAGIC_NUMBER

    def get_message(self, offset, size):
        '''Get an individual :class:`MacMailMessage` within a Mail
        data file, based on size and offset information from the
        corresponding :class:`MacIndexMessage`.

        :param offset: offset within the Mail file where the desired
            message begins, i.e. :attr:`MacMailMessage.offset`
        :param size: size of the message,
            i.e. :attr:`MacMailMessage.size`
        '''
        return MacMailMessage(size=size, mm=self.mmap, offset=offset)


class MacMailMessage(binfile.BinaryStructure):
    '''A single email message within the Mail data file, as indexed by
    a :class:`MacIndexMessage`.  Consists of a variable length header
    or message summary followed by the content of the email (also
    variable length).

    The size of a single :class:`MacMailMessage` is stored in the
    :class:`MacIndexMessage` but not (as far as we have determined) in
    the Mail data file, an individual message must be initialized with
    the a size parameter, so that the correct content can be returned.

    :param size: size of this message (as determined by
    :attr:`MacIndexMessage.size`); **required** to return
    :attr:`data` correctly.

    '''
    header_type = binfile.ByteField(0, 4)
    '''Each mail message begins with a header, starting with either
    ``MSum`` (message summary, perhaps) or ``MDel`` for deleted
    messages.'''

    MESSAGE = 'MSum'
    'Header string indicating a normal message'
    DELETED_MESSAGE = 'MDel'
    'Header string indicating a deleted message'

    content_offset = binfile.IntegerField(5, 8)
    '''offset within this message block where the message summary
    header ends and message content begins'''

    def __init__(self, size, *args, **kwargs):
        self.size = size
        super(MacMailMessage, self).__init__(*args, **kwargs)

    @property
    def deleted(self):
        'boolean flag indicating if this is a deleted message'
        return self.header_type == self.DELETED_MESSAGE

    @property
    def data(self):
        '''email content for this message'''
        # return data after any initial offset, plus content offset to
        # skip header, up to the size of this message
        return self.mmap[self.content_offset + self._offset: self._offset + self.size]

    def as_email(self):
        '''Return message data as a :class:`email.message.Message`
        object.'''
        return email.message_from_string(self.data)


class MacFolder(object):
    '''Wrapper object for an Outlook Express 4.5 for Mac folder, with
    a :class:`MacIndex` and an optional :class:`MacMail`.

    :param folder_path: path to the Outlook Express 4.5 folder
        directory, which must contain at least an ``Index`` file (and
        probably a ``Mail`` file, for non-empty folders)

    '''

    index = None
    data = None

    def __init__(self, folder_path):
        index_filename = os.path.join(folder_path, 'Index')
        data_filename = os.path.join(folder_path, 'Mail')
        if os.path.exists(index_filename):
            self.index = MacIndex(index_filename)
        else:
            raise RuntimeError('Outlook Express Folder Index does not exist at "%s"' % \
                            index_filename)
        # data file will not be present for empty folders
        if os.path.exists(data_filename):
            self.data = MacMail(data_filename)

    @property
    def count(self):
        'Number of email messages in this folder'
        return self.index.total_messages

    skipped_chunks = None
    '''Number of data chunks skipped between raw messages, based on
    offset and size.  (Only set after iterating through messages.)'''

    @property
    def raw_messages(self):
        '''A generator yielding a :class:`MacMailMessage` binary
        object for each message in this folder, based on message index
        information in :class:`MacIndex` and content in
        :class:`MacMail`.'''
        if self.data:
            # offset for first message, at end of Mail data file header
            last_offset = 24
            self.skipped_chunks = 0

            for msginfo in self.index.messages:
                msg = self.data.get_message(msginfo.offset, msginfo.size)
                # Index file seems to references messages in order by
                # offset; check for data skipped between messages.
                if msginfo.offset > last_offset:
                    logger.debug('Skipped %d bytes between %s (%s) and %s (%s)',
                           msginfo.offset - last_offset,
                           last_offset, hex(last_offset),
                           msginfo.offset, hex(msginfo.offset))

                    self.skipped_chunks += 1
                last_offset = msginfo.offset + msginfo.size

                yield msg

    @property
    def messages(self):
        '''A generator yielding an :class:`email.message.Message` for
        each message in this folder, based on message index
        information in :class:`MacIndex` and content in
        :class:`MacMail`.  Does **not** include deleted messages.'''
        return self._messages()

    @property
    def all_messages(self):
        '''Same as :attr:`messages` except deleted messages are included.'''
        return self._messages(skip_deleted=False)

    def _messages(self, skip_deleted=True):
        # common logic for messages / all_messages
        for raw_msg in self.raw_messages:
            if skip_deleted and raw_msg.deleted:
                continue
            yield raw_msg.as_email()
