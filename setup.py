#!/usr/bin/env python
from setuptools import setup, find_packages

from eulcommon import __version__

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
]

LONG_DESCRIPTION = None
try:
    # read the description if it's there
    with open('README.rst') as desc_f:
        LONG_DESCRIPTION = desc_f.read()
except:
    pass


setup(
    name='eulcommon',
    version=__version__,
    author='Emory University Libraries',
    author_email='libsysdev-l@listserv.cc.emory.edu',
    url='https://github.com/emory-libraries/eulcommon',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    install_requires=[
        'mimeparse',
    ],
    description='A collection of small python utilities for working with binary files and Django',
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    keywords='Binary data'
)
