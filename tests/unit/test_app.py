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
import json
import uuid
import typing as t
import logging
from unittest import mock
from threading import Lock

from flask import Flask
from flask.logging import default_handler

import pytest
from werkzeug.datastructures import Headers

from flask_jsonrpc import JSONRPC

# Added in version 3.11.
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


logger_lock = Lock()


@pytest.fixture(autouse=True)
def reset_logging(pytestconfig: pytest.Config) -> t.Generator[None, None, None]:
    root_handlers = logging.root.handlers[:]
    logging.root.handlers = []
    root_level = logging.root.level

    flask_logger = logging.getLogger('test_app')
    flask_logger.handlers = []
    flask_logger.setLevel(logging.NOTSET)

    logger = logging.getLogger('flask_jsonrpc')
    logger.handlers = []
    logger.setLevel(logging.NOTSET)

    logging_plugin = pytestconfig.pluginmanager.unregister(name='logging-plugin')

    yield

    logging.root.handlers[:] = root_handlers
    logging.root.setLevel(root_level)

    flask_logger.handlers = []
    flask_logger.setLevel(logging.NOTSET)

    logger.handlers = []
    logger.setLevel(logging.NOTSET)

    if logging_plugin:
        pytestconfig.pluginmanager.register(logging_plugin, 'logging-plugin')


class CustomException(Exception):
    def __init__(self: Self, message: str, data: dict[str, t.Any]) -> None:
        super().__init__(message)
        self.message = message
        self.data = data


def test_app_create() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    @jsonrpc.method('app.fn0')
    def fn0() -> None:
        pass

    @jsonrpc.method('app.fn1')
    def fn1() -> str:
        return 'Bar'

    @jsonrpc.method('app.fn2')
    def fn2(s: str) -> str:
        return f'Foo {s}'

    def fn3(s: str) -> str:
        return f'Foo {s}'

    @jsonrpc.method('app.fn4', notification=False)
    def fn4(s: str) -> str:
        return f'Goo {s}'

    jsonrpc.register(fn3, name='app.fn3')

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn0', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Bar'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn3', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn4', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Goo :)'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'app.fn4', 'params': [':)']})
        assert rv.json == {
            'error': {
                'code': -32600,
                'data': {
                    'message': "The method 'app.fn4' doesn't allow Notification Request object (without an 'id' member)"
                },
                'message': 'Invalid Request',
                'name': 'InvalidRequestError',
            },
            'id': None,
            'jsonrpc': '2.0',
        }
        assert rv.status_code == 400

        rv = client.post(
            '/api',
            data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'app.index'}),
            headers={'Content-Type': 'application/json-rpc'},
        )
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

        rv = client.post(
            '/api',
            data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []}),
            headers={'Content-Type': 'application/jsonrequest'},
        )
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

        rv = client.post(
            '/api',
            data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []}),
            headers={'Content-Type': 'application/json'},
        )
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200


def test_app_create_with_default_logger() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

    assert app.logger.name == 'test_app'
    assert app.logger.level == logging.NOTSET
    assert app.logger.handlers == [default_handler]

    assert jsonrpc.logger.name == 'flask_jsonrpc'
    assert jsonrpc.logger.level == logging.NOTSET
    assert jsonrpc.logger.handlers == [default_handler]


def test_app_create_with_custom_logger() -> None:
    with logger_lock:
        logger_handler = logging.StreamHandler()
        logger = logging.getLogger('flask_jsonrpc')
        logger.handlers = []
        logger.addHandler(logger_handler)
        logger.setLevel(logging.DEBUG)

        app = Flask('test_app', instance_relative_config=True)
        jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

        @jsonrpc.method('app.index')
        def index() -> str:
            return 'Welcome to Flask JSON-RPC'

        with app.test_client() as client:
            rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
            assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
            assert rv.status_code == 200

        assert app.logger.name == 'test_app'
        assert app.logger.level == logging.NOTSET
        assert app.logger.handlers == [default_handler]

        assert jsonrpc.logger.name == 'flask_jsonrpc'
        assert jsonrpc.logger.level == logging.DEBUG
        assert jsonrpc.logger.handlers == [logger_handler]


def test_app_create_using_error_handler() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.errorhandler(CustomException)
    def handle_custom_exc(exc: CustomException) -> dict[str, t.Any]:
        return exc.data

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    @jsonrpc.method('app.errorhandler')
    def fn0() -> t.NoReturn:
        raise CustomException('Testing error handler', data={'message': 'Flask JSON-RPC', 'code': '0000'})

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.errorhandler', 'params': []})
        assert rv.json == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'data': {'code': '0000', 'message': 'Flask JSON-RPC'},
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert rv.status_code == 500


