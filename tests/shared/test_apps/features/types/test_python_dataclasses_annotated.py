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


def test_app_with_dataclass(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.createCar',
            'params': {'car': {'name': 'Fusca', 'tag': 'blue'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}}

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.createCar',
            'params': {'car': {'name': 'Fusca'}},
        },
    )
    assert rv.status_code == 400
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['error']['code'] == -32602
    assert "missing 1 required positional argument: 'tag'" in data['error']['data']['message']
    assert data['error']['message'] == 'Invalid params'
    assert data['error']['name'] == 'InvalidParamsError'

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.createManyCar',
            'params': {'cars': [{'name': 'Fusca', 'tag': 'blue'}, {'name': 'Kombi', 'tag': 'yellow'}]},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Fusca', 'tag': 'blue'}, {'id': 1, 'name': 'Kombi', 'tag': 'yellow'}],
    }

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.createManyCar',
            'params': {'cars': [{'name': 'Fusca', 'tag': 'blue'}], 'car': {'name': 'Kombi', 'tag': 'yellow'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Fusca', 'tag': 'blue'}, {'id': 1, 'name': 'Kombi', 'tag': 'yellow'}],
    }

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.createManyCar',
            'params': [
                [{'name': 'Fusca', 'tag': 'blue'}, {'name': 'Kombi', 'tag': 'yellow'}],
                {'name': 'Gol', 'tag': 'white'},
            ],
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [
            {'id': 0, 'name': 'Fusca', 'tag': 'blue'},
            {'id': 1, 'name': 'Kombi', 'tag': 'yellow'},
            {'id': 2, 'name': 'Gol', 'tag': 'white'},
        ],
    }

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.createManyFixCar',
            'params': {'cars': {'1': {'name': 'Fusca', 'tag': 'blue'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Fusca', 'tag': 'blue'}]}

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.removeCar',
            'params': {'car': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}}

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.removeCar',
            'params': {'car': None},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'types.python_dataclasses_annotated.removeCar', 'params': []},
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_dataclasses_annotated.removeCar',
            'params': {'car': {'id': 100, 'name': 'Fusca', 'tag': 'blue'}},
        },
    )
    assert rv.status_code == 500
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'car_id': 100, 'reason': 'The car with an ID greater than 10 does not exist.'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-dataclasses-annotated', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'}
    )
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'types.python_dataclasses_annotated.createCar': {
            'description': 'This method creates a new car dataclass object with an auto-generated ID.',
            'examples': [
                {
                    'description': 'This demonstrates creating a Car dataclass from a NewCar input.',
                    'name': 'Example of creating a car',
                    'params': [
                        {
                            'description': 'A NewCar dataclass with name and tag.',
                            'name': 'car',
                            'value': {'name': 'Tesla Model 3', 'tag': 'electric'},
                        }
                    ],
                    'returns': {
                        'description': 'The created Car dataclass with ID.',
                        'name': 'result',
                        'value': {'id': 1, 'name': 'Tesla Model 3', 'tag': 'electric'},
                    },
                    'summary': 'Create a car with name and tag',
                }
            ],
            'name': 'types.python_dataclasses_annotated.createCar',
            'notification': True,
            'params': [
                {
                    'description': 'The car dataclass object to create, containing name and tag.',
                    'name': 'car',
                    'nullable': False,
                    'properties': {
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': True,
                    'summary': 'A new car dataclass object',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'A Car dataclass with an auto-generated ID, name, and tag.',
                'name': 'default',
                'properties': {'id': {'name': 'id', 'type': 'Number'}},
                'summary': 'The created car dataclass object',
                'type': 'Object',
            },
            'summary': 'Create a new car',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_dataclasses_annotated.createManyCar': {
            'description': 'This method creates multiple car dataclass objects from a list and an optional single car.',
            'examples': [
                {
                    'description': 'This demonstrates creating multiple Car dataclasses from a list of NewCar objects.',
                    'name': 'Example of creating many cars',
                    'params': [
                        {
                            'description': 'A list of NewCar dataclass objects.',
                            'name': 'cars',
                            'value': [{'name': 'BMW i3', 'tag': 'electric'}, {'name': 'Toyota Prius', 'tag': 'hybrid'}],
                        },
                        {
                            'description': 'An optional additional NewCar dataclass object.',
                            'name': 'car',
                            'value': {'name': 'Honda Civic', 'tag': 'gas'},
                        },
                    ],
                    'returns': {
                        'description': 'List of created Car dataclass objects with auto-generated IDs.',
                        'name': 'result',
                        'value': [
                            {'id': 0, 'name': 'BMW i3', 'tag': 'electric'},
                            {'id': 1, 'name': 'Toyota Prius', 'tag': 'hybrid'},
                            {'id': 2, 'name': 'Honda Civic', 'tag': 'gas'},
                        ],
                    },
                    'summary': 'Create multiple cars with optional extra car',
                }
            ],
            'name': 'types.python_dataclasses_annotated.createManyCar',
            'notification': True,
            'params': [
                {
                    'description': 'A list of car dataclass objects to create.',
                    'name': 'cars',
                    'nullable': False,
                    'required': True,
                    'summary': 'List of new car dataclass objects',
                    'type': 'Array',
                },
                {
                    'description': 'An optional additional car to add to the list.',
                    'name': 'car',
                    'nullable': True,
                    'properties': {
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': False,
                    'summary': 'Optional additional car',
                    'type': 'Object',
                },
            ],
            'returns': {
                'description': 'A list of Car dataclass objects with auto-generated IDs.',
                'name': 'default',
                'summary': 'List of created car dataclass objects',
                'type': 'Array',
            },
            'summary': 'Create many cars',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_dataclasses_annotated.createManyFixCar': {
            'description': 'This method creates exactly 4 car dataclass objects with specific names and tags.',
            'examples': [
                {
                    'description': 'This demonstrates creating 4 Car dataclasses with predetermined values.',
                    'name': 'Example of creating many fixed cars',
                    'params': [],
                    'returns': {
                        'description': 'A list of 4 fixed Car dataclass objects with predetermined values.',
                        'name': 'result',
                        'value': [
                            {'id': 1, 'name': 'Volkswagen Jetta', 'tag': 'gas'},
                            {'id': 2, 'name': 'Chevrolet Bolt', 'tag': 'electric'},
                            {'id': 3, 'name': 'Lexus NX 300h', 'tag': 'hybrid'},
                            {'id': 4, 'name': 'Buick Regal', 'tag': 'gas'},
                        ],
                    },
                    'summary': 'Create 4 predefined cars',
                }
            ],
            'name': 'types.python_dataclasses_annotated.createManyFixCar',
            'notification': True,
            'params': [
                {
                    'description': 'A list of car dataclass objects to create.',
                    'name': 'cars',
                    'nullable': False,
                    'required': True,
                    'summary': 'List of new car dataclass objects',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'A list of 4 predefined Car dataclass objects.',
                'name': 'default',
                'summary': 'List of fixed car dataclass objects',
                'type': 'Array',
            },
            'summary': 'Create many fixed cars',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_dataclasses_annotated.removeCar': {
            'description': 'This method removes a car dataclass by its ID and can optionally be forced.',
            'examples': [
                {
                    'description': 'This demonstrates removing a Car dataclass by providing its ID.',
                    'name': 'Example of removing a car',
                    'params': [
                        {'description': 'The ID of the car to remove.', 'name': 'car_id', 'value': 1},
                        {'description': 'Whether to force the removal.', 'name': 'force', 'value': False},
                    ],
                    'returns': {
                        'description': 'The removed Car dataclass object.',
                        'name': 'result',
                        'value': {'id': 1, 'name': 'Removed Car', 'tag': 'removed'},
                    },
                    'summary': 'Remove a car by ID',
                }
            ],
            'name': 'types.python_dataclasses_annotated.removeCar',
            'notification': True,
            'params': [
                {
                    'description': 'An optional removed car to add to the list.',
                    'name': 'car',
                    'nullable': True,
                    'properties': {'id': {'name': 'id', 'type': 'Number'}},
                    'required': False,
                    'summary': 'Optional removed car',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'The Car dataclass object that was removed.',
                'name': 'default',
                'properties': {'id': {'name': 'id', 'type': 'Number'}},
                'summary': 'Removed car dataclass object',
                'type': 'Object',
            },
            'summary': 'Remove a car by ID',
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
