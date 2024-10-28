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


def test_app_echo(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': ['Python']}
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'string': 'Flask'}},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Flask'}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'string': None}},
    )
    json_data = rv.json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert json_data['error']['code'] == -32602
    assert "missing 1 required positional argument: 'string'" in json_data['error']['data']['message']
    assert json_data['error']['message'] == 'Invalid params'
    assert json_data['error']['name'] == 'InvalidParamsError'
    assert rv.status_code == 400


def test_app_echo_raise_invalid_params_error(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': 'Wrong'}
    )
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'Parameter structures are by-position (list) or by-name (dict): Wrong'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = session.post(
        f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': [1]}
    )
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'argument "string" (int) is not an instance of str'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = session.post(
        f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'name': 2}}
    )
    json_data = rv.json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert json_data['error']['code'] == -32602
    assert "missing 1 required positional argument: 'string'" in json_data['error']['data']['message']
    assert json_data['error']['message'] == 'Invalid params'
    assert json_data['error']['name'] == 'InvalidParamsError'
    assert rv.status_code == 400

    rv = session.post(f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo'})
    json_data = rv.json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert json_data['error']['code'] == -32602
    assert "missing 1 required positional argument: 'string'" in json_data['error']['data']['message']
    assert json_data['error']['message'] == 'Invalid params'
    assert json_data['error']['name'] == 'InvalidParamsError'
    assert rv.status_code == 400


def test_app_notify(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/jsonrpc-basic', json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify'})
    assert rv.text == ''
    assert rv.status_code == 204

    rv = session.post(
        f'{api_url}/jsonrpc-basic', json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify', 'params': ['Some string']}
    )
    assert rv.text == ''
    assert rv.status_code == 204


def test_app_not_allow_notify(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/jsonrpc-basic', json={'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify'})
    assert rv.json() == {
        'error': {
            'code': -32600,
            'data': {
                'message': "The method 'jsonrpc.not_allow_notify' doesn't allow Notification Request "
                "object (without an 'id' member)"
            },
            'message': 'Invalid Request',
            'name': 'InvalidRequestError',
        },
        'id': None,
        'jsonrpc': '2.0',
    }
    assert rv.status_code == 400

    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify', 'params': ['Some string']},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notify'}
    assert rv.status_code == 200


def test_app_no_return(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.noReturn'})
    assert rv.json() == {
        'error': {'code': -32000, 'data': {'message': 'no return'}, 'message': 'Server error', 'name': 'ServerError'},
        'id': 1,
        'jsonrpc': '2.0',
    }
    assert rv.status_code == 500


def test_app_fails(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [2]}
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 2}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/jsonrpc-basic', json={'id': '1', 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [1]}
    )
    assert rv.json() == {
        'id': '1',
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'message': 'number is odd'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }
    assert rv.status_code == 500


def test_app_strange_echo(session: 'Session', api_url: str) -> None:
    data = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'jsonrpc.strangeEcho',
        'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask'],
    }
    rv = session.post(f'{api_url}/jsonrpc-basic', json=data)
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask']}
    assert rv.status_code == 200

    data = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'jsonrpc.strangeEcho',
        'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23],
    }
    rv = session.post(f'{api_url}/jsonrpc-basic', json=data)
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Default']}
    assert rv.status_code == 200


def test_app_sum(session: 'Session', api_url: str) -> None:
    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [1, 3]}
    rv = session.post(f'{api_url}/jsonrpc-basic', json=data)
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 4}
    assert rv.status_code == 200

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [0.5, 1.5]}
    rv = session.post(f'{api_url}/jsonrpc-basic', json=data)
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 2.0}
    assert rv.status_code == 200

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': {'a': None, 'b': None}}
    rv = session.post(f'{api_url}/jsonrpc-basic', json=data)
    json_data = rv.json()
    assert json_data['id'] == 1
    assert json_data['jsonrpc'] == '2.0'
    assert json_data['error']['code'] == -32602
    assert "missing 2 required positional arguments: 'a' and 'b'" in json_data['error']['data']['message']
    assert json_data['error']['message'] == 'Invalid params'
    assert json_data['error']['name'] == 'InvalidParamsError'
    assert rv.status_code == 400


def test_app_return_status_code(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCode', 'params': ['OK']},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code OK'}
    assert rv.status_code == 201


def test_app_return_headers(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnHeaders', 'params': ['OK']},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Headers OK'}
    assert rv.status_code == 200
    assert ('X-JSONRPC', '1') in list(rv.headers.items())


def test_app_return_status_code_and_headers(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCodeAndHeaders', 'params': ['OK']},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code and Headers OK'}
    assert rv.status_code == 400
    assert ('X-JSONRPC', '1') in list(rv.headers.items())


def test_app_with_rcp_batch(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json=[
            {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']},
            {'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
            {'id': 3, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['JSON-RCP']},
        ],
    )
    assert rv.json() == [
        {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'},
        {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask'},
        {'id': 3, 'jsonrpc': '2.0', 'result': 'Hello JSON-RCP'},
    ]
    assert rv.status_code == 200

    rv = session.post(
        f'{api_url}/jsonrpc-basic',
        json=[
            {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']},
            {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
            {'id': 3, 'jsonrpc': '2.0', 'params': ['Flask']},
            {'id': 4, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['JSON-RCP']},
        ],
    )
    assert rv.json() == [
        {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'},
        {
            'id': 3,
            'jsonrpc': '2.0',
            'error': {
                'code': -32600,
                'data': {'message': "Invalid JSON: {'id': 3, 'jsonrpc': '2.0', 'params': ['Flask']}"},
                'message': 'Invalid Request',
                'name': 'InvalidRequestError',
            },
        },
        {'id': 4, 'jsonrpc': '2.0', 'result': 'Hello JSON-RCP'},
    ]
    assert rv.status_code == 200

    rv = session.post(f'{api_url}/jsonrpc-basic', json={'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json() == {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/jsonrpc-basic', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '2.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'jsonrpc.echo': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'string', 'type': 'String'}, {'name': '_some', 'type': 'Object'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.fails': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'jsonrpc.greeting': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.mixin_not_validate': {
            'options': {'notification': True, 'validate': False},
            'params': [
                {'name': 's', 'type': 'Object'},
                {'name': 't', 'type': 'Number'},
                {'name': 'u', 'type': 'Object'},
                {'name': 'v', 'type': 'String'},
                {'name': 'x', 'type': 'Object'},
                {'name': 'z', 'type': 'Object'},
            ],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.noReturn': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'jsonrpc.not_allow_notify': {
            'options': {'notification': False, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.not_validate': {
            'options': {'notification': True, 'validate': False},
            'params': [{'name': 's', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.notify': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'jsonrpc.returnHeaders': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.returnStatusCode': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.returnStatusCodeAndHeaders': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.strangeEcho': {
            'options': {'notification': True, 'validate': True},
            'params': [
                {'name': 'string', 'type': 'String'},
                {'name': 'omg', 'type': 'Object'},
                {'name': 'wtf', 'type': 'Array'},
                {'name': 'nowai', 'type': 'Number'},
                {'name': 'yeswai', 'type': 'String'},
            ],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.sum': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'a', 'type': 'Number'}, {'name': 'b', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
    }
    assert rv.status_code == 200
