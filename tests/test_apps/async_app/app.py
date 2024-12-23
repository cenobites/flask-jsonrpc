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
import typing as t
import asyncio
import functools

from flask import Flask, jsonify

from flask_jsonrpc import JSONRPC

if t.TYPE_CHECKING:
    from flask import Response


def async_jsonrpc_decorator(fn: t.Callable[..., t.Awaitable[str]]) -> t.Callable[..., t.Awaitable[str]]:
    async def decorator(string: str) -> str:
        await asyncio.sleep(0)
        rv = await fn(string)
        return f'{rv} from decorator, ;)'

    return decorator


def async_jsonrpc_decorator_wrapped(fn: t.Callable[..., t.Awaitable[str]]) -> t.Callable[..., t.Awaitable[str]]:
    @functools.wraps(fn)
    async def decorator(string: str) -> str:
        await asyncio.sleep(0)
        rv = await fn(string)
        return f'{rv} from decorator, ;)'

    return decorator


class MyException(Exception):
    pass


class MyNotRegisteredException(Exception):
    pass


def create_app(test_config: t.Optional[dict[str, t.Any]] = None) -> Flask:  # noqa: C901
    """Create and configure an instance of the Flask application."""
    flask_app = Flask('apptest', instance_relative_config=True)
    if test_config:
        flask_app.config.update(test_config)

    jsonrpc = JSONRPC(flask_app, '/api', enable_web_browsable_api=True)

    @jsonrpc.errorhandler(MyException)
    async def handle_my_exception(ex: MyException) -> dict[str, t.Any]:
        await asyncio.sleep(0)
        return {'message': 'It is a custom exception', 'code': '0001'}

    @jsonrpc.method('jsonrpc.greeting')
    async def greeting(name: str = 'Flask JSON-RPC') -> str:
        await asyncio.sleep(0)
        return f'Hello {name}'

    @jsonrpc.method('jsonrpc.echo')
    async def echo(string: str, _some: t.Any = None) -> str:  # noqa: ANN401
        await asyncio.sleep(0)
        return string

    @jsonrpc.method('jsonrpc.notify')
    async def notify(_string: t.Optional[str] = None) -> None:
        await asyncio.sleep(0)

    @jsonrpc.method('jsonrpc.fails')
    async def fails(n: int) -> int:
        await asyncio.sleep(0)
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')

    @jsonrpc.method('jsonrpc.decorators')
    @async_jsonrpc_decorator
    async def decorators(string: str) -> str:
        await asyncio.sleep(0)
        return f'Hello {string}'

    @jsonrpc.method('jsonrpc.wrappedDecorators')
    @async_jsonrpc_decorator_wrapped
    async def wrapped_decorators(string: str) -> str:
        await asyncio.sleep(0)
        return f'Hello {string}'

    @jsonrpc.method('jsonrpc.failsWithCustomException')
    async def fails_with_custom_exception(_string: t.Optional[str] = None) -> t.NoReturn:
        await asyncio.sleep(0)
        raise MyException('example of fail with custom exception that will be handled')

    @jsonrpc.method('jsonrpc.failsWithCustomExceptionNotRegistered')
    async def fails_with_custom_exception_not_registered(_string: t.Optional[str] = None) -> t.NoReturn:
        await asyncio.sleep(0)
        raise MyNotRegisteredException('example of fail with custom exception that will not be handled')

    @flask_app.route('/health')
    async def health() -> 'Response':
        return jsonify({'status': 'UP'})

    return flask_app


if __name__ == '__main__':
    app = create_app({'SERVER_NAME': os.getenv('FLASK_SERVER_NAME')})
    app.run(host='0.0.0.0')
