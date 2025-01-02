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
from unittest import mock

from flask import Flask

import pytest
from werkzeug.datastructures import Headers

from flask_jsonrpc.site import JSONRPCSite
from flask_jsonrpc.types import AnnotatedMetadataTypeError
from flask_jsonrpc.exceptions import ParseError, InvalidRequestError


def test_site_simple() -> None:
    def view_func() -> str:
        return 'Hello world!'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    assert jsonrpc_site.path == '/path'
    assert jsonrpc_site.base_url == '/base'

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}
        assert status_code == 200
        assert headers == {}


def test_site_with_view_func_to_not_be_validated() -> None:
    def view_func() -> str:
        return 'Hello world!'

    view_func.jsonrpc_validate = False

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    assert jsonrpc_site.path == '/path'
    assert jsonrpc_site.base_url == '/base'

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
    jsonrpc_site = JSONRPCSite(version='1.0.0')
    jsonrpc_site.register('app.view_func', view_func=view_func)
    jsonrpc_site.set_path('/path')
    jsonrpc_site.set_base_url('/base')

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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')

    with app.test_request_context('/base/path', method='POST', data='XXX'), pytest.raises(ParseError):
        jsonrpc_site.dispatch_request()


def test_site_with_invalid_json_request() -> None:
    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')

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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')

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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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


def test_site_with_view_func_not_allowed_notification() -> None:
    def view_func(name: str) -> str:
        return f'Hello world {name}!'

    view_func.jsonrpc_validate = True
    view_func.jsonrpc_notification = False
    view_func.jsonrpc_method_params = {'name': str}
    view_func.jsonrpc_method_return = str

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'jsonrpc': '2.0', 'method': 'app.view_func', 'params': ['Lou']}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': None,
            'jsonrpc': '2.0',
            'error': {
                'code': -32600,
                'data': {
                    'message': "The method 'app.view_func' doesn't allow"
                    " Notification Request object (without an 'id' member)"
                },
                'message': 'Invalid Request',
                'name': 'InvalidRequestError',
            },
        }
        assert status_code == 400
        assert headers == {}


def test_site_with_no_view_func_registered() -> None:
    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')

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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': []}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}
        assert status_code == 200
        assert headers == {'X-Some-Attr': 'something'}


def test_site_with_view_func_returns_with_invalid_unpack_tuple() -> None:
    def view_func() -> tuple[str, int, dict[str, t.Any], int]:
        return 'Hello world!', 200, {'X-Some-Attr': 'something'}, -32000

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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
                'data': {
                    'message': 'the view function did not return a valid response tuple. The '
                    'tuple must have the form (body, status, headers), (body, status), '
                    'or (body, headers).'
                },
                'message': 'Server error',
                'name': 'ServerError',
            },
        }
        assert status_code == 500
        assert headers == {}


def test_site_with_batch_request() -> None:
    def view_func() -> str:
        return 'Hello world!'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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


