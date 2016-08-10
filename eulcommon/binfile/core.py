# file eulcommon/binfile/core.py
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

'''Map binary data on-disk to read-only Python objects.

This module facilitates exposing stored binary data using common Pythonic
idioms. Fields in relocatable binary objects map to Python attributes using
a priori knowledge about how the binary structure is organized. This is akin
to the standard :mod:`struct` module, but with some slightly different use
cases. :mod:`struct`, for instance, offers a more terse syntax, which is
handy for certain simple structures. :mod:`struct` is also a bit faster
since it's implemented in C. This module's more verbose
:class:`~eulcommon.binfile.BinaryStructure` definitions give it a few
advantages over :mod:`struct`, though:

 * This module allows users to define their own field types, where
   :mod:`struct` field types are basically inextensible.
 * The object-based nature of :class:`~eulcommon.binfile.BinaryStructure`
   makes it easy to add non-structural properties and methods to subclasses,
   which would require a bit of reimplementing and wrapping from a
   :mod:`struct` tuple.
 * :class:`~eulcommon.binfile.BinaryStructure` instances access fields through
   named properties instead of indexed tuples. :mod:`struct` tuples are fine
   for structures a few fields long, but when a packed binary structure
   grows to dozens of fields, navigating its :mod:`struct` tuple grows
   perilous.
 * :class:`~eulcommon.binfile.BinaryStructure` unpacks fields only when
   they're accessed, allowing us to define libraries of structures scores of
   fields long, understanding that any particular application might access
   only one or two of them.
 * Fields in a :class:`~eulcommon.binfile.BinaryStructure` can overlap
   eachother, greatly simplifying both C `unions
   <http://en.wikipedia.org/wiki/Union_(computer_science)>`_ and fields with
   multiple interpretations (integer/string, signed/unsigned).
 * This module makes sparse structures easy. If you're reverse-engineering a
   large binary structure and discover a 4-byte integer in the middle of 68
   bytes of unidentified mess, this module makes it easy to add an
   :class:`~eulcommon.binfile.IntegerField` at a known structure offset.
   :mod:`struct` requires you to split your ``'68x'`` into a ``'32xI32x'``
   (or was that a ``'30xi34x'``? Better recount.)

This package exports the following names:
 * :class:`~eulcommon.binfile.BinaryStructure` -- a base class for binary data
   structures
 * :class:`~eulcommon.binfile.ByteField` -- a field that maps fixed-length
   binary data to Python strings
 * :class:`~eulcommon.binfile.LengthPrependedStringField` -- a field that maps
   variable-length binary strings to Python strings
 * :class:`~eulcommon.binfile.IntegerField` -- a field that maps fixed-length
   binary data to Python numbers
'''
# see eulcommon/binfile/__init__.py for more docs

from mmap import mmap

__all__ = [ 'BinaryStructure', 'ByteField', 'LengthPrependedStringField',
            'IntegerField' ]

class BinaryStructure(object):
    """A superclass for binary data structures superimposed over files.

    Typical users will create a subclass containing field objects (e.g.,
    :class:`ByteField`, :class:`IntegerField`). Each subclass instance is
    created with a file and with an optional offset into that file. When
    code accesses fields on the instance, they are calculated from the
    underlying binary file data.

    Instead of a file, it is occasionally appropriate to overlay an
    :class:`~mmap.mmap` structure (from the :mod:`mmap` standard library).
    This happens most often when one ``BinaryStructure`` instance creates
    another, passing ``self.mmap`` to the secondary object's constructor. In
    this case, the caller may specify the `mm` argument instead of an
    `fobj`.

    :param fobj: a file object or filename to overlay
    :param mm: a :class:`~mmap.mmap` object to overlay
    :param offset: the offset into the file where the structured data begins
    """

    def __init__(self, fobj=None, mm=None, offset=0):
        if mm is not None:
            self.mmap = mm
        else:
            if isinstance(fobj, str):
                fobj = open(fobj)
            self.mmap = mmap(fobj.fileno(), 0, prot=1) # read-only for now
        self._offset = offset


