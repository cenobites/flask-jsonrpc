#!/usr/bin/env python
# Copyright (c) 2021-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
import asyncio

from flask import Flask

from flask_jsonrpc import JSONRPC

app = Flask('wba')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('App.index')
async def index() -> str:
    await asyncio.sleep(0)
    return 'Welcome to Flask JSON-RPC'


@jsonrpc.method('App.hello')
async def hello(name: str) -> str:
    await asyncio.sleep(0)
    return f'Hello {name}'


@jsonrpc.method('App.helloDefaultArgs')
async def hello_default_args(string: str = 'Flask JSON-RPC') -> str:
    await asyncio.sleep(0)
    return f'We salute you {string}'


@jsonrpc.method('App.helloDefaultArgsValidate')
async def hello_default_args_validate(string: str = 'Flask JSON-RPC') -> str:
    await asyncio.sleep(0)
    return f'We salute you {string}'


@jsonrpc.method('App.args')
async def args_validate_python_mode(a1: int, a2: str, a3: bool, a4: list, a5: dict) -> str:
    await asyncio.sleep(0)
    return f'int: {a1}, str: {a2}, bool: {a3}, list: {a4}, dict: {a5}'


@jsonrpc.method('App.notify')
async def notify(_string: Optional[str]) -> None:
    await asyncio.sleep(0)


@jsonrpc.method('App.fails')
async def fails(_string: Optional[str]) -> NoReturn:
    await asyncio.sleep(0)
    raise ValueError('example of fail')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