def test_site_with_batch_request_with_one_none_response() -> None:
    def view_func(n: int) -> t.Optional[str]:
        if n > 5:
            return None
        return 'Hello world!'

    view_func.jsonrpc_method_params = {'n': int}
    view_func.jsonrpc_method_return = t.Optional[str]

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path',
        method='POST',
        json=[
            {'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': [1]},
            {'id': 2, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': [6]},
            {'id': 3, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': [3]},
        ],
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == [
            {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'},
            {'id': 2, 'jsonrpc': '2.0', 'result': None},
            {'id': 3, 'jsonrpc': '2.0', 'result': 'Hello world!'},
        ]
        assert status_code == 200
        assert headers == Headers([])


def test_site_with_batch_request_notification() -> None:
    def view_func(n: int) -> t.Optional[str]:
        return None

    view_func.jsonrpc_method_params = {'n': int}
    view_func.jsonrpc_method_return = t.Optional[str]

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path',
        method='POST',
        json=[
            {'jsonrpc': '2.0', 'method': 'app.view_func', 'params': [1]},
            {'jsonrpc': '2.0', 'method': 'app.view_func', 'params': [6]},
            {'jsonrpc': '2.0', 'method': 'app.view_func', 'params': [3]},
        ],
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == []
        assert status_code == 204
        assert headers == Headers([])


def test_site_with_batch_request_empty_raises_exc() -> None:
    def view_func() -> str:
        return 'Hello world!'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context('/base/path', method='POST', json=[]), pytest.raises(InvalidRequestError):
        jsonrpc_site.dispatch_request()


def test_site_register_error_handler() -> None:
    def view_func() -> str:
        raise ValueError('some error')

    def value_error_handler(ex: ValueError) -> str:
        return f'Error: {ex}'

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
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


def test_site_with_view_func_params_annotated() -> None:
    def view_func(
        name: t.Annotated[str, 'documentation of name parameter'],
    ) -> t.Annotated[str, 'documentation of return']:
        return f'Hello world {name}!'

    view_func.jsonrpc_method_params = {'name': t.Annotated[str, 'documentation of name parameter']}
    view_func.jsonrpc_method_return = t.Annotated[str, 'documentation of return']

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': ['Lou']}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world Lou!'}
        assert status_code == 200
        assert headers == {}


def test_site_with_view_func_params_annotated_raises_exc() -> None:
    def view_func(
        name: t.Annotated[str, 'documentation of name parameter'],
    ) -> t.Annotated[str, 'documentation of return']:
        return f'Hello world {name}!'

    view_func.jsonrpc_validate = True
    view_func.jsonrpc_method_params = {'name': t.Annotated[str, 'documentation of name parameter']}
    view_func.jsonrpc_method_return = t.Annotated[str, 'documentation of return']

    mock_type_checker = mock.MagicMock()
    mock_type_checker.side_effect = AnnotatedMetadataTypeError(
        t.Annotated[str, 'documentation of name parameter'], 'name', 'Lou', 'reason error'
    )

    with mock.patch('flask_jsonrpc.site.type_checker', mock_type_checker):
        app = Flask('site')
        jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
        jsonrpc_site.register('app.view_func', view_func=view_func)

        with app.test_request_context(
            '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': ['Lou']}
        ):
            rv, status_code, headers = jsonrpc_site.dispatch_request()
            assert rv == {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': '_AnnotatedAlias',
                        'message': 'reason error',
                        'param': 'name',
                        'value': 'Lou',
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            }
            assert status_code == 400
            assert headers == {}


def test_site_with_view_func_return_raises_exc() -> None:
    def view_func(name: str) -> None:
        return f'Hello world {name}!'

    view_func.jsonrpc_validate = True
    view_func.jsonrpc_method_params = {'name': str}
    view_func.jsonrpc_method_return = None

    app = Flask('site')
    jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
    jsonrpc_site.register('app.view_func', view_func=view_func)

    with app.test_request_context(
        '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': ['Lou']}
    ):
        rv, status_code, headers = jsonrpc_site.dispatch_request()
        assert rv == {
            'id': 1,
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'data': {'message': 'return type of str must be a type; got NoneType instead'},
                'message': 'Invalid params',
                'name': 'InvalidParamsError',
            },
        }
        assert status_code == 400
        assert headers == {}


def test_site_with_view_func_return_annotated_raises_exc() -> None:
    def view_func(
        name: t.Annotated[str, 'documentation of name parameter'],
    ) -> t.Annotated[str, 'documentation of return']:
        return f'Hello world {name}!'

    view_func.jsonrpc_validate = True
    view_func.jsonrpc_method_params = {'name': t.Annotated[str, 'documentation of name parameter']}
    view_func.jsonrpc_method_return = t.Annotated[str, 'documentation of return']

    mock_type_checker = mock.MagicMock()
    mock_type_checker.side_effect = AnnotatedMetadataTypeError(
        t.Annotated[str, 'documentation of return'], 'return', 'Hello world Lou!', 'reason error'
    )

    with mock.patch('flask_jsonrpc.site.type_checker', mock_type_checker):
        app = Flask('site')
        jsonrpc_site = JSONRPCSite(version='1.0.0', path='/path', base_url='/base')
        jsonrpc_site.register('app.view_func', view_func=view_func)

        with app.test_request_context(
            '/base/path', method='POST', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.view_func', 'params': ['Lou']}
        ):
            rv, status_code, headers = jsonrpc_site.dispatch_request()
            assert rv == {
                'id': 1,
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': '_AnnotatedAlias',
                        'message': 'reason error',
                        'param': 'return',
                        'value': 'Hello world Lou!',
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
            }
            assert status_code == 400
            assert headers == {}
