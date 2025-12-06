#!/usr/bin/env python
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
import asyncio
import functools

from flask import Flask, jsonify

from shared.features.class_apps import jsonrpc as jsonrpc_class_apps_app
from shared.features.decorators import jsonrpc as jsonrpc_decorators_app
from shared.features.jsonrpc_basic import jsonrpc as jsonrpc_jsonrpc_basic_app
from shared.features.error_handlers import jsonrpc as jsonrpc_error_handlers_app
from shared.features.types.python_stds import jsonrpc as jsonrpc_types_python_std_app
from shared.features.objects.python_classes import jsonrpc as jsonrpc_objects_python_classes_app
from shared.features.objects.pydantic_models import jsonrpc as jsonrpc_objects_pydantic_models_app
from shared.features.objects.python_dataclasses import jsonrpc as jsonrpc_objects_python_dataclasses_app
from shared.features.types.python_stds_annotated import jsonrpc as jsonrpc_types_python_annotated_stds_app
from shared.features.types.python_classes_annotated import jsonrpc as jsonrpc_objects_python_classes_annotated_app
from shared.features.types.pydantic_models_annotated import jsonrpc as jsonrpc_objects_pydantic_models_annotated_app
from shared.features.types.python_dataclasses_annotated import (
    jsonrpc as jsonrpc_objects_python_dataclasses_annotated_app,
)

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


class MyExceptionWithCustomStatusCode(Exception):
    status_code = 409


class MyNotRegisteredException(Exception):
    pass


def create_app(test_config: dict[str, t.Any] | None = None) -> Flask:  # noqa: C901
    """Create and configure an instance of the Flask application."""
    flask_app = Flask('apptest', instance_relative_config=True)
    if test_config:
        flask_app.config.update(test_config)

    jsonrpc = JSONRPC(flask_app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(
        flask_app, jsonrpc_jsonrpc_basic_app, url_prefix='/jsonrpc-basic', enable_web_browsable_api=True
    )
    jsonrpc.register_blueprint(
        flask_app, jsonrpc_class_apps_app, url_prefix='/class-apps', enable_web_browsable_api=True
    )
    jsonrpc.register_blueprint(
        flask_app, jsonrpc_decorators_app, url_prefix='/decorators', enable_web_browsable_api=True
    )
    jsonrpc.register_blueprint(
        flask_app, jsonrpc_error_handlers_app, url_prefix='/error-handlers', enable_web_browsable_api=True
    )
    jsonrpc.register_blueprint(
        flask_app, jsonrpc_types_python_std_app, url_prefix='/types/python-stds', enable_web_browsable_api=True
    )
    jsonrpc.register_blueprint(
        flask_app,
        jsonrpc_types_python_annotated_stds_app,
        url_prefix='/types/python-stds-annotated',
        enable_web_browsable_api=True,
    )
    jsonrpc.register_blueprint(
        flask_app,
        jsonrpc_objects_python_classes_annotated_app,
        url_prefix='/types/python-classes-annotated',
        enable_web_browsable_api=True,
    )
    jsonrpc.register_blueprint(
        flask_app,
        jsonrpc_objects_python_dataclasses_annotated_app,
        url_prefix='/types/python-dataclasses-annotated',
        enable_web_browsable_api=True,
    )
    jsonrpc.register_blueprint(
        flask_app,
        jsonrpc_objects_pydantic_models_annotated_app,
        url_prefix='/types/pydantic-models-annotated',
        enable_web_browsable_api=True,
    )
    jsonrpc.register_blueprint(
        flask_app,
        jsonrpc_objects_python_classes_app,
        url_prefix='/objects/python-classes',
        enable_web_browsable_api=True,
    )
    jsonrpc.register_blueprint(
        flask_app,
        jsonrpc_objects_python_dataclasses_app,
        url_prefix='/objects/python-dataclasses',
        enable_web_browsable_api=True,
    )
    jsonrpc.register_blueprint(
        flask_app,
        jsonrpc_objects_pydantic_models_app,
        url_prefix='/objects/pydantic-models',
        enable_web_browsable_api=True,
    )

    jsonrpc.errorhandler(ValueError)

    async def handle_value_error_exception(ex: ValueError) -> dict[str, t.Any]:
        await asyncio.sleep(0)
        return {'message': 'Generic global error handler does not work, :(', 'code': '0000'}

    @jsonrpc.errorhandler(MyException)
    async def handle_my_exception(ex: MyException) -> dict[str, t.Any]:
        await asyncio.sleep(0)
        return {'message': 'It is a custom exception', 'code': '0001'}

    @jsonrpc.errorhandler(MyExceptionWithCustomStatusCode)
    async def handle_my_exception_with_custom_status_code(
        ex: MyExceptionWithCustomStatusCode,
    ) -> tuple[dict[str, t.Any], int]:
        await asyncio.sleep(0)
        return {'message': 'It is a custom exception with status code', 'code': '0001'}, ex.status_code

    @jsonrpc.method('app.greeting')
    async def greeting(name: str = 'Flask JSON-RPC') -> str:
        await asyncio.sleep(0)
        return f'Hello {name}'

    @jsonrpc.method('app.echo')
    async def echo(string: str, _some: t.Any = None) -> str:  # noqa: ANN401
        await asyncio.sleep(0)
        return string

    @jsonrpc.method('app.notify')
    async def notify(_string: str | None = None) -> None:
        await asyncio.sleep(0)

    @jsonrpc.method('app.fails')
    async def fails(n: int) -> int:
        await asyncio.sleep(0)
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')

    @jsonrpc.method('app.decorators')
    @async_jsonrpc_decorator
    async def decorators(string: str) -> str:
        await asyncio.sleep(0)
        return f'Hello {string}'

    @jsonrpc.method('app.wrappedDecorators')
    @async_jsonrpc_decorator_wrapped
    async def wrapped_decorators(string: str) -> str:
        await asyncio.sleep(0)
        return f'Hello {string}'

    @jsonrpc.method('app.failsWithCustomException')
    async def fails_with_custom_exception(_string: str | None = None) -> t.NoReturn:
        await asyncio.sleep(0)
        raise MyException('example of fail with custom exception that will be handled')

    @jsonrpc.method('app.failsWithCustomExceptionWithStatusCode')
    async def fails_with_custom_exception_with_status_code(_string: str | None = None) -> t.NoReturn:
        await asyncio.sleep(0)
        raise MyExceptionWithCustomStatusCode(
            'example of fail with custom exception with status code that will be handled'
        )

    @jsonrpc.method('app.failsWithCustomExceptionNotRegistered')
    async def fails_with_custom_exception_not_registered(_string: str | None = None) -> t.NoReturn:
        await asyncio.sleep(0)
        raise MyNotRegisteredException('example of fail with custom exception that will not be handled')

    @flask_app.route('/health')
    async def health() -> 'Response':
        return jsonify({'status': 'UP'})

    return flask_app
