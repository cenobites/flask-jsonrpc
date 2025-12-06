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

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient


def test_index(client: 'FlaskClient') -> None:
    rv = client.post('/api/article', json={'id': 1, 'jsonrpc': '2.0', 'method': 'Article.index'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Article API'}
    assert rv.status_code == 200


def test_get_user(client: 'FlaskClient') -> None:
    rv = client.post('/api/article', json={'id': 1, 'jsonrpc': '2.0', 'method': 'Article.getArticle', 'params': [1]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Founded'}}
    assert rv.status_code == 200

    rv = client.post('/api/article', json={'id': 1, 'jsonrpc': '2.0', 'method': 'Article.getArticle', 'params': [11]})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'code': '2001', 'message': 'Article 11 not found'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }
    assert rv.status_code == 500


def test_rpc_describe(client: 'FlaskClient') -> None:
    rv = client.post('/api/article', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'Article.getArticle': {
            'name': 'Article.getArticle',
            'notification': True,
            'params': [{'name': 'id', 'type': 'Number'}],
            'returns': {
                'name': 'default',
                'properties': {'id': {'name': 'id', 'type': 'Number'}, 'name': {'name': 'name', 'type': 'String'}},
                'type': 'Object',
            },
            'type': 'method',
            'validation': True,
        },
        'Article.index': {
            'name': 'Article.index',
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
