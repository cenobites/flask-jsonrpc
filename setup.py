#!/usr/bin/env python
# Copyright (c) 2012-2024, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# * Neither the name of the Cenobit Technologies nor the names of
#    its contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import os
import sys
import pathlib

import setuptools

setup_attrs = {}

if 'bdist_wheel' in sys.argv and os.environ.get('MYPYC_ENABLE', 'False').lower() in ('true', 't', '1'):
    from mypyc.build import mypycify  # pylint: disable=E0611

    project_dir = pathlib.Path(__file__).resolve().parent
    ext_modules = [
        '--config-file',
        str(project_dir / 'pyproject.toml'),
        '--strict',
        '--check-untyped-defs',
        '--ignore-missing-imports',
        '--disable-error-code',
        'unused-ignore',
        '--disable-error-code',
        'no-any-return',
        '--disable-error-code',
        'misc',
    ]
    ext_modules.extend([str(file) for file in (project_dir / 'src' / 'flask_jsonrpc').rglob('*.py')])
    setup_attrs['ext_modules'] = mypycify(ext_modules)
    setup_attrs['package_data'] = {'flask_jsonrpc.contrib.browse': ['static*', 'templates*']}

setuptools.setup(**setup_attrs)
