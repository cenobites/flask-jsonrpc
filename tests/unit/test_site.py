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

from flask import Flask

import pytest
from werkzeug.datastructures import Headers

from flask_jsonrpc.site import JSONRPCSite
from flask_jsonrpc.exceptions import ParseError


def test_site_simple() -> None:
    def view_func() -> str:
        return 'Hello world!'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}
        assert status_code == 200
        assert headers == {}


def test_site_with_request_using_list_as_params() -> None:
    def view_func(a: str, b: int, c: bool) -> str:
        return f'Params: {a}, {b}, {c}'

    view_func.jsonrpc_method_return = str
    view_func.jsonrpc_method_params = {'a': str, 'b': int, 'c': bool}

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path',
        method='POST',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': ['str', 1, True]},
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Params: str, 1, True'}
        assert status_code == 200
        assert headers == {}


def test_site_with_request_using_dict_as_params() -> None:
    def view_func(a: str, b: int, c: bool) -> str:
        return f'Params: {a}, {b}, {c}'

    view_func.jsonrpc_method_return = str
    view_func.jsonrpc_method_params = {'a': str, 'b': int, 'c': bool}

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path',
        method='POST',
        json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': {'a': 'str', 'b': 1, 'c': True}},
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Params: str, 1, True'}
        assert status_code == 200
        assert headers == {}


def test_site_with_invalid_request() -> None:
    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')

    with app.test_request_context('/base/path', method='POST', data='XXX'), pytest.raises(ParseError):
        jsonrpc_site.dispatch_request()


def test_site_with_invalid_json_request() -> None:
    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')

    with (
        app.test_request_context(
            '/base/path',
            method='POST',
            data='{"id": 1, "jsonrpc": "2.0", "method": "app.view_func", "params" []}',
            headers={'Content-Type': 'application/json'},
        ),
        pytest.raises(ParseError),
    ):
        jsonrpc_site.dispatch_request()


def test_site_with_invalid_jsonrpc_request_object() -> None:
    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')

    with app.test_request_context('/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0'}):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32600,
                'data': {'message': "Invalid JSON: {'id': 1, 'jsonrpc': '2.0'}"},
                'message': 'Invalid Request',
                'name': 'InvalidRequestError',
            },
        }
        assert status_code == 400
        assert headers == {}


def test_site_with_invalid_params() -> None:
    def view_func() -> str:
        return 'Hello world!'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': 'invalid'}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'data': {'message': 'Parameter structures are by-position (list) or by-name (dict): invalid'},
                'message': 'Invalid params',
                'name': 'InvalidParamsError',
            },
        }
        assert status_code == 400
        assert headers == {}


def test_site_with_no_view_func_registered() -> None:
    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'data': {'message': 'Method not found: app.view_func'},
                'message': 'Method not found',
                'name': 'MethodNotFoundError',
            },
        }
        assert status_code == 400
        assert headers == {}


def test_site_with_view_func_returns_response_and_status_code() -> None:
    def view_func() -> tuple[str, int]:
        return 'Hello world!', 200

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}
        assert status_code == 200
        assert headers == {}


def test_site_with_view_func_returns_response_and_headers() -> None:
    def view_func() -> tuple[str, dict[str, t.Any]]:
        return 'Hello world!', {'X-Some-Attr': 'something'}

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}
        assert status_code == 200
        assert headers == {'X-Some-Attr': 'something'}


def test_site_with_view_func_returns_response_and_status_code_and_heders() -> None:
    def view_func() -> tuple[str, int, dict[str, t.Any]]:
        return 'Hello world!', 200, {'X-Some-Attr': 'something'}

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}
        assert status_code == 200
        assert headers == {'X-Some-Attr': 'something'}


def test_site_with_batch_request() -> None:
    def view_func() -> str:
        return 'Hello world!'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path',
        method='POST',
        json=[
            {'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []},
            {'id': 2, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []},
            {'id': 3, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []},
        ],
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == [
            {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'},
            {'id': 2, 'jsonrpc': '2.0', 'result': 'Hello world!'},
            {'id': 3, 'jsonrpc': '2.0', 'result': 'Hello world!'},
        ]
        assert status_code == 200
        assert headers == Headers([])


def test_site_register_error_handler() -> None:
    def view_func() -> str:
        raise ValueError('some error')

    def value_error_handler(ex: ValueError) -> str:
        return f'Error: {ex}'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)
    jsonrpc_site.register_error_handler(ValueError, value_error_handler)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {'code': -32000, 'data': 'Error: some error', 'message': 'Server error', 'name': 'ServerError'},
        }
        assert status_code == 500
        assert headers == {}


def test_site_register_error_handler_without_a_handler() -> None:
    def view_func() -> str:
        raise ValueError('some error')

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'data': {'message': 'some error'},
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert status_code == 500
        assert headers == {}


def test_site_register_error_handler_rasing_an_except_not_registered() -> None:
    class MyException(Exception):
        pass

    def view_func() -> str:
        raise MyException('some type error')

    def value_error_handler(ex: ValueError) -> str:
        return f'Error: {ex}'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)
    jsonrpc_site.register_error_handler(ValueError, value_error_handler)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32000,
                'data': {'message': 'some type error'},
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert status_code == 500
        assert headers == {}
