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


def test_get_pets(client: 'FlaskClient', access_token: str) -> None:
    rv = client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'Petstore.get_pets', 'params': []},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    json_data = rv.get_json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert len(json_data['result']) > 1
    assert json_data['result'][0] == {'id': 1, 'name': 'Bob', 'tag': 'dog'}
    assert rv.status_code == 200


def test_create_pet(client: 'FlaskClient', access_token: str) -> None:
    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'Petstore.create_pet',
            'params': {'new_pet': {'name': 'Tequila', 'tag': 'cat'}},
        },
        headers={'Authorization': f'Bearer {access_token}'},
    )
    json_data = rv.get_json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert json_data['result']['id'] is not None
    assert json_data['result']['name'] == 'Tequila'
    assert json_data['result']['tag'] == 'cat'
    assert rv.status_code == 200


def test_get_by_id(client: 'FlaskClient', access_token: str) -> None:
    rv = client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'Petstore.get_pet_by_id', 'params': [1]},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Bob', 'tag': 'dog'}}
    assert rv.status_code == 200


def test_get_by_id_with_invalid_token(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'Petstore.get_pet_by_id', 'params': [1]},
        headers={'Authorization': 'Bearer invalid_token'},
    )
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'msg': 'Not enough segments'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }
    assert rv.status_code == 401


def test_delete_by_id(client: 'FlaskClient', access_token: str) -> None:
    rv = client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'Petstore.delete_pet_by_id', 'params': [2]},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 2, 'name': 'Eve', 'tag': 'cat'}}
    assert rv.status_code == 200


def test_rpc_describe(client: 'FlaskClient', access_token: str) -> None:
    rv = client.post(
        '/api',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'Petstore.create_pet': {
            'description': 'Creates a new pet in the store.\n\nDuplicates are allowed',
            'errors': [
                {
                    'code': -32000,
                    'data': {'message': 'Pet not found: <pet_id>'},
                    'message': 'Server error',
                    'status_code': 500,
                }
            ],
            'examples': [
                {
                    'name': 'default',
                    'params': [
                        {
                            'description': 'Tags to filter by',
                            'name': 'tags',
                            'summary': 'Tags to filter by',
                            'value': 'dog',
                        },
                        {
                            'description': 'Maximum number of results to return',
                            'name': 'limit',
                            'summary': 'Maximum number of results to return',
                            'value': 25,
                        },
                    ],
                }
            ],
            'name': 'Petstore.create_pet',
            'notification': True,
            'params': [
                {
                    'name': 'new_pet',
                    'properties': {
                        'name': {'name': 'name', 'summary': 'name of pet', 'type': 'String'},
                        'tag': {'name': 'tag', 'summary': 'tag of pet', 'type': 'String'},
                    },
                    'summary': 'Pet to add to the store',
                    'type': 'Object',
                }
            ],
            'returns': {
                'name': 'default',
                'properties': {
                    'id': {'name': 'id', 'type': 'Number'},
                    'name': {'name': 'name', 'type': 'String'},
                    'tag': {'name': 'tag', 'type': 'String'},
                },
                'summary': 'the newly created pet',
                'type': 'Object',
            },
            'tags': ['pet'],
            'type': 'method',
            'validation': True,
        },
        'Petstore.delete_pet_by_id': {
            'description': 'Deletes a single pet based on the ID supplied',
            'errors': [
                {
                    'code': -32000,
                    'data': {'message': 'Pet not found: <pet_id>'},
                    'message': 'Server error',
                    'status_code': 500,
                }
            ],
            'examples': [
                {
                    'name': 'default',
                    'params': [
                        {
                            'description': 'ID of pet to delete',
                            'name': 'id',
                            'summary': 'ID of pet to delete',
                            'value': 1,
                        }
                    ],
                }
            ],
            'name': 'Petstore.delete_pet_by_id',
            'notification': True,
            'params': [{'minimum': 1, 'name': 'id', 'summary': 'ID of pet to delete', 'type': 'Number'}],
            'returns': {
                'name': 'default',
                'properties': {
                    'id': {'name': 'id', 'type': 'Number'},
                    'name': {'name': 'name', 'type': 'String'},
                    'tag': {'name': 'tag', 'type': 'String'},
                },
                'summary': 'pet deleted',
                'type': 'Object',
            },
            'tags': ['pet'],
            'type': 'method',
            'validation': True,
        },
        'Petstore.get_pet_by_id': {
            'description': 'Returns a user based on a single ID, if the user does not have\naccess to the pet\n',
            'examples': [{'name': 'default', 'params': [{'description': '', 'name': 'id', 'summary': '', 'value': 1}]}],
            'name': 'Petstore.get_pet_by_id',
            'notification': True,
            'params': [{'minimum': 1, 'name': 'id', 'summary': 'ID of pet to fetch', 'type': 'Number'}],
            'returns': {
                'name': 'default',
                'properties': {
                    'id': {'name': 'id', 'type': 'Number'},
                    'name': {'name': 'name', 'type': 'String'},
                    'tag': {'name': 'tag', 'type': 'String'},
                },
                'summary': 'pet response',
                'type': 'Object',
            },
            'tags': ['pet'],
            'type': 'method',
            'validation': True,
        },
        'Petstore.get_pets': {
            'description': 'Returns all pets from the system that the user has access to\n'
            'Nam sed condimentum est. Maecenas tempor sagittis sapien, nec rhoncus '
            'sem sagittis sit amet. Aenean at gravida augue, ac iaculis sem. '
            'Curabitur odio lorem, ornare eget elementum nec, cursus id lectus. '
            'Duis mi turpis, pulvinar ac eros ac, tincidunt varius justo. In hac '
            'habitasse platea dictumst. Integer at adipiscing ante, a sagittis '
            'ligula. Aenean pharetra tempor ante molestie imperdiet. Vivamus id '
            'aliquam diam.',
            'errors': [
                {'code': -32000, 'data': {'message': 'Server error'}, 'message': 'ServerError', 'status_code': 500}
            ],
            'examples': [
                {
                    'name': 'default',
                    'params': [
                        {
                            'description': 'Tags to filter by',
                            'name': 'tags',
                            'summary': 'Tags to filter by',
                            'value': ['dog', 'cat'],
                        },
                        {
                            'description': 'Maximum number of results to return',
                            'name': 'limit',
                            'summary': 'Maximum number of results to return',
                            'value': 2,
                        },
                    ],
                }
            ],
            'name': 'Petstore.get_pets',
            'notification': True,
            'params': [
                {'name': 'tags', 'summary': 'tags to filter by', 'type': 'Array'},
                {'minimum': 1, 'name': 'limit', 'summary': 'maximum number of results to return', 'type': 'Number'},
            ],
            'returns': {'name': 'default', 'summary': 'pet response', 'type': 'Array'},
            'summary': 'Returns all pets from the system',
            'tags': ['pet'],
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
