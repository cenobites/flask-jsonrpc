# Copyright (c) 2020-2022, Cenobit Technologies, Inc. http://cenobit.es/
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

import pytest

pytest.importorskip('asgiref')


def test_app_greeting(async_client):
    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.greeting',
            'params': ['Python'],
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.greeting',
            'params': {'name': 'Flask'},
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200


def test_app_greeting_with_different_content_types(async_client):
    rv = async_client.post(
        '/api',
        data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}),
        headers={'Content-Type': 'application/json-rpc'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        data=json.dumps(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': ['Python'],
            }
        ),
        headers={'Content-Type': 'application/jsonrequest'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        data=json.dumps(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': {'name': 'Flask'},
            }
        ),
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200


def test_app_greeting_raise_parse_error(async_client):
    rv = async_client.post('/api', data={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {
                'message': 'Invalid mime type for JSON: application/x-www-form-urlencoded, '
                'use header Content-Type: application/json'
            },
            'message': 'Parse error',
            'name': 'ParseError',
        },
    }
    assert rv.status_code == 400

    rv = async_client.post(
        '/api',
        data="{'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}",
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {'message': 'Invalid JSON: b"{\'id\': 1, \'jsonrpc\': \'2.0\', \'method\': \'jsonrpc.greeting\'}"'},
            'message': 'Parse error',
            'name': 'ParseError',
        },
    }
    assert rv.status_code == 400

    rv = async_client.post(
        '/api',
        data="""[
            {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask'], 'id': '1'},
            {'jsonrpc': '2.0', 'method'
        ]""",
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {
                'message': 'Invalid JSON: b"[\\n            {\'jsonrpc\': '
                "'2.0', 'method': 'jsonrpc.greeting', 'params': "
                "['Flask'], 'id': '1'},\\n            "
                "{'jsonrpc': '2.0', 'method'\\n        "
                ']"'
            },
            'message': 'Parse error',
            'name': 'ParseError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_raise_invalid_request_error(async_client):
    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32600,
            'data': {'message': "Invalid JSON: {'id': 1, 'jsonrpc': '2.0'}"},
            'message': 'Invalid Request',
            'name': 'InvalidRequestError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_raise_invalid_params_error(async_client):
    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.greeting',
            'params': 'Wrong',
        },
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'Parameter structures are by-position (tuple, set, list) or by-name (dict): Wrong'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = async_client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': [1]},
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'type of argument "name" must be str; got int instead'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.greeting',
            'params': {'name': 2},
        },
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'type of argument "name" must be str; got int instead'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_raise_method_not_found_error(async_client):
    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'method-not-found'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'data': {'message': 'Method not found: method-not-found'},
            'message': 'Method not found',
            'name': 'MethodNotFoundError',
        },
    }
    assert rv.status_code == 400


def test_app_echo(async_client):
    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.echo',
            'params': ['Python'],
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.echo',
            'params': {'string': 'Flask'},
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Flask'}
    assert rv.status_code == 200


def test_app_echo_raise_invalid_params_error(async_client):
    rv = async_client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': 'Wrong'},
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'Parameter structures are by-position (tuple, set, list) or by-name (dict): Wrong'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = async_client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': [1]},
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'type of argument "string" must be str; got int instead'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.echo',
            'params': {'name': 2},
        },
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': "missing a required argument: 'string'"},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': "missing a required argument: 'string'"},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_notify(async_client):
    rv = async_client.post('/api', json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify'})
    assert rv.json is None
    assert rv.status_code == 204

    rv = async_client.post(
        '/api',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify', 'params': ['Some string']},
    )
    assert rv.json is None
    assert rv.status_code == 204


def test_app_not_allow_notify(async_client):
    rv = async_client.post('/api', json={'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify'})
    assert rv.json == {
        'error': {
            'code': -32600,
            'data': {
                'message': "The method 'jsonrpc.not_allow_notify' doesn't allow Notification Request "
                "object (without an 'id' member)"
            },
            'message': 'Invalid Request',
            'name': 'InvalidRequestError',
        },
        'id': None,
        'jsonrpc': '2.0',
    }
    assert rv.status_code == 400

    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.not_allow_notify',
            'params': ['Some string'],
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notify'}
    assert rv.status_code == 200


def test_app_no_return(async_client):
    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.noReturn'})
    assert rv.json == {
        'error': {
            'code': -32000,
            'data': {'message': 'no return'},
            'message': 'Server error',
            'name': 'ServerError',
        },
        'id': 1,
        'jsonrpc': '2.0',
    }
    assert rv.status_code == 500


def test_app_fails(async_client):
    rv = async_client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [2]},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 2}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json={'id': '1', 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [1]},
    )
    assert rv.json == {
        'id': '1',
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'message': 'number is odd'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }
    assert rv.status_code == 500


