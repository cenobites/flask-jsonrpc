# pylint: disable=C0302
# Copyright (c) 2022-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
# pylint: disable=duplicate-code,too-many-public-methods
import os
import json

from .conftest import APITestCase

API_URL = os.environ['API_URL']

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class APITest(APITestCase):
    def test_greeting(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 'Flask'}}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_app_greeting_with_different_content_types(self: Self) -> None:
        rv = self.requests.post(
            API_URL,
            data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}),
            headers={'Content-Type': 'application/json-rpc'},
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL, data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']})
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 'Flask'}}),
            headers={'Content-Type': 'application/json'},
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_greeting_raise_parse_error(self: Self) -> None:
        rv = self.requests.post(API_URL, data={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertDictEqual(
            {
                'id': None,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32700,
                    'data': {'message': "Invalid JSON: b'id=1&jsonrpc=2.0&method=jsonrpc.greeting'"},
                    'message': 'Parse error',
                    'name': 'ParseError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(
            API_URL,
            data="{'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}",
            headers={'Content-Type': 'application/json'},
        )
        self.assertDictEqual(
            {
                'id': None,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32700,
                    'data': {
                        'message': "Invalid JSON: b\"{'id': 1, " "'jsonrpc': '2.0', " "'method': 'jsonrpc.greeting'}\""
                    },
                    'message': 'Parse error',
                    'name': 'ParseError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(
            API_URL,
            data="""[
                {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask'], 'id': '1'},
                {'jsonrpc': '2.0', 'method'
            ]""",
            headers={'Content-Type': 'application/json'},
        )
        self.assertDictEqual(
            {
                'id': None,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32700,
                    'data': {
                        'message': 'Invalid JSON: b"[\\n                '
                        "{'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', "
                        "'params': ['Flask'], 'id': '1'},\\n                "
                        "{'jsonrpc': '2.0', 'method'\\n            ]\""
                    },
                    'message': 'Parse error',
                    'name': 'ParseError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

    def test_greeting_raise_invalid_request_error(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0'})
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32600,
                    'data': {'message': "Invalid JSON: {'id': 1, 'jsonrpc': '2.0'}"},
                    'message': 'Invalid Request',
                    'name': 'InvalidRequestError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

    def test_greeting_raise_invalid_params_error(self: Self) -> None:
        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': 'Wrong'}
        )
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {'message': 'Parameter structures are by-position (list) or by-name (dict): Wrong'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': [1]})
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {'message': 'type of argument "name" must be str; got int instead'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 2}}
        )
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {'message': 'type of argument "name" must be str; got int instead'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

    def test_greeting_raise_method_not_found_error(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'method-not-found'})
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32601,
                    'data': {'message': 'Method not found: method-not-found'},
                    'message': 'Method not found',
                    'name': 'MethodNotFoundError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

    def test_echo(self: Self) -> None:
        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': ['Python']}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'string': 'Flask'}}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_echo_raise_invalid_params_error(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': 'Wrong'})
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {'message': 'Parameter structures are by-position (list) or by-name (dict): Wrong'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': [1]})
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {'message': 'type of argument "string" must be str; got int instead'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'name': 2}}
        )
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {'message': "missing a required argument: 'string'"},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo'})
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {'message': "missing a required argument: 'string'"},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

    def test_notify(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify'})
        self.assertEqual('', rv.text)
        self.assertEqual(204, rv.status_code)

        rv = self.requests.post(API_URL, json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify', 'params': ['Some string']})
        self.assertEqual('', rv.text)
        self.assertEqual(204, rv.status_code)

    def test_not_allow_notify(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify'})
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notify'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify', 'params': ['Some string']}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notify'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify', 'params': ['Some string']}
        )
        self.assertDictEqual(
            {
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
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

    def test_fails(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [2]})
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 2}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': '1', 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [1]})
        self.assertDictEqual(
            {
                'id': '1',
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'data': {'message': 'number is odd'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
            },
            rv.json(),
        )
        self.assertEqual(500, rv.status_code)

    def test_strange_echo(self: Self) -> None:
        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.strangeEcho',
            'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask'],
        }
        rv = self.requests.post(API_URL, json=data)
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask']}, rv.json()
        )
        self.assertEqual(200, rv.status_code)

        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.strangeEcho',
            'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23],
        }
        rv = self.requests.post(API_URL, json=data)
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Default']}, rv.json()
        )
        self.assertEqual(200, rv.status_code)

    def test_sum(self: Self) -> None:
        data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [1, 3]}
        rv = self.requests.post(API_URL, json=data)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 4}, rv.json())
        self.assertEqual(200, rv.status_code)

        data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [0.5, 1.5]}
        rv = self.requests.post(API_URL, json=data)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 2.0}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_decorators(self: Self) -> None:
        data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.decorators', 'params': ['Python']}
        rv = self.requests.post(API_URL, json=data)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_return_status_code(self: Self) -> None:
        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCode', 'params': ['OK']}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code OK'}, rv.json())
        self.assertEqual(201, rv.status_code)

    def test_return_headers(self: Self) -> None:
        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnHeaders', 'params': ['OK']}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Headers OK'}, rv.json())
        self.assertEqual(200, rv.status_code)
        self.assertEqual('1', rv.headers['X-JSONRPC'])

    def test_return_status_code_and_headers(self: Self) -> None:
        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCodeAndHeaders', 'params': ['OK']}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code and Headers OK'}, rv.json())
        self.assertEqual(400, rv.status_code)
        self.assertEqual('1', rv.headers['X-JSONRPC'])

    def test_not_validate_method(self: Self) -> None:
        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.not_validate', 'params': ['OK']}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Not validate: OK'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_mixin_not_validate_method(self: Self) -> None:
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.mixin_not_validate',
                'params': [':)', 1, 3.2, ':D', [1, 2, 3], {1: 1}],
            },
        )
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': "Not validate: :) 1 3.2 :D [1, 2, 3] {'1': 1}"}, rv.json()
        )
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.mixin_not_validate',
                'params': {'s': ':)', 't': 1, 'u': 3.2, 'v': ':D', 'x': [1, 2, 3], 'z': {1: 1}},
            },
        )
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': "Not validate: :) 1 3.2 :D [1, 2, 3] {'1': 1}"}, rv.json()
        )
        self.assertEqual(200, rv.status_code)

    def test_no_return_method(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.noReturn', 'params': []})
        self.assertDictEqual(
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'no return'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'id': 1,
                'jsonrpc': '2.0',
            },
            rv.json(),
        )
        self.assertEqual(500, rv.status_code)

    def test_with_rcp_batch(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json=[
                {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']},
                {'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
                {'id': 3, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['JSON-RCP']},
            ],
        )
        self.assertEqual(
            [
                {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'},
                {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask'},
                {'id': 3, 'jsonrpc': '2.0', 'result': 'Hello JSON-RCP'},
            ],
            rv.json(),
        )
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json=[
                {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']},
                {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
                {'id': 3, 'jsonrpc': '2.0', 'params': ['Flask']},
                {'id': 4, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['JSON-RCP']},
            ],
        )
        self.assertEqual(
            [
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
            ],
            rv.json(),
        )
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertDictEqual({'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_class(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'classapp.index'})
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'greeting', 'params': ['Python']})
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'hello', 'params': {'name': 'Flask'}}
        )
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'echo', 'params': ['Python', 1]})
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(API_URL, json={'jsonrpc': '2.0', 'method': 'notify', 'params': ['Python']})
        self.assertEqual(204, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'fails', 'params': [13]})
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'data': {'message': 'number is odd'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
            },
            rv.json(),
        )
        self.assertEqual(500, rv.status_code)

    def test_app_with_pythonclass(self: Self) -> None:
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createColor',
                'params': {'color': {'name': 'Blue', 'tag': 'good'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}, rv.json())

        rv = self.requests.post(
            API_URL,
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createColor', 'params': {'color': {'name': 'Red'}}},
        )
        self.assertEqual(400, rv.status_code)
        data = rv.json()
        self.assertEqual(1, data['id'])
        self.assertEqual('2.0', data['jsonrpc'])
        self.assertEqual(-32602, data['error']['code'])
        self.assertTrue("missing 1 required positional argument: 'tag'" in data['error']['data']['message'])
        self.assertEqual('Invalid params', data['error']['message'])
        self.assertEqual('InvalidParamsError', data['error']['name'])

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyColor',
                'params': {'colors': [{'name': 'Blue', 'tag': 'good'}, {'name': 'Red', 'tag': 'bad'}]},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Blue', 'tag': 'good'}, {'id': 1, 'name': 'Red', 'tag': 'bad'}],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyColor',
                'params': {'colors': [{'name': 'Blue', 'tag': 'good'}], 'color': {'name': 'Red', 'tag': 'bad'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Blue', 'tag': 'good'}, {'id': 1, 'name': 'Red', 'tag': 'bad'}],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
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
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Blue', 'tag': 'good'},
                    {'id': 1, 'name': 'Red', 'tag': 'bad'},
                    {'id': 2, 'name': 'Green', 'tag': 'yay'},
                ],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyFixColor',
                'params': {'colors': {'1': {'name': 'Blue', 'tag': 'good'}}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Blue', 'tag': 'good'}]}, rv.json()
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.removeColor',
                'params': {'color': {'id': 1, 'name': 'Blue', 'tag': 'good'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'good'}}, rv.json())

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeColor', 'params': {'color': None}}
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': None}, rv.json())

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeColor', 'params': []}
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': None}, rv.json())

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.removeColor',
                'params': {'color': {'id': 100, 'name': 'Blue', 'tag': 'good'}},
            },
        )
        self.assertEqual(500, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'data': {'color_id': 100, 'reason': 'The color with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
            },
            rv.json(),
        )

    def test_app_with_dataclass(self: Self) -> None:
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createCar',
                'params': {'car': {'name': 'Fusca', 'tag': 'blue'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}}, rv.json()
        )

        rv = self.requests.post(
            API_URL,
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createCar', 'params': {'car': {'name': 'Fusca'}}},
        )
        self.assertEqual(400, rv.status_code)
        data = rv.json()
        self.assertEqual(1, data['id'])
        self.assertEqual('2.0', data['jsonrpc'])
        self.assertEqual(-32602, data['error']['code'])
        self.assertTrue("missing 1 required positional argument: 'tag'" in data['error']['data']['message'])
        self.assertEqual('Invalid params', data['error']['message'])
        self.assertEqual('InvalidParamsError', data['error']['name'])

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyCar',
                'params': {'cars': [{'name': 'Fusca', 'tag': 'blue'}, {'name': 'Kombi', 'tag': 'yellow'}]},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Fusca', 'tag': 'blue'}, {'id': 1, 'name': 'Kombi', 'tag': 'yellow'}],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyCar',
                'params': {'cars': [{'name': 'Fusca', 'tag': 'blue'}], 'car': {'name': 'Kombi', 'tag': 'yellow'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Fusca', 'tag': 'blue'}, {'id': 1, 'name': 'Kombi', 'tag': 'yellow'}],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
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
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Fusca', 'tag': 'blue'},
                    {'id': 1, 'name': 'Kombi', 'tag': 'yellow'},
                    {'id': 2, 'name': 'Gol', 'tag': 'white'},
                ],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyFixCar',
                'params': {'cars': {'1': {'name': 'Fusca', 'tag': 'blue'}}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Fusca', 'tag': 'blue'}]}, rv.json()
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.removeCar',
                'params': {'car': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Fusca', 'tag': 'blue'}}, rv.json()
        )

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeCar', 'params': {'car': None}}
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': None}, rv.json())

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removeCar', 'params': []})
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': None}, rv.json())

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.removeCar',
                'params': {'car': {'id': 100, 'name': 'Fusca', 'tag': 'blue'}},
            },
        )
        self.assertEqual(500, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'data': {'car_id': 100, 'reason': 'The car with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
            },
            rv.json(),
        )

    def test_app_with_pydantic(self: Self) -> None:
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createPet',
                'params': {'pet': {'name': 'Eve', 'tag': 'dog'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}, rv.json())

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.createPet', 'params': {'pet': {'name': 'Eve'}}}
        )
        self.assertEqual(400, rv.status_code)
        self.assertDictEqual(
            {
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
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyPet',
                'params': {'pets': [{'name': 'Eve', 'tag': 'dog'}, {'name': 'Lou', 'tag': 'dog'}]},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Eve', 'tag': 'dog'}, {'id': 1, 'name': 'Lou', 'tag': 'dog'}],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyPet',
                'params': {'pets': [{'name': 'Eve', 'tag': 'dog'}], 'pet': {'name': 'Lou', 'tag': 'dog'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Eve', 'tag': 'dog'}, {'id': 1, 'name': 'Lou', 'tag': 'dog'}],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
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
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Eve', 'tag': 'dog'},
                    {'id': 1, 'name': 'Lou', 'tag': 'dog'},
                    {'id': 2, 'name': 'Tequila', 'tag': 'cat'},
                ],
            },
            rv.json(),
        )

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.createManyFixPet',
                'params': {'pets': {'1': {'name': 'Eve', 'tag': 'dog'}}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': [{'id': 1, 'name': 'Eve', 'tag': 'dog'}]}, rv.json())

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.removePet',
                'params': {'pet': {'id': 1, 'name': 'Eve', 'tag': 'dog'}},
            },
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Eve', 'tag': 'dog'}}, rv.json())

        rv = self.requests.post(
            API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removePet', 'params': {'pet': None}}
        )
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': None}, rv.json())

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.removePet', 'params': []})
        self.assertEqual(200, rv.status_code)
        self.assertDictEqual({'id': 1, 'jsonrpc': '2.0', 'result': None}, rv.json())

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.removePet',
                'params': {'pet': {'id': 100, 'name': 'Lou', 'tag': 'dog'}},
            },
        )
        self.assertEqual(500, rv.status_code)
        self.assertDictEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32000,
                    'data': {'pet_id': 100, 'reason': 'The pet with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
            },
            rv.json(),
        )

    def test_system_describe(self: Self) -> None:
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
        json_data = rv.json()
        self.assertEqual(1, json_data['id'])
        self.assertEqual('2.0', json_data['jsonrpc'])
        self.assertEqual('Flask-JSONRPC', json_data['result']['name'])
        self.assertTrue('description' not in json_data['result'])
        self.assertEqual('2.0', json_data['result']['version'])
        self.assertIsNotNone(json_data['result']['servers'])
        self.assertDictEqual(
            {
                'classapp.index': {
                    'options': {'notification': True, 'validate': True},
                    'params': [{'name': 'name', 'type': 'String'}],
                    'returns': {'type': 'String'},
                    'type': 'method',
                },
                'echo': {
                    'options': {'notification': True, 'validate': True},
                    'params': [{'name': 'string', 'type': 'String'}, {'name': '_some', 'type': 'Object'}],
                    'returns': {'type': 'String'},
                    'type': 'method',
                },
                'fails': {
                    'options': {'notification': True, 'validate': True},
                    'params': [{'name': 'n', 'type': 'Number'}],
                    'returns': {'type': 'Number'},
                    'type': 'method',
                },
                'greeting': {
                    'options': {'notification': True, 'validate': True},
                    'params': [{'name': 'name', 'type': 'String'}],
                    'returns': {'type': 'String'},
                    'type': 'method',
                },
                'hello': {
                    'options': {'notification': True, 'validate': True},
                    'params': [{'name': 'name', 'type': 'String'}],
                    'returns': {'type': 'String'},
                    'type': 'method',
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
                    'options': {'notification': True, 'validate': True},
                    'params': [{'name': 'string', 'type': 'String'}],
                    'returns': {'type': 'String'},
                    'type': 'method',
                },
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
                'not_allow_notify': {
                    'options': {'notification': False, 'validate': True},
                    'params': [{'name': '_string', 'type': 'String'}],
                    'returns': {'type': 'String'},
                    'type': 'method',
                },
                'notify': {
                    'options': {'notification': True, 'validate': True},
                    'params': [{'name': '_string', 'type': 'String'}],
                    'returns': {'type': 'Null'},
                    'type': 'method',
                },
                'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
            },
            json_data['result']['methods'],
        )

        self.assertEqual(200, rv.status_code)
