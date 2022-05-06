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
# pylint: disable=duplicate-code
from .conftest import APITestCase


class APITest(APITestCase):
    def test_greeting(self):
        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 'Flask'}}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_greeting_raise_parse_error(self):
        rv = self.requests.post(self.api_url, data={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
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
            self.api_url,
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
            self.api_url,
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
        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0'})
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
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': 'Wrong'}
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
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': [1]}
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
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': {'name': 2}}
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
        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'method-not-found'})
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
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': ['Python']}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'string': 'Flask'}}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_echo_raise_invalid_params_error(self):
        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': 'Wrong'}
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

        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': [1]})
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
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo', 'params': {'name': 2}}
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

        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.echo'})
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
        rv = self.requests.post(self.api_url, json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify'})
        self.assertEqual('', rv.text)
        self.assertEqual(204, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'jsonrpc': '2.0', 'method': 'jsonrpc.notify', 'params': ['Some string']}
        )
        self.assertEqual('', rv.text)
        self.assertEqual(204, rv.status_code)

    def test_fails(self):
        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [2]}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 2}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'id': '1', 'jsonrpc': '2.0', 'method': 'jsonrpc.fails', 'params': [1]}
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
        rv = self.requests.post(self.api_url, json=data)
        self.assertEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Flask']}, rv.json()
        )
        self.assertEqual(200, rv.status_code)

        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'method': 'jsonrpc.strangeEcho',
            'params': ['string', {'a': 1}, ['a', 'b', 'c'], 23],
        }
        rv = self.requests.post(self.api_url, json=data)
        self.assertEqual(
            {'id': 1, 'jsonrpc': '2.0', 'result': ['string', {'a': 1}, ['a', 'b', 'c'], 23, 'Default']}, rv.json()
        )
        self.assertEqual(200, rv.status_code)

    def test_sum(self):
        data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [1, 3]}
        rv = self.requests.post(self.api_url, json=data)
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 4}, rv.json())
        self.assertEqual(200, rv.status_code)

        data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.sum', 'params': [0.5, 1.5]}
        rv = self.requests.post(self.api_url, json=data)
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 2.0}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_decorators(self):
        data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.decorators', 'params': ['Python']}
        rv = self.requests.post(self.api_url, json=data)
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_return_status_code(self):
        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCode', 'params': ['OK']}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code OK'}, rv.json())
        self.assertEqual(201, rv.status_code)

    def test_return_headers(self):
        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnHeaders', 'params': ['OK']}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Headers OK'}, rv.json())
        self.assertEqual(200, rv.status_code)
        self.assertEqual('1', rv.headers['X-JSONRPC'])

    def test_return_status_code_and_headers(self):
        rv = self.requests.post(
            self.api_url,
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.returnStatusCodeAndHeaders', 'params': ['OK']},
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Status Code and Headers OK'}, rv.json())
        self.assertEqual(400, rv.status_code)
        self.assertEqual('1', rv.headers['X-JSONRPC'])

    def test_with_rcp_batch(self):
        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url,
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
            self.api_url,
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

        rv = self.requests.post(self.api_url, json={'id': 2, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting'})
        self.assertEqual({'id': 2, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

    def test_class(self):
        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'classapp.index'})
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'greeting', 'params': ['Python']}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'hello', 'params': {'name': 'Flask'}}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Flask'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(
            self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'echo', 'params': ['Python', 1]}
        )
        self.assertEqual({'id': 1, 'jsonrpc': '2.0', 'result': 'Python'}, rv.json())
        self.assertEqual(200, rv.status_code)

        rv = self.requests.post(self.api_url, json={'jsonrpc': '2.0', 'method': 'notify', 'params': ['Python']})
        self.assertEqual(204, rv.status_code)

        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'fails', 'params': [13]})
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
        rv = self.requests.post(self.api_url, json={'id': 1, 'jsonrpc': '2.0', 'method': 'system.describe'})
        json_data = rv.json()
        self.assertEqual(1, json_data['id'])
        self.assertEqual('2.0', json_data['jsonrpc'])
        self.assertEqual('Flask-JSONRPC', json_data['result']['name'])
        self.assertEqual('1.0', json_data['result']['sdversion'])
        self.assertIsNone(json_data['result']['summary'])
        self.assertEqual('2.0', json_data['result']['version'])
        self.assertEqual(
            [
                {
                    'name': 'jsonrpc.greeting',
                    'params': [{'name': 'name', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.echo',
                    'params': [{'name': 'string', 'type': 'String'}, {'name': '_some', 'type': 'Object'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.notify',
                    'params': [{'name': '_string', 'type': 'String'}],
                    'return': {'type': 'Null'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.fails',
                    'params': [{'name': 'n', 'type': 'Number'}],
                    'return': {'type': 'Number'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.strangeEcho',
                    'params': [
                        {'name': 'string', 'type': 'String'},
                        {'name': 'omg', 'type': 'Object'},
                        {'name': 'wtf', 'type': 'Array'},
                        {'name': 'nowai', 'type': 'Number'},
                        {'name': 'yeswai', 'type': 'String'},
                    ],
                    'return': {'type': 'Array'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.sum',
                    'params': [{'name': 'a', 'type': 'Number'}, {'name': 'b', 'type': 'Number'}],
                    'return': {'type': 'Number'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.decorators',
                    'params': [{'name': 'string', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.returnStatusCode',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'Array'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.returnHeaders',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'Array'},
                    'summary': None,
                },
                {
                    'name': 'jsonrpc.returnStatusCodeAndHeaders',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'Array'},
                    'summary': None,
                },
                {
                    'name': 'classapp.index',
                    'params': [{'name': 'name', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'greeting',
                    'params': [{'name': 'name', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'hello',
                    'params': [{'name': 'name', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'echo',
                    'params': [{'name': 'string', 'type': 'String'}, {'name': '_some', 'type': 'Object'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'notify',
                    'params': [{'name': '_string', 'type': 'String'}],
                    'return': {'type': 'Null'},
                    'summary': None,
                },
                {
                    'name': 'fails',
                    'params': [{'name': 'n', 'type': 'Number'}],
                    'return': {'type': 'Number'},
                    'summary': None,
                },
            ],
            json_data['result']['procs'],
        )

        self.assertEqual(200, rv.status_code)
