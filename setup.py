#! /usr/bin/env python

import os
import setuptools

meta = {}
with open(os.path.join('pycallnumber', '__init__.py')) as fh:
    variables = [l.split(' = ') for l in fh if l.startswith('__')]
    for var in variables:
        meta[var[0].strip('_')] = var[-1].strip('"\'\n')

setuptools.setup(
    name=meta['name'],
    author=meta['author'],
    author_email=meta['author_email'],
    version=meta['version'],
    url=meta['url'],
    license=meta['license'],
    description=meta['description'],
    long_description=('Visit {} for the latest documentation.'.format(
                       meta['url'])),
    maintainer=meta['maintainer'],
    keywords=meta['keywords'],
    packages=setuptools.find_packages(),
    install_requires=[
        'future;python_version=="2.7"'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    classifiers=[
        'Intended Audience :: Education',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
