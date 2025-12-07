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


def test_get_pets(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'Petstore.get_pets', 'params': []})
    json_data = rv.get_json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert len(json_data['result']) > 1
    assert json_data['result'][0] == {'id': 1, 'name': 'Bob', 'tag': 'dog'}
    assert rv.status_code == 200


def test_create_pet(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'Petstore.create_pet',
            'params': {'new_pet': {'name': 'Tequila', 'tag': 'cat'}},
        },
    )
    json_data = rv.get_json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert json_data['result']['id'] is not None
    assert json_data['result']['name'] == 'Tequila'
    assert json_data['result']['tag'] == 'cat'
    assert rv.status_code == 200


def test_get_by_id(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'Petstore.get_pet_by_id', 'params': [1]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Bob', 'tag': 'dog'}}
    assert rv.status_code == 200


def test_delete_by_id(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'Petstore.delete_pet_by_id', 'params': [2]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 2, 'name': 'Eve', 'tag': 'cat'}}
    assert rv.status_code == 200


def test_rpc_discover(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.discover'})
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result'] == {
        'components': {
            'schemas': {
                'NewPet': {
                    'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}},
                    'required': ['name'],
                    'type': 'object',
                },
                'Pet': {
                    'allOf': [
                        {'$ref': '#/components/schemas/NewPet'},
                        {'properties': {'id': {'type': 'integer'}}, 'required': ['id']},
                    ]
                },
            }
        },
        'externalDocs': {
            'url': 'https://github.com/open-rpc/examples/blob/master/service-descriptions/petstore-expanded-openrpc.json'
        },
        'info': {
            'contact': {'email': 'doesntexist@open-rpc.org', 'name': 'OpenRPC Team', 'url': 'https://open-rpc.org'},
            'description': 'A sample API that uses a petstore as an example to demonstrate '
            'features in the OpenRPC specification',
            'license': {'name': 'Apache 2.0', 'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'},
            'termsOfService': 'https://open-rpc.org',
            'title': 'Petstore Expanded',
            'version': '1.0.0',
        },
        'methods': [
            {
                'name': 'rpc.describe',
                'description': 'Service description for JSON-RPC 2.0',
                'params': [],
                'result': {'name': 'default', 'schema': {'type': 'object'}},
            },
            {
                'description': 'Returns an OpenRPC schema as a description of this service',
                'name': 'rpc.discover',
                'params': [],
                'result': {
                    'name': 'OpenRPC Schema',
                    'schema': {'$ref': 'https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'},
                },
            },
            {
                'description': 'Returns all pets from the system that the user has access to\n'
                'Nam sed condimentum est. Maecenas tempor sagittis sapien, nec '
                'rhoncus sem sagittis sit amet. Aenean at gravida augue, ac '
                'iaculis sem. Curabitur odio lorem, ornare eget elementum nec, '
                'cursus id lectus. Duis mi turpis, pulvinar ac eros ac, tincidunt '
                'varius justo. In hac habitasse platea dictumst. Integer at '
                'adipiscing ante, a sagittis ligula. Aenean pharetra tempor ante '
                'molestie imperdiet. Vivamus id aliquam diam.',
                'name': 'Petstore.get_pets',
                'params': [
                    {
                        'description': 'tags to filter by',
                        'name': 'tags',
                        'schema': {'items': {'type': 'string'}, 'type': 'array'},
                    },
                    {
                        'description': 'maximum number of results to return',
                        'name': 'limit',
                        'schema': {'type': 'integer'},
                    },
                ],
                'result': {
                    'description': 'pet response',
                    'name': 'pet',
                    'schema': {'items': {'$ref': '#/components/schemas/Pet'}, 'type': 'array'},
                },
            },
            {
                'description': 'Creates a new pet in the store.  Duplicates are allowed',
                'name': 'Petstore.create_pet',
                'params': [
                    {
                        'description': 'Pet to add to the store.',
                        'name': 'newPet',
                        'schema': {'$ref': '#/components/schemas/NewPet'},
                    }
                ],
                'result': {
                    'description': 'the newly created pet',
                    'name': 'pet',
                    'schema': {'$ref': '#/components/schemas/Pet'},
                },
            },
            {
                'description': 'Returns a user based on a single ID, if the user does not have access to the pet',
                'name': 'Petstore.get_pet_by_id',
                'params': [
                    {'description': 'ID of pet to fetch', 'name': 'id', 'required': True, 'schema': {'type': 'integer'}}
                ],
                'result': {
                    'description': 'pet response',
                    'name': 'pet',
                    'schema': {'$ref': '#/components/schemas/Pet'},
                },
            },
            {
                'description': 'deletes a single pet based on the ID supplied',
                'name': 'Petstore.delete_pet_by_id',
                'params': [
                    {
                        'description': 'ID of pet to delete',
                        'name': 'id',
                        'required': True,
                        'schema': {'type': 'integer'},
                    }
                ],
                'result': {'description': 'pet deleted', 'name': 'pet', 'schema': {}},
            },
        ],
        'openrpc': '1.0.0-rc1',
        'servers': [{'name': 'default', 'url': 'http://petstore.open-rpc.org'}],
    }


def test_rpc_describe(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'Petstore.create_pet': {
            'name': 'Petstore.create_pet',
            'notification': True,
            'params': [
                {
                    'name': 'new_pet',
                    'properties': {
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'type': 'Object',
                }
            ],
            'returns': {'name': 'default', 'properties': {'id': {'name': 'id', 'type': 'Number'}}, 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'Petstore.delete_pet_by_id': {
            'name': 'Petstore.delete_pet_by_id',
            'notification': True,
            'params': [{'name': 'id', 'type': 'Number'}],
            'returns': {'name': 'default', 'properties': {'id': {'name': 'id', 'type': 'Number'}}, 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'Petstore.get_pet_by_id': {
            'name': 'Petstore.get_pet_by_id',
            'notification': True,
            'params': [{'name': 'id', 'type': 'Number'}],
            'returns': {'name': 'default', 'properties': {'id': {'name': 'id', 'type': 'Number'}}, 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'Petstore.get_pets': {
            'name': 'Petstore.get_pets',
            'notification': True,
            'params': [{'name': 'tags', 'type': 'Array'}, {'name': 'limit', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'rpc.describe': {
            'description': 'Service description for JSON-RPC 2.0',
            'name': 'rpc.describe',
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
        'rpc.discover': {
            'name': 'rpc.discover',
            'notification': True,
            'params': [],
            'returns': {'name': 'default', 'type': 'Null'},
            'type': 'method',
            'validation': True,
        },
    }
