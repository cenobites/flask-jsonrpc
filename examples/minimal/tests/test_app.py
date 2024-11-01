# Copyright (c) 2024-2024, Cenobit Technologies, Inc. http://cenobit.es/
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

from werkzeug.datastructures import Headers

from tests.utils import EqMock

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient


def test_index(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.index'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
    assert rv.status_code == 200


def test_greeting(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.greeting', 'params': ['Tequila']})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Tequila'}
    assert rv.status_code == 200


def test_hello_default_args(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.helloDefaultArgs'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'We salute you Flask JSON-RPC'}
    assert rv.status_code == 200


def test_args_validate(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'App.argsValidate',
            'params': [1, 'a', False, [1, 'a', True], {'k1': 1, 'k2': 'v2'}],
        },
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': "Number: 1, String: a, Boolean: False, Array: [1, 'a', True], Object: {'k1': 1, 'k2': 'v2'}",
    }
    assert rv.status_code == 200


def test_notify(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'App.notify'})
    assert rv.text == ''
    assert rv.status_code == 204

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.notify'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}
    assert rv.status_code == 200


def test_not_notify(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'App.notNotify', 'params': ['method']})
    assert rv.json == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32600,
            'data': {
                'message': "The method 'App.notNotify' doesn't allow Notification Request "
                "object (without an 'id' member)"
            },
            'message': 'Invalid Request',
            'name': 'InvalidRequestError',
        },
    }
    assert rv.status_code == 400

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.notNotify', 'params': ['method']})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notification: method'}
    assert rv.status_code == 200


def test_fails(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.fails'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'message': 'example of fail'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }
    assert rv.status_code == 500


def test_fails_with_custom_exception(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.failsWithCustomException'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'message': 'It is a custom exception', 'code': '0001'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }
    assert rv.status_code == 500


def test_sum(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.sum', 'params': [1, 1]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 2}
    assert rv.status_code == 200


def test_subtract(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.subtract', 'params': [1, 2]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': -1}
    assert rv.status_code == 200


def test_multiply(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.multiply', 'params': {'a': 2, 'b': 5}})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 10}
    assert rv.status_code == 200


def test_divide(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.divide', 'params': [1, 1]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 1.0}
    assert rv.status_code == 200


def test_one_decorator(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.oneDecorator', 'terminal_id': 1})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Terminal ID: 1'}
    assert rv.status_code == 200


def test_multi_decorators(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.multiDecorators', 'terminal_id': 1})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': {
            'terminal_id': 1,
            'headers': {
                'User-Agent': EqMock(),
                'Host': 'localhost',
                'Content-Type': 'application/json',
                'Content-Length': '78',
            },
        },
    }
    assert rv.headers == Headers(
        [('Content-Type', 'application/json'), ('Content-Length', '169'), ('X-JSONRPC-Tag', 'JSONRPC 2.0')]
    )
    assert rv.status_code == 200


def test_rpc_describe(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '2.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'App.argsValidate': {
            'options': {'notification': True, 'validate': True},
            'params': [
                {'name': 'a1', 'type': 'Number'},
                {'name': 'a2', 'type': 'String'},
                {'name': 'a3', 'type': 'Boolean'},
                {'name': 'a4', 'type': 'Array'},
                {'name': 'a5', 'type': 'Object'},
            ],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'App.divide': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'a', 'type': 'Number'}, {'name': 'b', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'App.fails': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'App.failsWithCustomException': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'App.greeting': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'App.helloDefaultArgs': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'string', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'App.index': {
            'options': {'notification': True, 'validate': True},
            'params': [],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'App.multiDecorators': {
            'options': {'notification': True, 'validate': True},
            'params': [],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'App.multiply': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'a', 'type': 'Number'}, {'name': 'b', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'App.notNotify': {
            'options': {'notification': False, 'validate': True},
            'params': [{'name': 'string', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'App.notify': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'App.oneDecorator': {
            'options': {'notification': True, 'validate': True},
            'params': [],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'App.subtract': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'a', 'type': 'Number'}, {'name': 'b', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'App.sum': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'a', 'type': 'Number'}, {'name': 'b', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
    }
