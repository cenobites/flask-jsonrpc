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


def test_app_with_pythonclass(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.createColor',
            'params': {'color': {'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.createColor',
            'params': {'color': {'name': 'Red'}},
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
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.createManyColor',
            'params': {'colors': [{'name': 'Blue', 'tag': 'good'}, {'name': 'Red', 'tag': 'bad'}]},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Blue', 'tag': 'good'}, {'id': 1, 'name': 'Red', 'tag': 'bad'}],
    }

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.createManyColor',
            'params': {'colors': [{'name': 'Blue', 'tag': 'good'}], 'color': {'name': 'Red', 'tag': 'bad'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Blue', 'tag': 'good'}, {'id': 1, 'name': 'Red', 'tag': 'bad'}],
    }

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.createManyColor',
            'params': [
                [{'name': 'Blue', 'tag': 'good'}, {'name': 'Red', 'tag': 'bad'}],
                {'name': 'Green', 'tag': 'yay'},
            ],
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [
            {'id': 0, 'name': 'Blue', 'tag': 'good'},
            {'id': 1, 'name': 'Red', 'tag': 'bad'},
            {'id': 2, 'name': 'Green', 'tag': 'yay'},
        ],
    }

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.createManyFixColor',
            'params': {'colors': {'1': {'name': 'Blue', 'tag': 'good'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Blue', 'tag': 'good'}]}

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.removeColor',
            'params': {'color': {'id': 1, 'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.removeColor',
            'params': {'color': None},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'types.python_classes_annotated.removeColor', 'params': []},
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/types/python-classes-annotated',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'types.python_classes_annotated.removeColor',
            'params': {'color': {'id': 100, 'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 500
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'color_id': 100, 'reason': 'The color with an ID greater than 10 does not exist.'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-classes-annotated', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'}
    )
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'types.python_classes_annotated.createColor': {
            'description': 'This method creates a new color object with an auto-generated ID.',
            'examples': [
                {
                    'description': 'This demonstrates creating a Color object from a NewColor input.',
                    'name': 'Example of creating a color',
                    'params': [
                        {
                            'description': 'A NewColor object with name and tag.',
                            'name': 'color',
                            'value': {'name': 'Red', 'tag': 'primary'},
                        }
                    ],
                    'returns': {
                        'description': 'The created Color object with ID.',
                        'name': 'result',
                        'value': {'id': 1, 'name': 'Red', 'tag': 'primary'},
                    },
                    'summary': 'Create a color with name and tag',
                }
            ],
            'name': 'types.python_classes_annotated.createColor',
            'notification': True,
            'params': [
                {
                    'description': 'The color object to create, containing name and tag.',
                    'name': 'color',
                    'nullable': False,
                    'properties': {
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': True,
                    'summary': 'A new color object',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'A Color object with an auto-generated ID, name, and tag.',
                'name': 'default',
                'properties': {
                    'id': {'name': 'id', 'type': 'Number'},
                    'name': {'name': 'name', 'type': 'String'},
                    'tag': {'name': 'tag', 'type': 'String'},
                },
                'summary': 'The created color object',
                'type': 'Object',
            },
            'summary': 'Create a new color',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_classes_annotated.createManyColor': {
            'description': 'This method creates multiple color objects from a list and an optional single color.',
            'examples': [
                {
                    'description': 'This demonstrates creating multiple Color objects from a list of NewColor objects.',
                    'name': 'Example of creating many colors',
                    'params': [
                        {
                            'description': 'A list of NewColor objects.',
                            'name': 'colors',
                            'value': [{'name': 'Red', 'tag': 'primary'}, {'name': 'Blue', 'tag': 'primary'}],
                        },
                        {
                            'description': 'An optional additional NewColor object.',
                            'name': 'color',
                            'value': {'name': 'Green', 'tag': 'secondary'},
                        },
                    ],
                    'returns': {
                        'description': 'List of created Color objects with auto-generated IDs.',
                        'name': 'result',
                        'value': [
                            {'id': 0, 'name': 'Red', 'tag': 'primary'},
                            {'id': 1, 'name': 'Blue', 'tag': 'primary'},
                            {'id': 2, 'name': 'Green', 'tag': 'secondary'},
                        ],
                    },
                    'summary': 'Create multiple colors with optional extra color',
                }
            ],
            'name': 'types.python_classes_annotated.createManyColor',
            'notification': True,
            'params': [
                {
                    'description': 'A list of color objects to create.',
                    'name': 'colors',
                    'nullable': False,
                    'required': True,
                    'summary': 'List of new color objects',
                    'type': 'Array',
                },
                {
                    'description': 'An optional additional color to add to the list.',
                    'name': 'color',
                    'nullable': True,
                    'properties': {
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': False,
                    'summary': 'Optional additional color',
                    'type': 'Object',
                },
            ],
            'returns': {
                'description': 'A list of Color objects with auto-generated IDs.',
                'name': 'default',
                'summary': 'List of created color objects',
                'type': 'Array',
            },
            'summary': 'Create many colors',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_classes_annotated.createManyFixColor': {
            'description': 'This method creates multiple color objects from a dictionary where keys are color IDs.',
            'examples': [
                {
                    'description': 'This demonstrates creating Color objects from a dictionary of NewColor objects.',
                    'name': 'Example of creating colors from dictionary',
                    'params': [
                        {
                            'description': 'A dictionary with string keys (color IDs) and NewColor values.',
                            'name': 'colors',
                            'value': {'1': {'name': 'Red', 'tag': 'primary'}, '2': {'name': 'Blue', 'tag': 'primary'}},
                        }
                    ],
                    'returns': {
                        'description': 'List of created Color objects with IDs from dictionary keys.',
                        'name': 'result',
                        'value': [
                            {'id': 1, 'name': 'Red', 'tag': 'primary'},
                            {'id': 2, 'name': 'Blue', 'tag': 'primary'},
                        ],
                    },
                    'summary': 'Create colors with predefined IDs',
                }
            ],
            'name': 'types.python_classes_annotated.createManyFixColor',
            'notification': True,
            'params': [
                {
                    'description': 'A dictionary where keys are string color IDs and values are NewColor objects.',
                    'name': 'colors',
                    'nullable': False,
                    'required': True,
                    'summary': 'Dictionary of color ID to color object mapping',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'A list of Color objects with IDs parsed from dictionary keys.',
                'name': 'default',
                'summary': 'List of created color objects',
                'type': 'Array',
            },
            'summary': 'Create many colors from dictionary',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_classes_annotated.removeColor': {
            'description': 'This method removes a color object. Throws an exception if color ID is greater than 10.',
            'errors': [{'code': -32001, 'message': 'Color not found', 'status_code': 404}],
            'examples': [
                {
                    'description': 'This demonstrates removing a Color object. Returns the same object if successful.',
                    'name': 'Example of removing a color',
                    'params': [
                        {
                            'description': 'The Color object to remove.',
                            'name': 'color',
                            'value': {'id': 5, 'name': 'Purple', 'tag': 'secondary'},
                        }
                    ],
                    'returns': {
                        'description': 'The removed Color object if successful.',
                        'name': 'result',
                        'value': {'id': 5, 'name': 'Purple', 'tag': 'secondary'},
                    },
                    'summary': 'Remove a color by providing the color object',
                }
            ],
            'name': 'types.python_classes_annotated.removeColor',
            'notification': True,
            'params': [
                {
                    'description': 'The color object to remove. Can be null to test null handling.',
                    'name': 'color',
                    'nullable': True,
                    'properties': {
                        'id': {'name': 'id', 'type': 'Number'},
                        'name': {'name': 'name', 'type': 'String'},
                        'tag': {'name': 'tag', 'type': 'String'},
                    },
                    'required': False,
                    'summary': 'Color object to remove',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'The removed color object, or null if input was null.',
                'name': 'default',
                'nullable': True,
                'properties': {
                    'id': {'name': 'id', 'type': 'Number'},
                    'name': {'name': 'name', 'type': 'String'},
                    'tag': {'name': 'tag', 'type': 'String'},
                },
                'summary': 'Removed color object',
                'type': 'Object',
            },
            'summary': 'Remove a color',
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
