# Copyright (c) 2020-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
import json
import typing as t

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient


def test_app_greeting(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = client.post(
        '/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 'Flask'}}
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200


def test_app_greeting_with_different_content_types(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}),
        headers={'Content-Type': 'application/json-rpc'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = client.post(
        '/api',
        data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']}),
        headers={'Content-Type': 'application/jsonrequest'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = client.post(
        '/api',
        data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 'Flask'}}),
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200


def test_app_greeting_raise_parse_error(client: 'FlaskClient') -> None:
    rv = client.post('/api', data={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {
                'message': 'Invalid mime type for JSON: application/x-www-form-urlencoded, '
                'use header Content-Type: application/json'
            },
            'message': 'Parse error',
            'name': 'ParseError',
        },
    }
    assert rv.status_code == 400

    rv = client.post(
        '/api',
        data="{'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}",
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {'message': "Invalid JSON: b\"{'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}\""},
            'message': 'Parse error',
            'name': 'ParseError',
        },
    }
    assert rv.status_code == 400

    rv = client.post(
        '/api',
        data="""[
            {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask'], 'id': '1'},
            {'jsonrpc': '2.0', 'method'
        ]""",
        headers={'Content-Type': 'application/json'},
    )
    assert rv.json == {
        'id': None,
        'jsonrpc': '2.0',
        'error': {
            'code': -32700,
            'data': {
                'message': "Invalid JSON: b\"[\\n            {'jsonrpc': "
                "'2.0', 'method': 'jsonrpc.greeting', 'params': "
                "['Flask'], 'id': '1'},\\n            "
                "{'jsonrpc': '2.0', 'method'\\n        "
                ']"'
            },
            'message': 'Parse error',
            'name': 'ParseError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_raise_invalid_request_error(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32600,
            'data': {'message': "Invalid JSON: {'id': 1, 'jsonrpc': '2.0'}"},
            'message': 'Invalid Request',
            'name': 'InvalidRequestError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_raise_invalid_params_error(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': 'Wrong'})
    assert rv.json == {
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

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': [1]})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'type of argument "name" must be str; got int instead'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 2}})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'type of argument "name" must be str; got int instead'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_greeting_raise_method_not_found_error(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'method-not-found'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'data': {'message': 'Method not found: method-not-found'},
            'message': 'Method not found',
            'name': 'MethodNotFoundError',
        },
    }
    assert rv.status_code == 400


def test_app_echo(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': ['Python']})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}
    assert rv.status_code == 200

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'string': 'Flask'}})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Flask'}
    assert rv.status_code == 200

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'string': None}})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': "missing a required argument: 'string'"},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_echo_raise_invalid_params_error(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': 'Wrong'})
    assert rv.json == {
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

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': [1]})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'type of argument "string" must be str; got int instead'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'name': 2}})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': "missing a required argument: 'string'"},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo'})
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': "missing a required argument: 'string'"},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_notify(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify'})
    assert rv.json is None
    assert rv.status_code == 204

    rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify', 'params': ['Some string']})
    assert rv.json is None
    assert rv.status_code == 204


def test_app_not_allow_notify(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify'})
    assert rv.json == {
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

    rv = client.post(
        '/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify', 'params': ['Some string']}
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notify'}
    assert rv.status_code == 200


def test_app_no_return(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.noReturn'})
    assert rv.json == {
        'error': {'code': -32000, 'data': {'message': 'no return'}, 'message': 'Server error', 'name': 'ServerError'},
        'id': 1,
        'jsonrpc': '2.0',
    }
    assert rv.status_code == 500


def test_app_fails(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [2]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 2}
    assert rv.status_code == 200

    rv = client.post('/api', json={'id': '1', 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [1]})
    assert rv.json == {
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


def test_app_strange_echo(client: 'FlaskClient') -> None:
    data = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'jsonrpc.strangeEcho',
        'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask'],
    }
    rv = client.post('/api', json=data)
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask']}
    assert rv.status_code == 200

    data = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'jsonrpc.strangeEcho',
        'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23],
    }
    rv = client.post('/api', json=data)
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Default']}
    assert rv.status_code == 200


def test_app_sum(client: 'FlaskClient') -> None:
    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [1, 3]}
    rv = client.post('/api', json=data)
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 4}
    assert rv.status_code == 200

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [0.5, 1.5]}
    rv = client.post('/api', json=data)
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 2.0}
    assert rv.status_code == 200

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': {'a': None, 'b': None}}
    rv = client.post('/api', json=data)
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': "missing a required argument: 'a'"},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_decorators(client: 'FlaskClient') -> None:
    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.decorators', 'params': ['Python']}
    rv = client.post('/api', json=data)
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'}
    assert rv.status_code == 200