def test_app_create_with_server_name() -> None:
    app = Flask('test_app', instance_relative_config=True)
    app.config.update({'SERVER_NAME': 'domain:80'})
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200


def test_app_create_without_register_app() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(path='/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn2')
    def fn1(s: str) -> str:
        return f'Foo {s}'

    jsonrpc.init_app(app)

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200


def test_app_create_without_register_browse() -> None:
    jsonrpc = JSONRPC(path='/api', enable_web_browsable_api=True)

    with pytest.raises(
        RuntimeError, match='you need to init the Browse app before register the Site, see JSONRPC.init_browse_app(...)'
    ):
        jsonrpc.register_browse(jsonrpc)


def test_app_create_with_method_without_annotation() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    with pytest.raises(ValueError, match='no type annotations present to: app.fn1'):

        @jsonrpc.method('app.fn1')
        def fn1(s):  # noqa: ANN001,ANN202
            return f'Foo {s}'

    @jsonrpc.method('app.fn2')
    def fn2(s: str) -> str:
        return f'Bar {s}'

    with pytest.raises(ValueError, match='no type annotations present to: app.fn3'):

        @jsonrpc.method('app.fn3')
        def fn3(s):  # noqa: ANN001,ANN202
            return f'Poo {s}'


def test_app_create_with_method_without_annotation_on_params() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn4')
    def fn4() -> None:
        pass

    with pytest.raises(ValueError, match='no type annotations present to: app.fn2'):

        @jsonrpc.method('app.fn2')
        def fn2(s) -> str:  # noqa: ANN001
            return f'Foo {s}'

    @jsonrpc.method('app.fn1')
    def fn1(s: str) -> str:
        return f'Bar {s}'

    with pytest.raises(ValueError, match='no type annotations present to: app.fn3'):

        @jsonrpc.method('app.fn3')
        def fn3(s):  # noqa: ANN001,ANN202
            return f'Poo {s}'


def test_app_create_with_method_without_annotation_on_return() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn1', validate=False)
    def fn1(s: str):  # noqa: ANN202
        return f'Foo {s}'

    @jsonrpc.method('app.fn2')
    def fn2(s: str) -> str:
        return f'Bar {s}'

    @jsonrpc.method('app.fn3')
    def fn3(s: str) -> t.NoReturn:
        raise ValueError(f'no return: {s}')

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': [':)']})
        assert rv.json == {'result': 'Foo :)', 'id': 1, 'jsonrpc': '2.0'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Bar :)'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn3', 'params': ['OK']})
        assert rv.json == {
            'error': {
                'code': -32000,
                'data': {'message': 'no return: OK'},
                'message': 'Server error',
                'name': 'ServerError',
            },
            'id': 1,
            'jsonrpc': '2.0',
        }
        assert rv.status_code == 500


def test_app_create_with_wrong_return() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn1')
    def fn2(s: str) -> tuple[str, int, int, int]:
        return f'Bar {s}', 1, 2, 3

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': [':)']})
        assert rv.json == {
            'error': {
                'code': -32000,
                'data': {
                    'message': 'the view function did not return a valid '
                    'response tuple. The tuple must have the form '
                    '(body, status, headers), (body, status), or '
                    '(body, headers).'
                },
                'message': 'Server error',
                'name': 'ServerError',
            },
            'id': 1,
            'jsonrpc': '2.0',
        }
        assert rv.status_code == 500


def test_app_create_with_invalid_view_func() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, path='/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn2')
    def fn1(s: str) -> str:
        return f'Foo {s}'

    with pytest.raises(ValueError, match='the view function must be either a function or a staticmethod'):
        jsonrpc.register(fn1.__new__, name='invalid')

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200


