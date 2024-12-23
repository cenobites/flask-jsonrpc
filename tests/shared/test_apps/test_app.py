# Copyright (c) 2020-2024, Cenobit Technologies, Inc. http://cenobit.es/
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

from flask import json

if t.TYPE_CHECKING:
    from requests import Session


def test_app_greeting(session: 'Session', api_url: str) -> None:
    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']})
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = session.post(
        api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 'Flask'}}
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200

    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 1}})
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'argument "name" (int) is not an instance of str'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_with_different_content_types(session: 'Session', api_url: str) -> None:
    rv = session.post(
        api_url,
        data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}),
        headers={'Content-Type': 'application/json-rpc'},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = session.post(
        api_url,
        data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']}),
        headers={'Content-Type': 'application/jsonrequest'},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = session.post(
        api_url,
        data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 'Flask'}}),
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200


def test_app_greeting_raise_parse_error(session: 'Session', api_url: str) -> None:
    rv = session.post(api_url, data={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json() == {
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

    rv = session.post(
        api_url,
        data="{'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}",
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json() == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {'message': "Invalid JSON: b\"{'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}\""},
            'message': 'Parse error',
            'name': 'ParseError',
        },
    }
    assert rv.status_code == 400

    rv = session.post(
        api_url,
        data="""[
            {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask'], 'id': '1'},
            {'jsonrpc': '2.0', 'method'
        ]""",
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json() == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {
                'message': "Invalid JSON: b\"[\\n            {'jsonrpc': "
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


def test_app_greeting_raise_invalid_request_error(session: 'Session', api_url: str) -> None:
    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0'})
    assert rv.json() == {
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


def test_app_greeting_raise_invalid_params_error(session: 'Session', api_url: str) -> None:
    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': 'Wrong'})
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'Parameter structures are by-position (list) or by-name (dict): Wrong'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': [1]})
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'argument "name" (int) is not an instance of str'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 2}})
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'argument "name" (int) is not an instance of str'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_raise_method_not_found_error(session: 'Session', api_url: str) -> None:
    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'method-not-found'})
    assert rv.json() == {
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


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '2.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'jsonrpc.greeting': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
    }
    assert rv.status_code == 200