class ByteField(object):
    """A field mapping fixed-length binary data to Python strings.

    :param start: The offset into the structure of the beginning of the
      byte data.
    :param end: The offset into the structure of the end of the byte data.
      This is actually one past the last byte of data, so a four-byte
      ``ByteField`` starting at index 4 would be defined as
      ``ByteField(4, 8)`` and would include bytes 4, 5, 6, and 7 of the
      binary structure.

    Typical users will create a `ByteField` inside a :class:`BinaryStructure`
    subclass definition::

        class MyObject(BinaryStructure):
            myfield = ByteField(0, 4) # the first 4 bytes of the file

    When you instantiate the subclass and access the field, its value will
    be the literal bytes at that location in the structure::

        >>> o = MyObject('file.bin')
        >>> o.myfield
        'ABCD'
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __get__(self, obj, owner):
        if obj is None:
            return self

        return obj.mmap[self.start + obj._offset : self.end + obj._offset]


class LengthPrependedStringField(object):
    """A field mapping variable-length binary strings to Python strings.

    This field accesses strings encoded with their length in their first
    byte and string data following that byte.

    :param offset: The offset of the single-byte string length.

    Typical users will create a ``LengthPrependedStringField`` inside a
    :class:`BinaryStructure` subclass definition::

        class MyObject(BinaryStructure):
            myfield = LengthPrependedStringField(0)

    When you instantiate the subclass and access the field, its length will
    be read from that location in the structure, and its data will be the
    bytes immediately following it. So with a file whose first bytes are
    ``'\\x04ABCD'``::

        >>> o = MyObject('file.bin')
        >>> o.myfield
        'ABCD'
    """

    def __init__(self, offset):
        self.offset = offset

    def __get__(self, obj, owner):
        if obj is None:
            return self

        length_offset = self.offset + obj._offset
        length = ord(obj.mmap[length_offset])
        data_offset = length_offset + 1
        return obj.mmap[data_offset:data_offset + length]


class IntegerField(ByteField):
    """A field mapping fixed-length binary data to Python numbers.

    This field accessses arbitrary-length integers encoded as binary data.
    Currently only `big-endian <http://en.wikipedia.org/wiki/Endianness>`_,
    unsigned integers are supported.

    :param start: The offset into the structure of the beginning of the
      byte data.
    :param end: The offset into the structure of the end of the byte data.
      This is actually one past the last byte of data, so a four-byte
      ``IntegerField`` starting at index 4 would be defined as
      ``IntegerField(4, 8)`` and would include bytes 4, 5, 6, and 7 of the
      binary structure.

    Typical users will create an `IntegerField` inside a
    :class:`BinaryStructure` subclass definition::

        class MyObject(BinaryStructure):
            myfield = IntegerField(3, 6) # integer encoded in bytes 3, 4, 5

    When you instantiate the subclass and access the field, its value will
    be big-endian unsigned integer encoded at that location in the
    structure. So with a file whose bytes 3, 4, and 5 are
    ``'\\x00\\x01\\x04'``::

        >>> o = MyObject('file.bin')
        >>> o.myfield
        260
    """
    def __get__(self, obj, owner):
        if obj is None:
            return self

        # Conveniently, ByteField already supports arbitrary fixed-length
        # strings. Draw on our ByteField parent to get the bytes underlying
        # this number field, and then interpret those bytes as a number.

        byte_data = ByteField.__get__(self, obj, owner)
        val = 0
        # we only support big-endian for now. big-endian integers are sort
        # of like base-256 numbers. in base 10 to get from 432 to 4326 we
        # multiply by 10 and add 6. so in base 256 we multiply by 256 and
        # add our next byte.
        for byte in byte_data:
            val *= 256
            val += ord(byte)
        return val
