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
            API_URL,
            data=json.dumps({'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.greeting', 'params': ['Python']}),
            headers={'Content-Type': 'application/json'},
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
                    'data': {
                        'message': 'Invalid mime type for JSON: application/x-www-form-urlencoded, '
                        'use header Content-Type: application/json'
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
                    'data': {'message': 'argument "name" (int) is not an instance of str'},
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
                    'data': {'message': 'argument "name" (int) is not an instance of str'},
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
