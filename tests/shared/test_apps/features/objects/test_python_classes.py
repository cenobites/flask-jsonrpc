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


def test_app_with_pythonclass(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/objects/python-classes',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createColor',
            'params': {'color': {'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}

    rv = session.post(
        f'{api_url}/objects/python-classes',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createColor', 'params': {'color': {'name': 'Red'}}},
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
        f'{api_url}/objects/python-classes',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyColor',
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
        f'{api_url}/objects/python-classes',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyColor',
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
        f'{api_url}/objects/python-classes',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyColor',
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
        f'{api_url}/objects/python-classes',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyFixColor',
            'params': {'colors': {'1': {'name': 'Blue', 'tag': 'good'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Blue', 'tag': 'good'}]}

    rv = session.post(
        f'{api_url}/objects/python-classes',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removeColor',
            'params': {'color': {'id': 1, 'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}

    rv = session.post(
        f'{api_url}/objects/python-classes',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeColor', 'params': {'color': None}},
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/objects/python-classes',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeColor', 'params': []},
    )
    assert rv.status_code == 200
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = session.post(
        f'{api_url}/objects/python-classes',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removeColor',
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
    rv = session.post(f'{api_url}/objects/python-classes', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '2.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'jsonrpc.createColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.createManyColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'colors', 'type': 'Array'}, {'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.createManyFixColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'colors', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.removeColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
    }
