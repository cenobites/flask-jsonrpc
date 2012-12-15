#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
"""
Flask-JSONRPC
-----------

Adds JSONRPC support to Flask.

Links
`````

* `documentation <http://packages.python.org/Flask-JSONRPC>`_
* `development version <http://github.com/cenobites/flask-jsonrpc/zipball/master#egg=Flask-JSONRPC>`_
"""
from setuptools import setup

setup(
    name='Flask-JSONRPC',
    version='0.1',
    url='https://github.com/cenobites/flask-jsonrpc',
    license='New BSD License',
    author='Nycholas de Oliveira e Oliveira',
    author_email='nycholas@gmail.com',
    description='Adds JSONRPC support to Flask.',
    long_description=__doc__,
    packages=['flask_jsonrpc'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
