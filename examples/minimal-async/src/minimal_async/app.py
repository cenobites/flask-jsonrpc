# Copyright (c) 2021-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
import typing as t
import asyncio

from flask import Flask, request

from flask_jsonrpc import JSONRPC

app = Flask('minimal-async')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


def check_terminal_id(fn: t.Callable[..., t.Any]) -> t.Any:  # noqa: ANN401
    async def wrapped() -> t.Any:  # noqa: ANN401
        await asyncio.sleep(0)
        terminal_id = int(request.get_json(silent=True).get('terminal_id', 0))
        if terminal_id < 0:
            raise ValueError('Invalid terminal ID')
        rv = await fn()
        return rv

    return wrapped


def jsonrpc_headers(fn: t.Callable[..., t.Any]) -> t.Any:  # noqa: ANN401
    async def wrapped() -> t.Any:  # noqa: ANN401
        await asyncio.sleep(0)
        headers = {'X-JSONRPC-Tag': 'JSONRPC 2.0'}
        rv = await fn()
        return rv, 200, headers

    return wrapped


class MyException(Exception):
    pass


@jsonrpc.errorhandler(MyException)
async def handle_my_exception(ex: MyException) -> dict[str, t.Any]:
    await asyncio.sleep(0)
    return {'message': 'It is a custom exception', 'code': '0001'}


@jsonrpc.method('App.index')
async def index() -> str:
    await asyncio.sleep(0)
    return 'Welcome to Flask JSON-RPC'


@jsonrpc.method('App.greeting')
async def greeting(name: str) -> str:
    await asyncio.sleep(0)
    return f'Hello {name}'


@jsonrpc.method('App.helloDefaultArgs')
async def hello_default_args(string: str = 'Flask JSON-RPC') -> str:
    await asyncio.sleep(0)
    return f'We salute you {string}'


@jsonrpc.method('App.argsValidate')
async def args_validate(a1: int, a2: str, a3: bool, a4: list[t.Any], a5: dict[t.Any, t.Any]) -> str:
    await asyncio.sleep(0)
    return f'Number: {a1}, String: {a2}, Boolean: {a3}, Array: {a4}, Object: {a5}'


@jsonrpc.method('App.notify')
async def notify(_string: str | None = None) -> None:
    await asyncio.sleep(0)


@jsonrpc.method('App.notNotify', notification=False)
async def not_notify(string: str) -> str:
    await asyncio.sleep(0)
    return f'Not allow notification: {string}'


@jsonrpc.method('App.fails')
async def fails(_string: str | None = None) -> t.NoReturn:
    await asyncio.sleep(0)
    raise ValueError('example of fail')


@jsonrpc.method('App.failsWithCustomException')
async def fails_with_custom_exception(_string: str | None = None) -> t.NoReturn:
    await asyncio.sleep(0)
    raise MyException('example of fail with custom exception that will be handled')


@jsonrpc.method('App.sum')
async def sum_(a: float, b: float) -> float:
    await asyncio.sleep(0)
    return a + b


@jsonrpc.method('App.subtract')
async def subtract(a: float, b: float) -> float:
    await asyncio.sleep(0)
    return a - b


@jsonrpc.method('App.multiply')
async def multiply(a: float, b: float) -> float:
    await asyncio.sleep(0)
    return a * b


@jsonrpc.method('App.divide')
async def divide(a: float, b: float) -> float:
    await asyncio.sleep(0)
    return a / float(b)


@jsonrpc.method('App.oneDecorator')
@check_terminal_id
async def one_decorator() -> str:
    await asyncio.sleep(0)
    terminal_id = request.get_json(silent=True).get('terminal_id', 0)
    return f'Terminal ID: {terminal_id}'


@jsonrpc.method('App.multiDecorators')
@check_terminal_id
@jsonrpc_headers
async def multi_decorators() -> dict[str, t.Any]:
    await asyncio.sleep(0)
    return {'terminal_id': request.get_json(silent=True).get('terminal_id', 0), 'headers': dict(request.headers)}