def test_app_return_status_code(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCode', 'params': ['OK']})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code OK'}
    assert rv.status_code == 201


def test_app_return_headers(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnHeaders', 'params': ['OK']})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Headers OK'}
    assert rv.status_code == 200
    assert ('X-JSONRPC', '1') in list(rv.headers)


def test_app_return_status_code_and_headers(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCodeAndHeaders', 'params': ['OK']}
    )
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code and Headers OK'}
    assert rv.status_code == 400
    assert ('X-JSONRPC', '1') in list(rv.headers)


def test_app_with_rcp_batch(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = client.post(
        '/api',
        json=[
            {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']},
            {'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
            {'id': 3, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['JSON-RCP']},
        ],
    )
    assert rv.json == [
        {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'},
        {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask'},
        {'id': 3, 'jsonrpc': '2.0', 'result': 'Hello JSON-RCP'},
    ]
    assert rv.status_code == 200

    rv = client.post(
        '/api',
        json=[
            {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']},
            {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
            {'id': 3, 'jsonrpc': '2.0', 'params': ['Flask']},
            {'id': 4, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['JSON-RCP']},
        ],
    )
    assert rv.json == [
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

    rv = client.post('/api', json={'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
    assert rv.json == {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200


def test_app_class(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'classapp.index'})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}
    assert rv.status_code == 200

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'greeting', 'params': ['Python']})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}
    assert rv.status_code == 200

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'hello', 'params': {'name': 'Flask'}})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}
    assert rv.status_code == 200

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'echo', 'params': ['Python', 1]})
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}
    assert rv.status_code == 200

    rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'notify', 'params': ['Python']})
    assert rv.status_code == 204

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'fails', 'params': [13]})
    assert rv.json == {
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


def test_app_with_invalid_union(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.invalidUnion1',
            'params': {'color': {'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 400
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {
                'message': 'the only type of union that is supported is: typing.Union[T, ' 'None] or typing.Optional[T]'
            },
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.invalidUnion2',
            'params': {'color': {'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 400
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {
                'message': 'the only type of union that is supported is: typing.Union[T, ' 'None] or typing.Optional[T]'
            },
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }


def test_app_with_pythontypes(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.literalType', 'params': {'x': 'X'}})
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'X'}


def test_app_with_pythonclass(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createColor',
            'params': {'color': {'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}

    rv = client.post(
        '/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createColor', 'params': {'color': {'name': 'Red'}}}
    )
    assert rv.status_code == 400
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['error']['code'] == -32602
    assert "missing 1 required positional argument: 'tag'" in data['error']['data']['message']
    assert data['error']['message'] == 'Invalid params'
    assert data['error']['name'] == 'InvalidParamsError'

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyColor',
            'params': {'colors': [{'name': 'Blue', 'tag': 'good'}, {'name': 'Red', 'tag': 'bad'}]},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Blue', 'tag': 'good'}, {'id': 1, 'name': 'Red', 'tag': 'bad'}],
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyColor',
            'params': {'colors': [{'name': 'Blue', 'tag': 'good'}], 'color': {'name': 'Red', 'tag': 'bad'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Blue', 'tag': 'good'}, {'id': 1, 'name': 'Red', 'tag': 'bad'}],
    }

    rv = client.post(
        '/api',
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
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [
            {'id': 0, 'name': 'Blue', 'tag': 'good'},
            {'id': 1, 'name': 'Red', 'tag': 'bad'},
            {'id': 2, 'name': 'Green', 'tag': 'yay'},
        ],
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyFixColor',
            'params': {'colors': {'1': {'name': 'Blue', 'tag': 'good'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Blue', 'tag': 'good'}]}

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removeColor',
            'params': {'color': {'id': 1, 'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}

    rv = client.post(
        '/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeColor', 'params': {'color': None}}
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeColor', 'params': []})
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removeColor',
            'params': {'color': {'id': 100, 'name': 'Blue', 'tag': 'good'}},
        },
    )
    assert rv.status_code == 500
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'color_id': 100, 'reason': 'The color with an ID greater than 10 does not exist.'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }


def test_app_with_dataclass(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createCar',
            'params': {'car': {'name': 'Fusca', 'tag': 'blue'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}}

    rv = client.post(
        '/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createCar', 'params': {'car': {'name': 'Fusca'}}}
    )
    assert rv.status_code == 400
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['error']['code'] == -32602
    assert "missing 1 required positional argument: 'tag'" in data['error']['data']['message']
    assert data['error']['message'] == 'Invalid params'
    assert data['error']['name'] == 'InvalidParamsError'

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyCar',
            'params': {'cars': [{'name': 'Fusca', 'tag': 'blue'}, {'name': 'Kombi', 'tag': 'yellow'}]},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Fusca', 'tag': 'blue'}, {'id': 1, 'name': 'Kombi', 'tag': 'yellow'}],
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyCar',
            'params': {'cars': [{'name': 'Fusca', 'tag': 'blue'}], 'car': {'name': 'Kombi', 'tag': 'yellow'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Fusca', 'tag': 'blue'}, {'id': 1, 'name': 'Kombi', 'tag': 'yellow'}],
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyCar',
            'params': [
                [{'name': 'Fusca', 'tag': 'blue'}, {'name': 'Kombi', 'tag': 'yellow'}],
                {'name': 'Gol', 'tag': 'white'},
            ],
        },
    )
    assert rv.status_code == 200
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [
            {'id': 0, 'name': 'Fusca', 'tag': 'blue'},
            {'id': 1, 'name': 'Kombi', 'tag': 'yellow'},
            {'id': 2, 'name': 'Gol', 'tag': 'white'},
        ],
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyFixCar',
            'params': {'cars': {'1': {'name': 'Fusca', 'tag': 'blue'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Fusca', 'tag': 'blue'}]}

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removeCar',
            'params': {'car': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}}

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeCar', 'params': {'car': None}})
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeCar', 'params': []})
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removeCar',
            'params': {'car': {'id': 100, 'name': 'Fusca', 'tag': 'blue'}},
        },
    )
    assert rv.status_code == 500
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'car_id': 100, 'reason': 'The car with an ID greater than 10 does not exist.'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }


def test_app_with_pydantic(client: 'FlaskClient') -> None:
    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createPet',
            'params': {'pet': {'name': 'Eve', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}

    rv = client.post(
        '/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createPet', 'params': {'pet': {'name': 'Eve'}}}
    )
    assert rv.status_code == 400
    assert rv.json == {
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

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyPet',
            'params': {'pets': [{'name': 'Eve', 'tag': 'dog'}, {'name': 'Lou', 'tag': 'dog'}]},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Eve', 'tag': 'dog'}, {'id': 1, 'name': 'Lou', 'tag': 'dog'}],
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyPet',
            'params': {'pets': [{'name': 'Eve', 'tag': 'dog'}], 'pet': {'name': 'Lou', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [{'id': 0, 'name': 'Eve', 'tag': 'dog'}, {'id': 1, 'name': 'Lou', 'tag': 'dog'}],
    }

    rv = client.post(
        '/api',
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
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'result': [
            {'id': 0, 'name': 'Eve', 'tag': 'dog'},
            {'id': 1, 'name': 'Lou', 'tag': 'dog'},
            {'id': 2, 'name': 'Tequila', 'tag': 'cat'},
        ],
    }

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.createManyFixPet',
            'params': {'pets': {'1': {'name': 'Eve', 'tag': 'dog'}}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Eve', 'tag': 'dog'}]}

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removePet',
            'params': {'pet': {'id': 1, 'name': 'Eve', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removePet', 'params': {'pet': None}})
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removePet', 'params': []})
    assert rv.status_code == 200
    assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}

    rv = client.post(
        '/api',
        json={
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.removePet',
            'params': {'pet': {'id': 100, 'name': 'Lou', 'tag': 'dog'}},
        },
    )
    assert rv.status_code == 500
    assert rv.json == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32000,
            'data': {'pet_id': 100, 'reason': 'The pet with an ID greater than 10 does not exist.'},
            'message': 'Server error',
            'name': 'ServerError',
        },
    }


def test_app_system_describe(client: 'FlaskClient') -> None:
    rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.get_json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '2.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'jsonrpc.greeting': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'type': 'String'},
        },
        'jsonrpc.echo': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'string', 'type': 'String'}, {'name': '_some', 'type': 'Object'}],
            'returns': {'type': 'String'},
        },
        'jsonrpc.notify': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
        },
        'jsonrpc.not_allow_notify': {
            'type': 'method',
            'options': {'notification': False, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'String'},
        },
        'jsonrpc.fails': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
        },
        'jsonrpc.strangeEcho': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [
                {'name': 'string', 'type': 'String'},
                {'name': 'omg', 'type': 'Object'},
                {'name': 'wtf', 'type': 'Array'},
                {'name': 'nowai', 'type': 'Number'},
                {'name': 'yeswai', 'type': 'String'},
            ],
            'returns': {'type': 'Array'},
        },
        'jsonrpc.sum': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'a', 'type': 'Number'}, {'name': 'b', 'type': 'Number'}],
            'returns': {'type': 'Number'},
        },
        'jsonrpc.createCar': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'car', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.createColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.createManyCar': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'cars', 'type': 'Array'}, {'name': 'car', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.createManyColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'colors', 'type': 'Array'}, {'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.createManyFixCar': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'cars', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.createManyFixColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'colors', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
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
        'jsonrpc.decorators': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'string', 'type': 'String'}],
            'returns': {'type': 'String'},
        },
        'jsonrpc.returnStatusCode': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'type': 'Array'},
        },
        'jsonrpc.removeCar': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'car', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.removeColor': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.removePet': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'pet', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.returnHeaders': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'type': 'Array'},
        },
        'jsonrpc.returnStatusCodeAndHeaders': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'type': 'Array'},
        },
        'jsonrpc.not_validate': {
            'type': 'method',
            'options': {'notification': True, 'validate': False},
            'params': [{'name': 's', 'type': 'Object'}],
            'returns': {'type': 'Object'},
        },
        'jsonrpc.invalidUnion1': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.invalidUnion2': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'color', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.literalType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'x', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.mixin_not_validate': {
            'type': 'method',
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
        },
        'jsonrpc.noReturn': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
        },
        'classapp.index': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'type': 'String'},
        },
        'greeting': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'type': 'String'},
        },
        'hello': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'name', 'type': 'String'}],
            'returns': {'type': 'String'},
        },
        'echo': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'string', 'type': 'String'}, {'name': '_some', 'type': 'Object'}],
            'returns': {'type': 'String'},
        },
        'notify': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'Null'},
        },
        'not_allow_notify': {
            'type': 'method',
            'options': {'notification': False, 'validate': True},
            'params': [{'name': '_string', 'type': 'String'}],
            'returns': {'type': 'String'},
        },
        'fails': {
            'type': 'method',
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
        },
        'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
    }

    assert rv.status_code == 200
