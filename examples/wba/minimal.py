#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012-2020, Cenobit Technologies, Inc. http://cenobit.es/
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
# isort:skip_file
import os
import sys
from typing import NoReturn, Optional

from flask import Flask

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(os.path.dirname(os.path.realpath(__file__)))

FLASK_JSONRPC_PROJECT_DIR = os.path.join(PROJECT_DIR, os.pardir)
if os.path.exists(FLASK_JSONRPC_PROJECT_DIR) and FLASK_JSONRPC_PROJECT_DIR not in sys.path:
    sys.path.append(FLASK_JSONRPC_PROJECT_DIR)

from flask_jsonrpc import JSONRPC  # noqa: E402   pylint: disable=C0413

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('App.index')
def index() -> str:
    return 'Welcome to Flask JSON-RPC'


@jsonrpc.method('App.hello')
def hello(name: str) -> str:
    return 'Hello {0}'.format(name)


@jsonrpc.method('App.helloDefaultArgs')
def hello_default_args(string: str = 'Flask JSON-RPC') -> str:
    return 'We salute you {0}'.format(string)


@jsonrpc.method('App.helloDefaultArgsValidate')
def hello_default_args_validate(string: str = 'Flask JSON-RPC') -> str:
    return 'We salute you {0}'.format(string)


@jsonrpc.method('App.args')
def args_validate_python_mode(a1: int, a2: str, a3: bool, a4: list, a5: dict) -> str:
    return 'int: {0}, str: {1}, bool: {2}, list: {3}, dict: {4}'.format(a1, a2, a3, a4, a5)


@jsonrpc.method('App.notify')
def notify(_string: Optional[str]) -> None:
    pass


@jsonrpc.method('App.fails')
def fails(string: Optional[str]) -> NoReturn:
    raise ValueError('example of fail')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
