#!/usr/bin/env python
from collections import defaultdict
import os
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

package_data = defaultdict(list)
for path, dirs, files in os.walk('eulcommon'):
    templates_idx = path.find('templates')
    if templates_idx != -1:
        package_path = path[:templates_idx].rstrip('/')
        relative_path = path[templates_idx:]
        targetfiles = [os.path.join(relative_path, f) for f in files]
        package = package_path.replace('/', '.')
        package_data[package].extend(targetfiles)

test_requirements = [
    'mock',
    'ply',
    'pytest',
    'pytest-cov',
    'pytest-django',
    'django-celery',
]

dev_requirements = test_requirements + ['django<1.9', 'sphinx']

setup(
    name='eulcommon',
    version=__version__,
    author='Emory University Libraries',
    author_email='libsysdev-l@listserv.cc.emory.edu',
    url='https://github.com/emory-libraries/eulcommon',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    package_data=package_data,
    install_requires=[
        'mimeparse',
        'python-magic',
        'celery',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'django', 'mock'],
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements
    },
    description='A collection of small python utilities for working with binary files and Django',
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    keywords='Binary data',
)