def test_app_strange_echo(async_client):
    data = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'jsonrpc.strangeEcho',
        'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask'],
    }
    rv = async_client.post('/api', json=data)
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask'],
    }
    assert rv.status_code == 200

    data = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'jsonrpc.strangeEcho',
        'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23],
    }
    rv = async_client.post('/api', json=data)
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Default'],
    }
    assert rv.status_code == 200


def test_app_sum(async_client):
    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [1, 3]}
    rv = async_client.post('/api', json=data)
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 4}
    assert rv.status_code == 200

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [0.5, 1.5]}
    rv = async_client.post('/api', json=data)
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 2.0}
    assert rv.status_code == 200


def test_app_decorators(async_client):
    data = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'jsonrpc.decorators',
        'params': ['Python'],
    }
    rv = async_client.post('/api', json=data)
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': 'Hello Python from decorator, ;)',
    }
    assert rv.status_code == 200


def test_app_return_status_code(async_client):
    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.returnStatusCode',
            'params': ['OK'],
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code OK'}
    assert rv.status_code == 201


def test_app_return_headers(async_client):
    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.returnHeaders',
            'params': ['OK'],
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Headers OK'}
    assert rv.status_code == 200
    assert ('X-JSONRPC', '1') in list(rv.headers)


def test_app_return_status_code_and_headers(async_client):
    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.returnStatusCodeAndHeaders',
            'params': ['OK'],
        },
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': 'Status Code and Headers OK',
    }
    assert rv.status_code == 400
    assert ('X-JSONRPC', '1') in list(rv.headers)


def test_app_with_rcp_batch(async_client):
    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json=[
            {
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': ['Python'],
            },
            {
                'id': 2,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': ['Flask'],
            },
            {
                'id': 3,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': ['JSON-RCP'],
            },
        ],
    )
    assert rv.json == [
        {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'},
        {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask'},
        {'id': 3, 'jsonrpc': '2.0', 'result': 'Hello JSON-RCP'},
    ]
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json=[
            {
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': ['Python'],
            },
            {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
            {'id': 3, 'jsonrpc': '2.0', 'params': ['Flask']},
            {
                'id': 4,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': ['JSON-RCP'],
            },
        ],
    )
    assert rv.json == [
        {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'},
        {
            'id': 3,
            'jsonrpc': '2.0',
            'error': {
                'code': -32600,
                'data': {'message': "Invalid JSON: {'id': 3, 'jsonrpc': '2.0', 'params': ['Flask']}"},
                'message': 'Invalid Request',
                'name': 'InvalidRequestError',
            },
        },
        {'id': 4, 'jsonrpc': '2.0', 'result': 'Hello JSON-RCP'},
    ]
    assert rv.status_code == 200

    rv = async_client.post('/api', json={'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200


def test_app_class(async_client):
    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'classapp.index'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'greeting', 'params': ['Python']},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'hello',
            'params': {'name': 'Flask'},
        },
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200

    rv = async_client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'echo', 'params': ['Python', 1]},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}
    assert rv.status_code == 200

    rv = async_client.post('/api', json={'jsonrpc': '2.0', 'method': 'notify', 'params': ['Python']})
    assert rv.status_code == 204

    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'fails', 'params': [13]})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'message': 'number is odd'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }
    assert rv.status_code == 500


