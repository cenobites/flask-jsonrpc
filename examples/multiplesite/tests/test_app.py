# Copyright (c) 2024-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

import pytest
from multiplesite.app import UnauthorizedError

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient


def test_index_v1(client: 'FlaskClient') -> None:
    rv = client.post('/api/v1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App1.index'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC Version API 1'}
    assert rv.status_code == 200


def test_index_v2(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api/v2',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'App2.index'},
        headers={'X-Username': 'username', 'X-Password': 'secret'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC Version API 2'}
    assert rv.status_code == 200


def test_index_v2_with_invalid_auth(client: 'FlaskClient') -> None:
    with pytest.raises(UnauthorizedError):
        client.post(
            '/api/v2',
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'App2.index'},
            headers={'X-Username': 'username', 'X-Password': 'invalid'},
        )


def test_rpc_describe_v1(client: 'FlaskClient') -> None:
    rv = client.post('/api/v1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'App1.index': {
            'name': 'App1.index',
            'notification': True,
            'params': [],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'rpc.describe': {
            'name': 'rpc.describe',
            'description': 'Service description for JSON-RPC 2.0',
            'notification': False,
            'params': [],
            'returns': {
                'name': 'default',
                'properties': {
                    'description': {'name': 'description', 'type': 'String'},
                    'id': {'name': 'id', 'type': 'String'},
                    'methods': {'name': 'methods', 'type': 'Null'},
                    'name': {'name': 'name', 'type': 'String'},
                    'servers': {'name': 'servers', 'type': 'Null'},
                    'title': {'name': 'title', 'type': 'String'},
                    'version': {'name': 'version', 'type': 'String'},
                },
                'type': 'Object',
            },
            'summary': 'RPC Describe',
            'type': 'method',
            'validation': False,
        },
    }


def test_rpc_describe_v2(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api/v2',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'},
        headers={'X-Username': 'username', 'X-Password': 'secret'},
    )
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'App2.index': {
            'name': 'App2.index',
            'notification': True,
            'params': [],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'rpc.describe': {
            'name': 'rpc.describe',
            'description': 'Service description for JSON-RPC 2.0',
            'notification': False,
            'params': [],
            'returns': {
                'name': 'default',
                'properties': {
                    'description': {'name': 'description', 'type': 'String'},
                    'id': {'name': 'id', 'type': 'String'},
                    'methods': {'name': 'methods', 'type': 'Null'},
                    'name': {'name': 'name', 'type': 'String'},
                    'servers': {'name': 'servers', 'type': 'Null'},
                    'title': {'name': 'title', 'type': 'String'},
                    'version': {'name': 'version', 'type': 'String'},
                },
                'type': 'Object',
            },
            'summary': 'RPC Describe',
            'type': 'method',
            'validation': False,
        },
    }