def test_app_create_multiple_jsonrpc_versions() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc_v1 = JSONRPC(app, '/api/v1', enable_web_browsable_api=True)
    jsonrpc_v2 = JSONRPC(app, '/api/v2', enable_web_browsable_api=True)

    @jsonrpc_v1.method('app.fn2')
    def fn1_v1(s: str) -> str:
        return f'v1: Foo {s}'

    @jsonrpc_v2.method('app.fn2')
    def fn1_v2(s: str) -> str:
        return f'v2: Foo {s}'

    @jsonrpc_v1.method('app.fn3')
    def fn3(s: str) -> str:
        return f'Poo {s}'

    @jsonrpc_v2.method('app.fn1')
    def fn2(s: str) -> str:
        return f'Bar {s}'

    def fn4_v1(s: str) -> str:
        return f'Poo {s}'

    jsonrpc_v1.register(fn4_v1)

    def fn4_v2(s: str) -> str:
        return f'Bar {s}'

    jsonrpc_v2.register(fn4_v2)

    with app.test_client() as client:
        rv = client.post('/api/v1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'v1: Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api/v2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':D']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'v2: Foo :D'}
        assert rv.status_code == 200

        rv = client.post('/api/v1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn3', 'params': [';)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Poo ;)'}
        assert rv.status_code == 200

        rv = client.post('/api/v2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': ['\\oB']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Bar \\oB'}
        assert rv.status_code == 200

        rv = client.post('/api/v1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'fn4_v1', 'params': ['\\oB']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Poo \\oB'}
        assert rv.status_code == 200

        rv = client.post('/api/v2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'fn4_v2', 'params': ['\\oB']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Bar \\oB'}
        assert rv.status_code == 200


def test_app_create_with_rcp_batch() -> None:
    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('sum')
    def sum_(a: int, b: int) -> int:
        return a + b

    @jsonrpc.method('subtract')
    def subtract(a: int, b: int) -> int:
        return a - b

    @jsonrpc.method('get_user')
    def get_user(uid: str) -> dict[str, t.Any]:
        return {'uid': uid, 'name': 'John Dee'}

    @jsonrpc.method('notify_sum')
    def notify_sum(numbers: list[int]) -> int:
        s = sum(x**2 for x in numbers)
        return s

    @jsonrpc.method('headers1')
    def headers1() -> tuple[float, int, list[tuple[str, t.Any]]]:
        return 3.141592653589793, 200, [('X-Header-1-a', 'a1'), ('X-Header-1-b', 'b1')]

    @jsonrpc.method('headers2')
    def headers2() -> tuple[float, int, tuple[str, t.Any]]:
        return 3.141592653589793, 201, ('X-Header-2-a', 'a2')

    @jsonrpc.method('headers3')
    def headers3() -> tuple[float, int, Headers]:
        headers = Headers()
        headers.set('X-Header-3-a', 'a3')
        headers.set('X-Header-3-b', 'b3')
        headers.set('X-Header-3-c', 'c3')
        return 3.141592653589793, 200, headers

    @jsonrpc.method('headers4')
    def headers4() -> tuple[float, int, dict[str, t.Any]]:
        return 3.141592653589793, 200, {'X-Header-4-a': 'a4', 'X-Header-4-b': 'b4'}

    @jsonrpc.method('headers_duplicate')
    def headers_duplicate() -> tuple[float, int, dict[str, t.Any]]:
        return (
            3.141592653589793,
            400,
            {
                'X-Header-2-a': 'a2-replaced',
                'X-Header-4-b': 'b4-replaced',
                'X-Header-3-c': 'c3-replaced',
                'X-Header-1-a': 'a1-replaced',
            },
        )

    with app.test_client() as client:
        idx = uuid.uuid4()
        rv = client.post('/api', json={'id': idx.hex, 'jsonrpc': '2.0', 'method': 'sum', 'params': [1, 1]})
        assert rv.json == {'id': idx.hex, 'jsonrpc': '2.0', 'result': 2}
        assert rv.status_code == 200

        rv = client.post('/api', json=[])
        assert rv.json == {
            'error': {
                'code': -32600,
                'data': {'message': 'Empty array'},
                'message': 'Invalid Request',
                'name': 'InvalidRequestError',
            },
            'id': None,
            'jsonrpc': '2.0',
        }
        assert rv.status_code == 400

        rv = client.post('/api', json=[1])
        assert rv.json == [
            {
                'error': {
                    'code': -32600,
                    'data': {'message': 'Invalid JSON: 1'},
                    'message': 'Invalid Request',
                    'name': 'InvalidRequestError',
                },
                'id': None,
                'jsonrpc': '2.0',
            }
        ]
        assert rv.status_code == 200

        rv = client.post('/api', json=[1, 2, 3])
        assert rv.json == [
            {
                'error': {
                    'code': -32600,
                    'data': {'message': 'Invalid JSON: 1'},
                    'message': 'Invalid Request',
                    'name': 'InvalidRequestError',
                },
                'id': None,
                'jsonrpc': '2.0',
            },
            {
                'error': {
                    'code': -32600,
                    'data': {'message': 'Invalid JSON: 2'},
                    'message': 'Invalid Request',
                    'name': 'InvalidRequestError',
                },
                'id': None,
                'jsonrpc': '2.0',
            },
            {
                'error': {
                    'code': -32600,
                    'data': {'message': 'Invalid JSON: 3'},
                    'message': 'Invalid Request',
                    'name': 'InvalidRequestError',
                },
                'id': None,
                'jsonrpc': '2.0',
            },
        ]
        assert rv.status_code == 200

        rv = client.post(
            '/api',
            json=[
                {'id': '1', 'jsonrpc': '2.0', 'method': 'sum', 'params': [1, 1]},
                {'id': '2', 'jsonrpc': '2.0', 'method': 'subtract', 'params': [2, 2]},
                {'id': '3', 'jsonrpc': '2.0', 'method': 'sum', 'params': [3, 3]},
                {'id': '4', 'jsonrpc': '2.0', 'method': 'headers1'},
            ],
        )
        assert rv.json == [
            {'id': '1', 'jsonrpc': '2.0', 'result': 2},
            {'id': '2', 'jsonrpc': '2.0', 'result': 0},
            {'id': '3', 'jsonrpc': '2.0', 'result': 6},
            {'id': '4', 'jsonrpc': '2.0', 'result': 3.141592653589793},
        ]
        assert rv.status_code == 200
        assert len(rv.headers) == 4
        assert 'Content-Type' in rv.headers
        assert 'Content-Length' in rv.headers
        assert rv.headers.get('X-Header-1-a') == 'a1'
        assert rv.headers.get('X-Header-1-b') == 'b1'

        rv = client.post(
            '/api',
            json=[
                {'id': '1', 'jsonrpc': '2.0', 'method': 'sum', 'params': [1, 1]},
                {'id': '2', 'jsonrpc': '2.0', 'method': 'subtract', 'params': [2, 2]},
                {'id': '3', 'jsonrpc': '2.0', 'method': 'get_user', 'params': {'uid': '345'}},
                {'jsonrpc': '2.0', 'method': 'notify_sum', 'params': [[1, 2, 3, 4, 5]]},
                {'id': 'h1', 'jsonrpc': '2.0', 'method': 'headers1'},
                {'id': 'h2', 'jsonrpc': '2.0', 'method': 'headers2'},
                {'id': 'h3', 'jsonrpc': '2.0', 'method': 'headers3'},
                {'id': 'h4', 'jsonrpc': '2.0', 'method': 'headers4'},
            ],
        )
        assert rv.json == [
            {'id': '1', 'jsonrpc': '2.0', 'result': 2},
            {'id': '2', 'jsonrpc': '2.0', 'result': 0},
            {'id': '3', 'jsonrpc': '2.0', 'result': {'uid': '345', 'name': 'John Dee'}},
            {'id': 'h1', 'jsonrpc': '2.0', 'result': 3.141592653589793},
            {'id': 'h2', 'jsonrpc': '2.0', 'result': 3.141592653589793},
            {'id': 'h3', 'jsonrpc': '2.0', 'result': 3.141592653589793},
            {'id': 'h4', 'jsonrpc': '2.0', 'result': 3.141592653589793},
        ]
        assert rv.status_code == 200
        assert len(rv.headers) == 10
        assert 'Content-Type' in rv.headers
        assert 'Content-Length' in rv.headers
        assert rv.headers.get('X-Header-1-a') == 'a1'
        assert rv.headers.get('X-Header-1-b') == 'b1'
        assert rv.headers.get('X-Header-2-a') == 'a2'
        assert rv.headers.get('X-Header-3-a') == 'a3'
        assert rv.headers.get('X-Header-3-b') == 'b3'
        assert rv.headers.get('X-Header-3-c') == 'c3'
        assert rv.headers.get('X-Header-4-a') == 'a4'
        assert rv.headers.get('X-Header-4-b') == 'b4'

        rv = client.post(
            '/api',
            json=[
                {'jsonrpc': '2.0', 'method': 'notify_sum', 'params': [[1, 2, 3, 4, 5]]},
                {'jsonrpc': '2.0', 'method': 'notify_sum', 'params': [[1, 2, 3, 4, 5]]},
                {'jsonrpc': '2.0', 'method': 'notify_sum', 'params': [[1, 2, 3, 4, 5]]},
            ],
        )
        assert rv.json is None
        assert rv.status_code == 204

        rv = client.post(
            '/api',
            json=[
                {'id': '1', 'jsonrpc': '2.0', 'method': 'sum', 'params': [1, 1]},
                1,
                {'id': '2', 'jsonrpc': '2.0', 'method': 'subtract', 'params': [2, 2]},
                {'id': 'h1', 'jsonrpc': '2.0', 'method': 'headers1'},
                {'id': 'h2', 'jsonrpc': '2.0', 'method': 'headers2'},
                {'id': 'h3', 'jsonrpc': '2.0', 'method': 'headers3'},
                {'id': 'h4', 'jsonrpc': '2.0', 'method': 'headers4'},
                {'id': 'h_duplicate', 'jsonrpc': '2.0', 'method': 'headers_duplicate'},
            ],
        )
        assert rv.json == [
            {'id': '1', 'jsonrpc': '2.0', 'result': 2},
            {
                'error': {
                    'code': -32600,
                    'data': {'message': 'Invalid JSON: 1'},
                    'message': 'Invalid Request',
                    'name': 'InvalidRequestError',
                },
                'id': None,
                'jsonrpc': '2.0',
            },
            {'id': '2', 'jsonrpc': '2.0', 'result': 0},
            {'id': 'h1', 'jsonrpc': '2.0', 'result': 3.141592653589793},
            {'id': 'h2', 'jsonrpc': '2.0', 'result': 3.141592653589793},
            {'id': 'h3', 'jsonrpc': '2.0', 'result': 3.141592653589793},
            {'id': 'h4', 'jsonrpc': '2.0', 'result': 3.141592653589793},
            {'id': 'h_duplicate', 'jsonrpc': '2.0', 'result': 3.141592653589793},
        ]
        assert rv.status_code == 200
        assert len(rv.headers) == 10
        assert 'Content-Type' in rv.headers
        assert 'Content-Length' in rv.headers
        assert rv.headers.get('X-Header-1-a') == 'a1-replaced'
        assert rv.headers.get('X-Header-1-b') == 'b1'
        assert rv.headers.get('X-Header-2-a') == 'a2-replaced'
        assert rv.headers.get('X-Header-3-a') == 'a3'
        assert rv.headers.get('X-Header-3-b') == 'b3'
        assert rv.headers.get('X-Header-3-c') == 'c3-replaced'
        assert rv.headers.get('X-Header-4-a') == 'a4'
        assert rv.headers.get('X-Header-4-b') == 'b4-replaced'


def test_app_create_with_register_blueprint() -> None:
    mock_jsonrpc_site = mock.MagicMock()
    mock_jsonrpc_site_api = mock.MagicMock()
    mock_as_view = mock.MagicMock()
    mock_as_view.__name__ = 'view_func'
    mock_jsonrpc_site_api.as_view.return_value = mock_as_view

    mock_jsonrpc_blueprint = mock.MagicMock()
    mock_jsonrpc_blueprint.get_jsonrpc_site.return_value = mock_jsonrpc_site
    mock_jsonrpc_blueprint.get_jsonrpc_site_api.return_value = mock_jsonrpc_site_api

    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, mock_jsonrpc_blueprint, '/blue', enable_web_browsable_api=True)

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200


def test_app_create_with_register_browse() -> None:
    mock_jsonrpc_site = mock.MagicMock()
    mock_jsonrpc_site_api = mock.MagicMock()

    mock_jsonrpc_blueprint = mock.MagicMock()
    mock_jsonrpc_blueprint.get_jsonrpc_site.return_value = mock_jsonrpc_site
    mock_jsonrpc_blueprint.get_jsonrpc_site_api.return_value = mock_jsonrpc_site_api

    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_browse(mock_jsonrpc_blueprint)

    @jsonrpc.method('app.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200


def test_app_create_with_register_browse_when_jsonrpc_browse_is_null_raises_exc() -> None:
    mock_jsonrpc_site = mock.MagicMock()
    mock_jsonrpc_site_api = mock.MagicMock()

    mock_jsonrpc_blueprint = mock.MagicMock()
    mock_jsonrpc_blueprint.get_jsonrpc_site.return_value = mock_jsonrpc_site
    mock_jsonrpc_blueprint.get_jsonrpc_site_api.return_value = mock_jsonrpc_site_api

    app = Flask('test_app', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api')

    with pytest.raises(RuntimeError):
        jsonrpc.register_browse(mock_jsonrpc_blueprint)
