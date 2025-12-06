# Copyright (c) 2012-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

from flask import Flask, request

from flask_jsonrpc import JSONRPC

app = Flask('minimal')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


def check_terminal_id(fn: t.Callable[..., t.Any]) -> t.Any:  # noqa: ANN401
    def wrapped() -> t.Any:  # noqa: ANN401
        terminal_id = int(request.get_json(silent=True).get('terminal_id', 0))
        if terminal_id < 0:
            raise ValueError('Invalid terminal ID')
        rv = fn()
        return rv

    return wrapped


def jsonrpc_headers(fn: t.Callable[..., t.Any]) -> t.Any:  # noqa: ANN401
    def wrapped() -> t.Any:  # noqa: ANN401
        headers = {'X-JSONRPC-Tag': 'JSONRPC 2.0'}
        rv = fn()
        return rv, 200, headers

    return wrapped


class MyException(Exception):
    pass


class MyExceptionWithCustomStatusCode(Exception):
    status_code = 409


@jsonrpc.errorhandler(MyException)
def handle_my_exception(ex: MyException) -> dict[str, t.Any]:
    return {'message': 'It is a custom exception', 'code': '0001'}


@jsonrpc.errorhandler(MyExceptionWithCustomStatusCode)
def handle_my_exception_with_custom_status_code(ex: MyExceptionWithCustomStatusCode) -> tuple[dict[str, t.Any], int]:
    return {'message': 'It is a custom exception with status code', 'code': '0001'}, ex.status_code


@jsonrpc.method('App.index')
def index() -> str:
    return 'Welcome to Flask JSON-RPC'


@jsonrpc.method('App.greeting')
def greeting(name: str) -> str:
    return f'Hello {name}'


@jsonrpc.method('App.helloDefaultArgs')
def hello_default_args(string: str = 'Flask JSON-RPC') -> str:
    return f'We salute you {string}'


@jsonrpc.method('App.argsValidate')
def args_validate(a1: int, a2: str, a3: bool, a4: list[t.Any], a5: dict[t.Any, t.Any]) -> str:
    return f'Number: {a1}, String: {a2}, Boolean: {a3}, Array: {a4}, Object: {a5}'


@jsonrpc.method('App.notify')
def notify(_string: str | None = None) -> None:
    pass


@jsonrpc.method('App.notNotify', notification=False)
def not_notify(string: str) -> str:
    return f'Not allow notification: {string}'


@jsonrpc.method('App.fails')
def fails(_string: str | None = None) -> t.NoReturn:
    raise ValueError('example of fail')


@jsonrpc.method('App.failsWithCustomException')
def fails_with_custom_exception(_string: str | None = None) -> t.NoReturn:
    raise MyException('example of fail with custom exception that will be handled')


@jsonrpc.method('App.failsWithCustomExceptionWithStatusCode')
def fails_with_custom_exception_with_status_code(_string: str | None = None) -> t.NoReturn:
    raise MyExceptionWithCustomStatusCode('example of fail with custom exception with status code that will be handled')


@jsonrpc.method('App.sum')
def sum_(a: float, b: float) -> float:
    return a + b


@jsonrpc.method('App.subtract')
def subtract(a: float, b: float) -> float:
    return a - b


@jsonrpc.method('App.multiply')
def multiply(a: float, b: float) -> float:
    return a * b


@jsonrpc.method('App.divide')
def divide(a: float, b: float) -> float:
    return a / float(b)


@jsonrpc.method('App.oneDecorator')
@check_terminal_id
def one_decorator() -> str:
    terminal_id = request.get_json(silent=True).get('terminal_id', 0)
    return f'Terminal ID: {terminal_id}'


@jsonrpc.method('App.multiDecorators')
@check_terminal_id
@jsonrpc_headers
def multi_decorators() -> dict[str, t.Any]:
    return {'terminal_id': request.get_json(silent=True).get('terminal_id', 0), 'headers': dict(request.headers)}
