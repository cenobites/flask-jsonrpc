# Copyright (c) 2020-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

from flask import Flask

import pytest

from flask_jsonrpc import JSONRPC, JSONRPCBlueprint

# Added in version 3.11.
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class CustomException(Exception):
    def __init__(self: Self, message: str, data: dict[str, t.Any]) -> None:
        super().__init__(message)
        self.message = message
        self.data = data


def test_jsonrpc_blueprint() -> None:
    jsonrpc_api_1 = JSONRPCBlueprint('jsonrpc_api_1', __name__)

    @jsonrpc_api_1.method('blue1.fn2')
    def fn1_b1(s: str) -> str:
        return f'b1: Foo {s}'

    def fn2_b1(s: str) -> str:
        return f'b2: Foo {s}'

    jsonrpc_api_1.register(fn1_b1, name='blue1.fn1')

    jsonrpc_api_2 = JSONRPCBlueprint('jsonrpc_api_2', __name__)

    @jsonrpc_api_2.method('blue2.fn2')
    def fn1_b2(s: str) -> str:
        return f'b2: Foo {s}'

    @jsonrpc_api_2.method('blue2.fn1')
    def fn2_b2(s: str) -> str:
        return f'b2: Bar {s}'

    jsonrpc_api_3 = JSONRPCBlueprint('jsonrpc_api_3', __name__)

    @jsonrpc_api_3.method('blue3.fn2')
    def fn1_b3(s: str) -> str:
        return f'b3: Foo {s}'

    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_1, url_prefix='/b1')
    jsonrpc.register_blueprint(app, jsonrpc_api_2, url_prefix='/b2')
    jsonrpc.register_blueprint(app, jsonrpc_api_3, url_prefix='/b3')

    with app.test_client() as client:
        rv = client.post('/api/b1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue1.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b1: Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api/b1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue1.fn1', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b1: Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api/b2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue2.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b2: Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api/b2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue2.fn1', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b2: Bar :)'}
        assert rv.status_code == 200

        rv = client.post('/api/b3', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue3.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b3: Foo :)'}
        assert rv.status_code == 200


def test_jsonrpc_blueprint_using_error_handler() -> None:  # noqa: C901
    jsonrpc_api_1 = JSONRPCBlueprint('jsonrpc_api_1', __name__)

    @jsonrpc_api_1.errorhandler(CustomException)
    def handle_custom_exc_jsonrpc_api_1(exc: CustomException) -> str:
        return f'jsonrpc_api_1: {exc.data["message"]}'

    @jsonrpc_api_1.errorhandler(ValueError)
    def handle_value_error_exc_jsonrpc_api_1(exc: ValueError) -> tuple[str, int]:
        return f'jsonrpc_api_1: {exc}', 409

    @jsonrpc_api_1.method('blue1.index')
    def index_b1() -> str:
        return 'b1 index'

    @jsonrpc_api_1.method('blue1.errorhandler')
    def error_b1() -> t.NoReturn:
        raise CustomException('Testing error handler', data={'message': 'Flask JSON-RPC', 'code': '0000'})

    @jsonrpc_api_1.method('blue1.errorhandlerWithStatusCode')
    def error_status_code_b1() -> t.NoReturn:
        raise ValueError('Testing error handler')

    jsonrpc_api_2 = JSONRPCBlueprint('jsonrpc_api_2', __name__)

    @jsonrpc_api_2.errorhandler(CustomException)
    def handle_custom_exc_jsonrpc_api_2(exc: CustomException) -> str:
        return f'jsonrpc_api_2: {exc.data["message"]}'

    @jsonrpc_api_2.errorhandler(ValueError)
    def handle_value_error_exc_jsonrpc_api_2(exc: ValueError) -> tuple[str, int]:
        return f'jsonrpc_api_2: {exc}', 400

    @jsonrpc_api_2.method('blue2.index')
    def index_b2() -> str:
        return 'b2 index'

    @jsonrpc_api_2.method('blue2.errorhandler')
    def error_b2() -> t.NoReturn:
        raise CustomException('Testing error handler', data={'message': 'Flask JSON-RPC', 'code': '0000'})

    @jsonrpc_api_2.method('blue2.errorhandlerWithStatusCode')
    def error_with_status_code_b2() -> t.NoReturn:
        raise ValueError('Testing error handler')

    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_1, url_prefix='/b1')
    jsonrpc.register_blueprint(app, jsonrpc_api_2, url_prefix='/b2')

    with app.test_client() as client:
        rv = client.post('/api/b1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue1.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b1 index'}
        assert rv.status_code == 200

        rv = client.post('/api/b1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue1.errorhandler', 'params': []})
        assert rv.json == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'data': 'jsonrpc_api_1: Flask JSON-RPC',
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert rv.status_code == 500

        rv = client.post(
            '/api/b1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue1.errorhandlerWithStatusCode', 'params': []}
        )
        assert rv.json == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'data': 'jsonrpc_api_1: Testing error handler',
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert rv.status_code == 409

        rv = client.post('/api/b2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue2.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b2 index'}
        assert rv.status_code == 200

        rv = client.post('/api/b2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue2.errorhandler', 'params': []})
        assert rv.json == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'data': 'jsonrpc_api_2: Flask JSON-RPC',
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert rv.status_code == 500

        rv = client.post(
            '/api/b2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue2.errorhandlerWithStatusCode', 'params': []}
        )
        assert rv.json == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'data': 'jsonrpc_api_2: Testing error handler',
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert rv.status_code == 400


def test_jsonrpc_blueprint_with_server_name() -> None:
    jsonrpc_api_1 = JSONRPCBlueprint('jsonrpc_api_1', __name__)

    @jsonrpc_api_1.method('blue1.fn2')
    def fn1_b1(s: str) -> str:
        return f'b1: Foo {s}'

    app = Flask('test_app', instance_relative_config=True)
    app.config.update({'SERVER_NAME': 'domain:80'})
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_1, url_prefix='/b1')

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

        rv = client.post('/api/b1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue1.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b1: Foo :)'}
        assert rv.status_code == 200


def test_jsonrpc_blueprint_with_method_without_annotation() -> None:
    jsonrpc_api_1 = JSONRPCBlueprint('jsonrpc_api_1', __name__)

    with pytest.raises(ValueError, match='no type annotations present to: blue1.fn2'):

        @jsonrpc_api_1.method('blue1.fn2')
        def fn1_b1(s):  # noqa: ANN001, ANN202
            return f'b1: Foo {s}'

    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'
