# Copyright (c) 2024-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
        f'{api_url}/objects/pydantic-models',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createPet',
            'params': {'pet': {'name': 'Eve', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}

    rv = session.post(
        f'{api_url}/objects/pydantic-models',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createPet', 'params': {'pet': {'name': 'Eve'}}},
    )
    assert rv.status_code == 400
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {
                'message': '1 validation error for NewPet\n'
                'tag\n'
                "  Field required [type=missing, input_value={'name': 'Eve'}, "
                'input_type=dict]\n'
                '    For further information visit '
                'https://errors.pydantic.dev/2.9/v/missing'
            },
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }

    rv = session.post(
        f'{api_url}/objects/pydantic-models',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyPet',
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
        f'{api_url}/objects/pydantic-models',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyPet',
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
        f'{api_url}/objects/pydantic-models',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyPet',
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
        f'{api_url}/objects/pydantic-models',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyFixPet',
            'params': {'pets': {'1': {'name': 'Eve', 'tag': 'dog'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Eve', 'tag': 'dog'}]}

    rv = session.post(
        f'{api_url}/objects/pydantic-models',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removePet',
            'params': {'pet': {'id': 1, 'name': 'Eve', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}

    rv = session.post(
        f'{api_url}/objects/pydantic-models',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removePet', 'params': {'pet': None}},
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/objects/pydantic-models',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removePet', 'params': []},
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/objects/pydantic-models',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removePet',
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
    rv = session.post(f'{api_url}/objects/pydantic-models', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '2.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'jsonrpc.createManyFixPet': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'pets', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.createManyPet': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'pets', 'type': 'Array'}, {'name': 'pet', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.createPet': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'pet', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.removePet': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'pet', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
    }
