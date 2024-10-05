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
from typing import NoReturn, Optional

from flask import Flask

from flask_jsonrpc import JSONRPC

app = Flask('wba')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('App.index')
def index() -> str:
    return 'Welcome to Flask JSON-RPC'


@jsonrpc.method('App.hello')
def hello(name: str) -> str:
    return f'Hello {name}'


@jsonrpc.method('App.helloDefaultArgs')
def hello_default_args(string: str = 'Flask JSON-RPC') -> str:
    return f'We salute you {string}'


@jsonrpc.method('App.helloDefaultArgsValidate')
def hello_default_args_validate(string: str = 'Flask JSON-RPC') -> str:
    return f'We salute you {string}'


@jsonrpc.method('App.args')
def args_validate_python_mode(a1: int, a2: str, a3: bool, a4: list, a5: dict) -> str:
    return f'int: {a1}, str: {a2}, bool: {a3}, list: {a4}, dict: {a5}'


@jsonrpc.method('App.notify')
def notify(_string: Optional[str]) -> None:
    pass


@jsonrpc.method('App.fails')
def fails(_string: Optional[str]) -> NoReturn:
    raise ValueError('example of fail')


@jsonrpc.method('App.notValidate', validate=False)
def not_validate(s='Oops!'):  # noqa: ANN001,ANN202,ANN201
    return f'Not validate: {s}'


@jsonrpc.method('App.mixinNotValidate', validate=False)
def mixin_not_validate(s, t: int, u, v: str, x, z):  # noqa: ANN001,ANN202,ANN201
    return f'Not validate: {s} {t} {u} {v} {x} {z}'


@jsonrpc.method('App.mixinNotValidateReturn', validate=False)
def mixin_not_validate_with_no_return(_s, _t: int, _u, _v: str, _x, _z):  # noqa: ANN001,ANN202,ANN201
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
