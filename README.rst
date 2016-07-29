EULcommon
=========

EULcommon is a `Python <http://www.python.org/>`_ module with a few
small utilities that might be useful to others, but were not large or
significant enough to warrant splitting out into their own
repositories at this time.  These components may be broken out at a
later date.

**eulcommon.binfile** provides the capability to map arbitrary binary
data into a read-only python object.

**eulcommon.djangoextras** consists of a small number of extensions
and add-ons for use with `Django <https://www.djangoproject.com/>`_,
such as custom auth decorators, additional form fields, and additional
HTTP responses.


Contact Information
-------------------

**eulcommon** was created by the Digital Programs and Systems Software
Team of `Emory University Libraries <http://web.library.emory.edu/>`_.

libsysdev-l@listserv.cc.emory.edu


License
-------
**eulcommon** is distributed under the Apache 2.0 License.


Developer Notes
---------------

To install dependencies for your local check out of the code, run ``pip install``
in the ``eulcommon`` directory (the use of `virtualenv`_ is recommended)::

    pip install -e .

.. _virtualenv: http://www.virtualenv.org/en/latest/

If you want to run unit tests or build sphinx documentation, you should also
install development dependencies::

    pip install -e . "eulfedora[dev]"

Unit Tests
^^^^^^^^^^

Unit tests can be run with ``py.test``, and include options for
generating xml and coverage reports for continuous integration::

    py.test --junitxml=unittests.xml --cov=eulcommon

Development History
-------------------

For instructions on how to see and interact with the full development
history of **eulcommon**, see
`eulcore-history <https://github.com/emory-libraries/eulcore-history>`_.
