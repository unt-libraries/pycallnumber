#! /usr/bin/env python

import os
import setuptools


name = 'pycallnumber'
url = 'https://github.com/unt-libraries/pycallnumber'
description = 'A Python library for parsing call numbers.'
package_metadata = {}
with open(os.path.join(name, '__init__.py')) as fh:
    variables = [l.split(' = ') for l in fh if l.startswith('__')]
    for var in variables:
        package_metadata[var[0].strip('_')] = var[-1].strip('"\'\n')

setuptools.setup(
    name=name,
    author=package_metadata['author'],
    author_email='jason.thomale@unt.edu',
    version=package_metadata['version'],
    url=url,
    license='BSD',
    description=description,
    long_description=('Visit {} for the latest documentation.'.format(url)),
    packages=setuptools.find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Intended Audience :: Education',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
