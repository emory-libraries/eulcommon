:mod:`eulcore.binfile` -- Map binary data to Python objects
===========================================================

.. automodule:: eulcommon.binfile.core
.. pull in core's __doc__, even though we're treating the symbols as if
   they're in eulcommon.binfile

.. module:: eulcommon.binfile

:class:`BinaryStructure` Subclasses
-----------------------------------

.. toctree::
   :maxdepth: 1

   Eudora index files <binfile/eudora>
   

General Usage
-------------

Suppose we have an 8-byte file whose binary data consists of the bytes 0, 1,
2, 3, etc.::

   >>> with open('numbers.bin') as f:
   ...     f.read()
   ... 
   '\x00\x01\x02\x03\x04\x05\x06\x07'

Suppose further that these contents represent sensible binary data, laid out
such that the first two bytes are a literal string value. Except that
sometimes, in the binary format we're parsing, it might sometimes be
necessary to interpret those first two bytes not as a literal string, but
instead as a number, encoded as a `big-endian
<http://en.wikipedia.org/wiki/Endianness>`_ unsigned integer. Following that
is a variable-length string, encoded with the total string length in the
third byte.

This structure might be represented as::

   from eulcommon.binfile import *
   class MyObject(BinaryStructure):
       mybytes = ByteField(0, 2)
       myint = IntegerField(0, 2)
       mystring = LengthPrepededStringField(2)

Client code might then read data from that file::

   >>> f = open('numbers.bin')
   >>> obj = MyObject(f)
   >>> obj.mybytes
   '\x00\x01'
   >>> obj.myint
   1
   >>> obj.mystring
   '\x03\x04'

It's not uncommon for such binary structures to be repeated at different
points within a file. Consider if we overlay the same structure on the same
file, but starting at byte 1 instead of byte 0::

   >>> f = open('numbers.bin')
   >>> obj = MyObject(f, offset=1)
   >>> obj.mybytes
   '\x01\x02'
   >>> obj.myint
   258
   >>> obj.mystring
   '\x04\x05\x06'

:class:`BinaryStructure`
------------------------

.. autoclass:: BinaryStructure


Field classes
-------------

.. autoclass:: ByteField

.. autoclass:: LengthPrependedStringField

.. autoclass:: IntegerField
