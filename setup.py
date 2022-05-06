#!/usr/bin/env python
# Copyright (c) 2012-2022, Cenobit Technologies, Inc. http://cenobit.es/
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
import setuptools

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setuptools.setup(
    name='Flask-JSONRPC',
    install_requires=[
        'Flask>=1.0.0,<3.0',
        'typeguard==2.13.3',
        'typing>=3.7.4;python_version<"3.5"',
        'typing_extensions>=3.7.4;python_version>="3.6"',
        'typing_extensions>=3.7.4,<3.10;python_version<"3.6"',
        'typing_inspect==0.7.1',
    ],
    extras_require={
        'async': ['Flask[async]>=1.0.0,<3.0'],
        'dotenv': ['Flask[dotenv]>=1.0.0,<3.0'],
    },
    setup_requires=['pytest-runner'],
    tests_require=[
        'mock==4.0.3',
        'coverage==6.3.2;python_version>"3.6"',
        'coverage<6.2;python_version<="3.6"',
        'pytest==7.1.2;python_version>"3.6"',
        'pytest<7;python_version<="3.6"',
        'pytest-cov==3.0.0',
        'pytest-xdist==2.5.0',
        'pytest-sugar==0.9.4',
        'pytest-env==0.6.2',
        'typeguard==2.13.3',
    ],
)
