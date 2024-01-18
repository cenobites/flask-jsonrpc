# pylint: disable=C0302
# Copyright (c) 2022-2022, Cenobit Technologies, Inc. http://cenobit.es/
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


class APITest(APITestCase):
    def test_greeting(self):
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': ['Python'],
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': {'name': 'Flask'},
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_app_greeting_with_different_content_types(self):
        rv = self.requests.post(
            API_URL,
            data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'}),
            headers={'Content-Type': 'application/json-rpc'},
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            data=json.dumps(
                {
                    'id': 1,
                    'jsonrpc': '2.0',
                    'method': 'jsonrpc.greeting',
                    'params': ['Python'],
                }
            ),
            headers={'Content-Type': 'application/jsonrequest'},
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            data=json.dumps(
                {
                    'id': 1,
                    'jsonrpc': '2.0',
                    'method': 'jsonrpc.greeting',
                    'params': {'name': 'Flask'},
                }
            ),
            headers={'Content-Type': 'application/json'},
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_greeting_raise_parse_error(self):
        rv = self.requests.post(API_URL, data={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertEqual(
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
        self.assertEqual(
            {
                'id': None,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32700,
                    'data': {
                        'message': 'Invalid JSON: b"{\'id\': 1, '
                        '\'jsonrpc\': \'2.0\', '
                        '\'method\': \'jsonrpc.greeting\'}"'
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
        self.assertEqual(
            {
                'id': None,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32700,
                    'data': {
                        'message': "Invalid JSON: b\"[\\n                "
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

    def test_greeting_raise_invalid_request_error(self):
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0'})
        self.assertEqual(
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

    def test_greeting_raise_invalid_params_error(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': 'Wrong',
            },
        )
        self.assertEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {
                        'message': 'Parameter structures are by-position (tuple, set, list) or by-name (dict): Wrong'
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': [1],
            },
        )
        self.assertEqual(
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
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.greeting',
                'params': {'name': 2},
            },
        )
        self.assertEqual(
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

    def test_greeting_raise_method_not_found_error(self):
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'method-not-found'})
        self.assertEqual(
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

    def test_echo(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.echo',
                'params': ['Python'],
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.echo',
                'params': {'string': 'Flask'},
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_echo_raise_invalid_params_error(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.echo',
                'params': 'Wrong',
            },
        )
        self.assertEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {
                        'message': 'Parameter structures are by-position (tuple, set, list) or by-name (dict): Wrong'
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            },
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': [1]},
        )
        self.assertEqual(
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
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.echo',
                'params': {'name': 2},
            },
        )
        self.assertEqual(
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
        self.assertEqual(
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

    def test_notify(self):
        rv = self.requests.post(API_URL, json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify'})
        self.assertEqual('', rv.text)
        self.assertEqual(204, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'jsonrpc': '2.0',
                'method': 'jsonrpc.notify',
                'params': ['Some string'],
            },
        )
        self.assertEqual('', rv.text)
        self.assertEqual(204, rv.status_code)

    def test_not_allow_notify(self):
        rv = self.requests.post(
            API_URL,
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.not_allow_notify'},
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notify'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.not_allow_notify',
                'params': ['Some string'],
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Not allow notify'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'jsonrpc': '2.0',
                'method': 'jsonrpc.not_allow_notify',
                'params': ['Some string'],
            },
        )
        self.assertEqual(
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

    def test_fails(self):
        rv = self.requests.post(
            API_URL,
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [2]},
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 2}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': '1',
                'jsonrpc': '2.0',
                'method': 'jsonrpc.fails',
                'params': [1],
            },
        )
        self.assertEqual(
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

    def test_strange_echo(self):
        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.strangeEcho',
            'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask'],
        }
        rv = self.requests.post(API_URL, json=data)
        self.assertEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask'],
            },
            rv.json(),
        )
        self.assertEqual(200, rv.status_code)

        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.strangeEcho',
            'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23],
        }
        rv = self.requests.post(API_URL, json=data)
        self.assertEqual(
            {
                'id': 1,
                'jsonrpc': '2.0',
                'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Default'],
            },
            rv.json(),
        )
        self.assertEqual(200, rv.status_code)

    def test_sum(self):
        data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [1, 3]}
        rv = self.requests.post(API_URL, json=data)
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 4}, rv.json())
        self.assertEqual(200, rv.status_code)

        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.sum',
            'params': [0.5, 1.5],
        }
        rv = self.requests.post(API_URL, json=data)
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 2.0}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_decorators(self):
        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.decorators',
            'params': ['Python'],
        }
        rv = self.requests.post(API_URL, json=data)
        self.assertEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'},
            rv.json(),
        )
        self.assertEqual(200, rv.status_code)

    def test_return_status_code(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.returnStatusCode',
                'params': ['OK'],
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code OK'}, rv.json())
        self.assertEqual(201, rv.status_code)

    def test_return_headers(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.returnHeaders',
                'params': ['OK'],
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Headers OK'}, rv.json())
        self.assertEqual(200, rv.status_code)
        self.assertEqual('1', rv.headers['X-JSONRPC'])

    def test_return_status_code_and_headers(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.returnStatusCodeAndHeaders',
                'params': ['OK'],
            },
        )
        self.assertEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code and Headers OK'},
            rv.json(),
        )
        self.assertEqual(400, rv.status_code)
        self.assertEqual('1', rv.headers['X-JSONRPC'])

    def test_not_validate_method(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.not_validate',
                'params': ['OK'],
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Not validate: OK'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_no_return_method(self):
        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'jsonrpc.noReturn',
                'params': [],
            },
        )
        self.assertEqual(
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

    def test_with_rcp_batch(self):
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json=[
                {
                    'id': 1,
                    'jsonrpc': '2.0',
                    'method': 'jsonrpc.greeting',
                    'params': ['Python'],
                },
                {
                    'id': 2,
                    'jsonrpc': '2.0',
                    'method': 'jsonrpc.greeting',
                    'params': ['Flask'],
                },
                {
                    'id': 3,
                    'jsonrpc': '2.0',
                    'method': 'jsonrpc.greeting',
                    'params': ['JSON-RCP'],
                },
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
                {
                    'id': 1,
                    'jsonrpc': '2.0',
                    'method': 'jsonrpc.greeting',
                    'params': ['Python'],
                },
                {'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Flask']},
                {'id': 3, 'jsonrpc': '2.0', 'params': ['Flask']},
                {
                    'id': 4,
                    'jsonrpc': '2.0',
                    'method': 'jsonrpc.greeting',
                    'params': ['JSON-RCP'],
                },
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
        self.assertEqual({'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_class(self):
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'classapp.index'})
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'greeting',
                'params': ['Python'],
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'hello',
                'params': {'name': 'Flask'},
            },
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            API_URL,
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'echo', 'params': ['Python', 1]},
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(API_URL, json={'jsonrpc': '2.0', 'method': 'notify', 'params': ['Python']})
        self.assertEqual(204, rv.status_code)

        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'fails', 'params': [13]})
        self.assertEqual(
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

    def test_system_describe(self):
        rv = self.requests.post(API_URL, json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
        json_data = rv.json()
        self.assertEqual(1, json_data['id'])
        self.assertEqual('2.0', json_data['jsonrpc'])
        self.assertEqual('Flask-JSONRPC', json_data['result']['name'])
        self.assertIsNone(json_data['result']['description'])
        self.assertEqual('2.0', json_data['result']['version'])
        self.assertIsNotNone(json_data['result']['servers'])
        self.assertEqual(
            {
                'jsonrpc.greeting': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'name',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'jsonrpc.echo': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        },
                        {
                            'name': '_some',
                            'type': 'Object',
                            'required': False,
                            'nullable': False,
                        },
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'jsonrpc.notify': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': '_string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Null'},
                    'description': None,
                },
                'jsonrpc.not_allow_notify': {
                    'type': 'method',
                    'options': {'notification': False, 'validate': True},
                    'params': [
                        {
                            'name': '_string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'jsonrpc.fails': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'n',
                            'type': 'Number',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Number'},
                    'description': None,
                },
                'jsonrpc.strangeEcho': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        },
                        {
                            'name': 'omg',
                            'type': 'Object',
                            'required': False,
                            'nullable': False,
                        },
                        {
                            'name': 'wtf',
                            'type': 'Array',
                            'required': False,
                            'nullable': False,
                        },
                        {
                            'name': 'nowai',
                            'type': 'Number',
                            'required': False,
                            'nullable': False,
                        },
                        {
                            'name': 'yeswai',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        },
                    ],
                    'returns': {'type': 'Array'},
                    'description': None,
                },
                'jsonrpc.sum': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'a',
                            'type': 'Number',
                            'required': False,
                            'nullable': False,
                        },
                        {
                            'name': 'b',
                            'type': 'Number',
                            'required': False,
                            'nullable': False,
                        },
                    ],
                    'returns': {'type': 'Number'},
                    'description': None,
                },
                'jsonrpc.decorators': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'jsonrpc.returnStatusCode': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 's',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Array'},
                    'description': None,
                },
                'jsonrpc.returnHeaders': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 's',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Array'},
                    'description': None,
                },
                'jsonrpc.returnStatusCodeAndHeaders': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 's',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Array'},
                    'description': None,
                },
                'jsonrpc.not_validate': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': False},
                    'params': [],
                    'returns': {'type': 'Null'},
                    'description': None,
                },
                'jsonrpc.noReturn': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': '_string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Null'},
                    'description': None,
                },
                'classapp.index': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'name',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'greeting': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'name',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'hello': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'name',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'echo': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        },
                        {
                            'name': '_some',
                            'type': 'Object',
                            'required': False,
                            'nullable': False,
                        },
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'notify': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': '_string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Null'},
                    'description': None,
                },
                'not_allow_notify': {
                    'type': 'method',
                    'options': {'notification': False, 'validate': True},
                    'params': [
                        {
                            'name': '_string',
                            'type': 'String',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'String'},
                    'description': None,
                },
                'fails': {
                    'type': 'method',
                    'options': {'notification': True, 'validate': True},
                    'params': [
                        {
                            'name': 'n',
                            'type': 'Number',
                            'required': False,
                            'nullable': False,
                        }
                    ],
                    'returns': {'type': 'Number'},
                    'description': None,
                },
            },
            json_data['result']['methods'],
        )

        self.assertEqual(200, rv.status_code)