def test_app_system_describe(async_client):
    rv = async_client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    assert rv.json['id'] == 1
    assert rv.json['jsonrpc'] == '2.0'
    assert rv.json['result']['name'] == 'Flask-JSONRPC'
    assert rv.json['result']['description'] is None
    assert rv.json['result']['version'] == '2.0'
    assert rv.json['result']['servers'] is not None
    assert 'url' in rv.json['result']['servers'][0]
    assert rv.json['result']['methods'] == {
        'jsonrpc.greeting': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String', 'required': False, 'nullable': False}],
            'returns': {'type': 'String'},
            'description': None,
        },
        'jsonrpc.echo': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {
                    'name': 'string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                },
                {
                    'name': '_some',
                    'type': 'Object',
                    'required': False,
                    'nullable': False,
                },
            ],
            'returns': {'type': 'String'},
            'description': None,
        },
        'jsonrpc.notify': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {
                    'name': '_string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                }
            ],
            'returns': {'type': 'Null'},
            'description': None,
        },
        'jsonrpc.not_allow_notify': {
            'type': 'method',
            'options': {'notification': False, 'validate': True},
            'params': [
                {
                    'name': '_string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                }
            ],
            'returns': {'type': 'String'},
            'description': None,
        },
        'jsonrpc.fails': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number', 'required': False, 'nullable': False}],
            'returns': {'type': 'Number'},
            'description': None,
        },
        'jsonrpc.strangeEcho': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {
                    'name': 'string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                },
                {'name': 'omg', 'type': 'Object', 'required': False, 'nullable': False},
                {'name': 'wtf', 'type': 'Array', 'required': False, 'nullable': False},
                {
                    'name': 'nowai',
                    'type': 'Number',
                    'required': False,
                    'nullable': False,
                },
                {
                    'name': 'yeswai',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                },
            ],
            'returns': {'type': 'Array'},
            'description': None,
        },
        'jsonrpc.sum': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {'name': 'a', 'type': 'Number', 'required': False, 'nullable': False},
                {'name': 'b', 'type': 'Number', 'required': False, 'nullable': False},
            ],
            'returns': {'type': 'Number'},
            'description': None,
        },
        'jsonrpc.decorators': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {
                    'name': 'string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                }
            ],
            'returns': {'type': 'String'},
            'description': None,
        },
        'jsonrpc.returnStatusCode': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String', 'required': False, 'nullable': False}],
            'returns': {'type': 'Array'},
            'description': None,
        },
        'jsonrpc.returnHeaders': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String', 'required': False, 'nullable': False}],
            'returns': {'type': 'Array'},
            'description': None,
        },
        'jsonrpc.returnStatusCodeAndHeaders': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String', 'required': False, 'nullable': False}],
            'returns': {'type': 'Array'},
            'description': None,
        },
        'jsonrpc.not_validate': {
            'type': 'method',
            'options': {'notification': True, 'validate': False},
            'params': [],
            'returns': {'type': 'Null'},
            'description': None,
        },
        'jsonrpc.noReturn': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {
                    'name': '_string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                }
            ],
            'returns': {'type': 'Null'},
            'description': None,
        },
        'classapp.index': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String', 'required': False, 'nullable': False}],
            'returns': {'type': 'String'},
            'description': None,
        },
        'greeting': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String', 'required': False, 'nullable': False}],
            'returns': {'type': 'String'},
            'description': None,
        },
        'hello': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String', 'required': False, 'nullable': False}],
            'returns': {'type': 'String'},
            'description': None,
        },
        'echo': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {
                    'name': 'string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                },
                {
                    'name': '_some',
                    'type': 'Object',
                    'required': False,
                    'nullable': False,
                },
            ],
            'returns': {'type': 'String'},
            'description': None,
        },
        'notify': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {
                    'name': '_string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                }
            ],
            'returns': {'type': 'Null'},
            'description': None,
        },
        'not_allow_notify': {
            'type': 'method',
            'options': {'notification': False, 'validate': True},
            'params': [
                {
                    'name': '_string',
                    'type': 'String',
                    'required': False,
                    'nullable': False,
                }
            ],
            'returns': {'type': 'String'},
            'description': None,
        },
        'fails': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number', 'required': False, 'nullable': False}],
            'returns': {'type': 'Number'},
            'description': None,
        },
    }

    assert rv.status_code == 200
