# file eulcommon/binfile/eudora.py
#
#   Copyright 2011 Emory University General Library
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

'''Map binary email table of contents files for the Eudora mail client to
Python objects.

The `Eudora <http://en.wikipedia.org/wiki/Eudora_(e-mail_client)>`_ email
client has a long history through the early years of email. It supported
versions for early Mac systems as well as early Windows OSes. Unfortunately,
most of them use binary file formats that are entirely incompatible with one
another. This module is aimed at one day reading all of them, but for now
practicality and immediate needs demand that it focus on the files saved by
a particular version on mid-90s Mac System 7.

That Eudora version stores email in flat (non-hierarchical) folders. It
stores each folder's email data in a single file akin to a Unix `mbox
<http://en.wikipedia.org/wiki/Mbox>`_ file, but with some key differences,
described below. In addition to this folder data file, each folder also
stores a binary "table of contents" index. In this version, a folder called
``In`` stores its index in a file called ``In.toc``. This file consists of a
fixed-size binary header with folder metadata, followed by fixed-size binary
email records containing cached email header metadata as well as the
location of the full email in the mbox-like data file. As the contents of
the folder are updated, these fixed-size binary email records are added,
removed, and reordered, apparently compacting the file as necessary so that
it matches the folder contents displayed to the application end user.

With the index serving to dictate the order of the emails and their
contents, their locations and sizes inside the data storage file become less
important. When emails are deleted from a folder, the index is updated, but
they are not removed immediately from the data file. Instead that data space
is marked as inactive and might be reused later when a new email is added to
the folder. As a result, the folder data file may contain stale and
out-of-order data and thus **cannot be read directly as a standard mbox
file**.

This module, then, provides classes for parsing the binary structures of the
index file and mapping them to Python objects. This binary file has gone
through many formats. Only one is represented in this module, though it
could certainly be expanded to support more. Parsers and information about
other versions of the index file are available at
http://eudora2unix.sourceforge.net/ and
http://users.starpower.net/ksimler/eudora/toc.html; these were immensely
helpful in reverse-engineering the version represented by this module.

This module exports the following names:
 * :class:`Toc` -- a :class:`~eulcommon.binfile.BinaryStructure` for the index
   file header
 * :class:`Message` -- a :class:`~eulcommon.binfile.BinaryStructure` for the
   fixed-length email metadata entries in the index files
'''

from eulcommon import binfile

class Toc(binfile.BinaryStructure):
    '''A :class:`~eulcommon.binfile.BinaryStructure` for an email folder index
    header.

    Only a few fields are currently represented; other fields contain
    interesting data but have not yet been reverse-engineered.
    '''

    LENGTH = 278
    '''the size of this binary header'''

    version = binfile.IntegerField(0, 2)
    '''the file format version'''
    name = binfile.LengthPrependedStringField(58)
    '''the user-displayed folder name, e.g., "In" for the default inbox'''

    @property
    def messages(self):
        '''a generator yielding the :class:`Message` structures in the index'''

        # the file contains the fixed-size file header followed by
        # fixed-size message structures. start after the file header and
        # then simply return the message structures in sequence until the
        # end of the file.

        offset = self.LENGTH
        while offset < len(self.mmap):
            yield Message(mm=self.mmap, offset=offset)
            offset += Message.LENGTH


class Message(binfile.BinaryStructure):
    '''A :class:`~eulcommon.binfile.BinaryStructure` for a single email's
    metadata cached in the index file.

    Only a few fields are currently represented; other fields contain
    interesting data but have not yet been reverse-engineered.
    '''

    LENGTH = 220
    '''the size of a single message header'''

    offset = binfile.IntegerField(0, 4)
    '''the offset of the raw email data in the folder data file'''
    size = binfile.IntegerField(4, 8)
    '''the size of the raw email data in the folder data file'''
    body_offset = binfile.IntegerField(8, 12)
    '''the offset of the body within the raw email data'''
    status = binfile.ByteField(12, 13)
    '''some kind of unspecified single-byte status field'''
    date = binfile.LengthPrependedStringField(13)
    '''a date value copied from email headers'''
    # bytes 14-61 not reverse-engineered
    priority = binfile.ByteField(62, 63)
    '''some kind of unspecified single-byte priority field'''
    # bytes 63-77 not reverse-engineered
    to = binfile.LengthPrependedStringField(78)
    '''a recipient copied from email headers'''
    # bytes 79-141 not reverse-engieered
    subject = binfile.LengthPrependedStringField(142)
    '''the email subject copied from email headers'''
