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
    from requests import Session


def test_app_class(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/class-apps', json={'id': 1, 'jsonrpc': '2.0', 'method': 'class_apps.index'})
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/class-apps', json={'id': 1, 'jsonrpc': '2.0', 'method': 'class_apps.greeting', 'params': ['Python']}
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/class-apps',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'class_apps.hello', 'params': {'name': 'Flask'}},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/class-apps', json={'id': 1, 'jsonrpc': '2.0', 'method': 'class_apps.echo', 'params': ['Python', 1]}
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/class-apps', json={'jsonrpc': '2.0', 'method': 'class_apps.notify', 'params': ['Python']}
    )
    assert rv.status_code == 204

    rv = session.post(
        f'{api_url}/class-apps', json={'id': 1, 'jsonrpc': '2.0', 'method': 'class_apps.fails', 'params': [13]}
    )
    assert rv.json() == {
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


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/class-apps', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    assert rv.status_code == 200
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'class_apps.index': {
            'name': 'class_apps.index',
            'notification': True,
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'class_apps.echo': {
            'name': 'class_apps.echo',
            'notification': True,
            'params': [{'name': 'string', 'type': 'String'}, {'name': '_some', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'class_apps.fails': {
            'name': 'class_apps.fails',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
            'type': 'method',
            'validation': True,
        },
        'class_apps.greeting': {
            'name': 'class_apps.greeting',
            'notification': True,
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'class_apps.hello': {
            'name': 'class_apps.hello',
            'notification': True,
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'class_apps.not_allow_notify': {
            'name': 'class_apps.not_allow_notify',
            'notification': False,
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'class_apps.notify': {
            'name': 'class_apps.notify',
            'notification': True,
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'Null'},
            'type': 'method',
            'validation': True,
        },
        'rpc.describe': {
            'name': 'rpc.describe',
            'summary': 'RPC Describe',
            'description': 'Service description for JSON-RPC 2.0',
            'notification': False,
            'params': [],
            'returns': {
                'name': 'default',
                'type': 'Object',
                'properties': {
                    'description': {'name': 'description', 'type': 'String'},
                    'id': {'name': 'id', 'type': 'String'},
                    'methods': {'name': 'methods', 'type': 'Null'},
                    'name': {'name': 'name', 'type': 'String'},
                    'servers': {'name': 'servers', 'type': 'Null'},
                    'title': {'name': 'title', 'type': 'String'},
                    'version': {'name': 'version', 'type': 'String'},
                },
            },
            'type': 'method',
            'validation': False,
        },
    }
