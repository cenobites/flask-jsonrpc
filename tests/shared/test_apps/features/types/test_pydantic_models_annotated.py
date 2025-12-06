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


def test_app_with_pydantic(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.createPet',
            'params': {'pet': {'name': 'Eve', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.createPet',
            'params': {'pet': {'name': 'Eve'}},
        },
    )
    assert rv.status_code == 400
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['error']['code'] == -32602
    assert data['error']['name'] == 'InvalidParamsError'
    assert data['error']['message'] == 'Invalid params'
    assert (
        '1 validation error for NewPet\n'
        'tag\n'
        "  Field required [type=missing, input_value={'name': 'Eve'}, "
        'input_type=dict]\n'
        '    For further information visit '
    ) in data['error']['data']['message']

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.createManyPet',
            'params': {'pets': [{'name': 'Eve', 'tag': 'dog'}, {'name': 'Lou', 'tag': 'dog'}]},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Eve', 'tag': 'dog'}, {'id': 1, 'name': 'Lou', 'tag': 'dog'}],
    }

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.createManyPet',
            'params': {'pets': [{'name': 'Eve', 'tag': 'dog'}], 'pet': {'name': 'Lou', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Eve', 'tag': 'dog'}, {'id': 1, 'name': 'Lou', 'tag': 'dog'}],
    }

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.createManyPet',
            'params': [
                [{'name': 'Eve', 'tag': 'dog'}, {'name': 'Lou', 'tag': 'dog'}],
                {'name': 'Tequila', 'tag': 'cat'},
            ],
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [
            {'id': 0, 'name': 'Eve', 'tag': 'dog'},
            {'id': 1, 'name': 'Lou', 'tag': 'dog'},
            {'id': 2, 'name': 'Tequila', 'tag': 'cat'},
        ],
    }

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.createManyFixPet',
            'params': {'pets': {'1': {'name': 'Eve', 'tag': 'dog'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Eve', 'tag': 'dog'}]}

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.removePet',
            'params': {'pet': {'id': 1, 'name': 'Eve', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.removePet',
            'params': {'pet': None},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'types.pydantic_models_annotated.removePet', 'params': []},
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.pydantic_models_annotated.removePet',
            'params': {'pet': {'id': 100, 'name': 'Lou', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 500
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'pet_id': 100, 'reason': 'The pet with an ID greater than 10 does not exist.'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/pydantic-models-annotated', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'}
    )
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'types.pydantic_models_annotated.createManyFixPet': {
            'description': 'This method creates pet Pydantic model objects from a dictionary of '
            'pet IDs to NewPet objects.',
            'examples': [
                {
                    'description': 'This demonstrates creating Pet Pydantic models from a '
                    'dictionary mapping IDs to NewPet objects.',
                    'name': 'Example of creating many pets from dictionary',
                    'params': [
                        {
                            'description': 'A dictionary mapping pet IDs to NewPet Pydantic model objects.',
                            'name': 'pets',
                            'value': {'1': {'name': 'Max', 'tag': 'dog'}, '2': {'name': 'Luna', 'tag': 'cat'}},
                        }
                    ],
                    'returns': {
                        'description': 'List of created Pet Pydantic model objects with IDs from dictionary keys.',
                        'name': 'result',
                        'value': [{'id': 1, 'name': 'Max', 'tag': 'dog'}, {'id': 2, 'name': 'Luna', 'tag': 'cat'}],
                    },
                    'summary': 'Create pets from dict mapping',
                }
            ],
            'name': 'types.pydantic_models_annotated.createManyFixPet',
            'notification': True,
            'params': [
                {
                    'description': 'A dictionary mapping pet IDs to NewPet Pydantic model objects.',
                    'name': 'pets',
                    'nullable': False,
                    'required': True,
                    'summary': 'Dictionary of pet ID to NewPet models',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'A list of Pet Pydantic model objects with IDs from dictionary keys.',
                'name': 'default',
                'summary': 'List of created pet Pydantic models',
                'type': 'Array',
            },
            'summary': 'Create many pets from dictionary',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.pydantic_models_annotated.createManyPet': {
            'description': 'This method creates multiple pet Pydantic model objects from a list '
            'and an optional single pet.',
            'examples': [
                {
                    'description': 'This demonstrates creating multiple Pet Pydantic models from '
                    'a list of NewPet objects.',
                    'name': 'Example of creating many pets',
                    'params': [
                        {
                            'description': 'A list of NewPet Pydantic model objects.',
                            'name': 'pets',
                            'value': [{'name': 'Rex', 'tag': 'dog'}, {'name': 'Whiskers', 'tag': 'cat'}],
                        },
                        {
                            'description': 'An optional additional NewPet Pydantic model object.',
                            'name': 'pet',
                            'value': {'name': 'Buddy', 'tag': 'dog'},
                        },
                    ],
                    'returns': {
                        'description': 'List of created Pet Pydantic model objects with auto-generated IDs.',
                        'name': 'result',
                        'value': [
                            {'id': 0, 'name': 'Rex', 'tag': 'dog'},
                            {'id': 1, 'name': 'Whiskers', 'tag': 'cat'},
                            {'id': 2, 'name': 'Buddy', 'tag': 'dog'},
                        ],
                    },
                    'summary': 'Create multiple pets with optional extra pet',
                }
            ],
            'name': 'types.pydantic_models_annotated.createManyPet',
            'notification': True,
            'params': [
                {
                    'description': 'A list of pet Pydantic model objects to create.',
                    'name': 'pets',
                    'nullable': False,
                    'required': True,
                    'summary': 'List of new pet Pydantic models',
                    'type': 'Array',
                },
                {
                    'description': 'An optional additional pet to add to the list.',
                    'name': 'pet',
                    'nullable': True,
                    'properties': {
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': False,
                    'summary': 'Optional additional pet',
                    'type': 'Object',
                },
            ],
            'returns': {
                'description': 'A list of Pet Pydantic model objects with auto-generated IDs.',
                'name': 'default',
                'summary': 'List of created pet Pydantic models',
                'type': 'Array',
            },
            'summary': 'Create many pets',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.pydantic_models_annotated.createPet': {
            'description': 'This method creates a pet Pydantic model object from a NewPet object.',
            'examples': [
                {
                    'description': 'This demonstrates creating a Pet Pydantic model from a NewPet object.',
                    'name': 'Example of creating a pet',
                    'params': [
                        {
                            'description': 'A NewPet Pydantic model object.',
                            'name': 'pet',
                            'value': {'name': 'Fluffy', 'tag': 'cat'},
                        }
                    ],
                    'returns': {
                        'description': 'The created Pet Pydantic model object with auto-generated ID.',
                        'name': 'result',
                        'value': {'id': 1, 'name': 'Fluffy', 'tag': 'cat'},
                    },
                    'summary': 'Create a pet from NewPet model',
                }
            ],
            'name': 'types.pydantic_models_annotated.createPet',
            'notification': True,
            'params': [
                {
                    'description': 'A NewPet Pydantic model object to create.',
                    'name': 'pet',
                    'nullable': False,
                    'properties': {
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': True,
                    'summary': 'New pet Pydantic model',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'A Pet Pydantic model object with auto-generated ID.',
                'name': 'default',
                'properties': {
                    'id': {'name': 'id', 'type': 'Number'},
                    'name': {'name': 'name', 'type': 'String'},
                    'tag': {'name': 'tag', 'type': 'String'},
                },
                'summary': 'Created pet Pydantic model',
                'type': 'Object',
            },
            'summary': 'Create a pet',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.pydantic_models_annotated.removePet': {
            'description': 'This method removes a pet Pydantic model and can raise exceptions for certain conditions.',
            'examples': [
                {
                    'description': 'This demonstrates removing a Pet Pydantic model with exception handling.',
                    'name': 'Example of removing a pet',
                    'params': [
                        {
                            'description': 'An optional Pet Pydantic model object to remove.',
                            'name': 'pet',
                            'value': {'id': 5, 'name': 'Charlie', 'tag': 'bird'},
                        }
                    ],
                    'returns': {
                        'description': 'The removed Pet Pydantic model object, or None if not provided.',
                        'name': 'result',
                        'value': {'id': 5, 'name': 'Charlie', 'tag': 'bird'},
                    },
                    'summary': 'Remove a pet with error handling',
                }
            ],
            'name': 'types.pydantic_models_annotated.removePet',
            'notification': True,
            'params': [
                {
                    'description': 'The Pet Pydantic model object to remove.',
                    'name': 'pet',
                    'nullable': True,
                    'properties': {
                        'id': {'name': 'id', 'type': 'Number'},
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': False,
                    'summary': 'Optional pet to remove',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'The Pet Pydantic model object that was removed, or None if not provided.',
                'name': 'default',
                'properties': {
                    'id': {'name': 'id', 'type': 'Number'},
                    'name': {'name': 'name', 'type': 'String'},
                    'tag': {'name': 'tag', 'type': 'String'},
                },
                'summary': 'Removed pet Pydantic model',
                'type': 'Object',
            },
            'summary': 'Remove a pet',
            'tags': ['types'],
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
    }
