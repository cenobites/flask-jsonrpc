# Copyright (c) 2025-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

import pytest
from playwright.sync_api import Page


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('app.echo', 'app.echo(string: String, _some: Object) -> String', '')],
)
def test_app_echo_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('app.echo', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'Hello World'},
            {'jsonrpc': '2.0', 'method': 'app.echo', 'params': {'string': 'Hello World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World'},
        ),
        (
            {'string': 'Python'},
            {'jsonrpc': '2.0', 'method': 'app.echo', 'params': {'string': 'Python'}},
            {'jsonrpc': '2.0', 'result': 'Python'},
        ),
        (
            {'string': 'Flask JSON-RPC'},
            {'jsonrpc': '2.0', 'method': 'app.echo', 'params': {'string': 'Flask JSON-RPC'}},
            {'jsonrpc': '2.0', 'result': 'Flask JSON-RPC'},
        ),
        (
            {'string': ''},
            {'jsonrpc': '2.0', 'method': 'app.echo', 'params': {}},
            {
                'error': {
                    'code': -32602,
                    'data': {'message': 'argument "string" (None) is not an instance of str'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'string': 'Test', '_some': 'extra'},
            {'jsonrpc': '2.0', 'method': 'app.echo', 'params': {'string': 'Test', '_some': 'extra'}},
            {'jsonrpc': '2.0', 'result': 'Test'},
        ),
        (
            {'string': 'Hello αβγδε 中文 🚀', '_some': 'extra'},
            {'jsonrpc': '2.0', 'method': 'app.echo', 'params': {'string': 'Hello αβγδε 中文 🚀', '_some': 'extra'}},
            {'jsonrpc': '2.0', 'result': 'Hello αβγδε 中文 🚀'},
        ),
    ],
)
def test_app_echo_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('app.echo', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description', [('app.notify', 'app.notify(_string: String) -> Null', '')]
)
def test_app_notify_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('app.notify', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test'},
            {'jsonrpc': '2.0', 'method': 'app.notify', 'params': {'_string': 'Test'}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        ({}, {'jsonrpc': '2.0', 'method': 'app.notify', 'params': {}}, {'jsonrpc': '2.0', 'result': None}),
        ({'_string': ''}, {'jsonrpc': '2.0', 'method': 'app.notify', 'params': {}}, {'jsonrpc': '2.0', 'result': None}),
        (
            {'_string': 'Notification'},
            {'jsonrpc': '2.0', 'method': 'app.notify', 'params': {'_string': 'Notification'}},
            {'jsonrpc': '2.0', 'result': None},
        ),
    ],
)
def test_app_notify_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('app.notify', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description', [('app.fails', 'app.fails(n: Number) -> Number', '')]
)
def test_app_fails_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('app.fails', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        ({'n': 2}, {'jsonrpc': '2.0', 'method': 'app.fails', 'params': {'n': 2}}, {'jsonrpc': '2.0', 'result': 2}),
        ({'n': 0}, {'jsonrpc': '2.0', 'method': 'app.fails', 'params': {'n': 0}}, {'jsonrpc': '2.0', 'result': 0}),
        ({'n': 42}, {'jsonrpc': '2.0', 'method': 'app.fails', 'params': {'n': 42}}, {'jsonrpc': '2.0', 'result': 42}),
        (
            {'n': 1},
            {'jsonrpc': '2.0', 'method': 'app.fails', 'params': {'n': 1}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'number is odd'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 3},
            {'jsonrpc': '2.0', 'method': 'app.fails', 'params': {'n': 3}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'number is odd'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 13},
            {'jsonrpc': '2.0', 'method': 'app.fails', 'params': {'n': 13}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'number is odd'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_app_fails_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('app.fails', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('app.decorators', 'app.decorators(string: String) -> String', '')],
)
def test_app_decorators_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('app.decorators', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'World'},
            {'jsonrpc': '2.0', 'method': 'app.decorators', 'params': {'string': 'World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World from decorator, ;)'},
        ),
        (
            {'string': 'Python'},
            {'jsonrpc': '2.0', 'method': 'app.decorators', 'params': {'string': 'Python'}},
            {'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'},
        ),
        (
            {'string': 'Flask'},
            {'jsonrpc': '2.0', 'method': 'app.decorators', 'params': {'string': 'Flask'}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask from decorator, ;)'},
        ),
        (
            {'string': ''},
            {'jsonrpc': '2.0', 'method': 'app.decorators', 'params': {}},
            {'error': {'code': -32602, 'message': 'Invalid params', 'name': 'InvalidParamsError'}, 'jsonrpc': '2.0'},
        ),
    ],
)
def test_app_decorators_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('app.decorators', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('app.wrappedDecorators', 'app.wrappedDecorators(string: String) -> String', '')],
)
def test_app_wrapped_decorators_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('app.wrappedDecorators', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'World'},
            {'jsonrpc': '2.0', 'method': 'app.wrappedDecorators', 'params': {'string': 'World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World from decorator, ;)'},
        ),
        (
            {'string': 'Python'},
            {'jsonrpc': '2.0', 'method': 'app.wrappedDecorators', 'params': {'string': 'Python'}},
            {'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'},
        ),
        (
            {'string': 'JSON-RPC'},
            {'jsonrpc': '2.0', 'method': 'app.wrappedDecorators', 'params': {'string': 'JSON-RPC'}},
            {'jsonrpc': '2.0', 'result': 'Hello JSON-RPC from decorator, ;)'},
        ),
        (
            {'string': ''},
            {'jsonrpc': '2.0', 'method': 'app.wrappedDecorators', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Hello None from decorator, ;)'},
        ),
    ],
)
def test_app_wrapped_decorators_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('app.wrappedDecorators', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('app.failsWithCustomException', 'app.failsWithCustomException(_string: String) -> Null', '')],
)
def test_app_fails_with_custom_exception_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('app.failsWithCustomException', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test'},
            {'jsonrpc': '2.0', 'method': 'app.failsWithCustomException', 'params': {'_string': 'Test'}},
            {
                'error': {
                    'code': -32000,
                    'data': {'code': '0001', 'message': 'It is a custom exception'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'app.failsWithCustomException', 'params': {}},
            {
                'error': {
                    'code': -32000,
                    'data': {'code': '0001', 'message': 'It is a custom exception'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'_string': 'Exception'},
            {'jsonrpc': '2.0', 'method': 'app.failsWithCustomException', 'params': {'_string': 'Exception'}},
            {
                'error': {
                    'code': -32000,
                    'data': {'code': '0001', 'message': 'It is a custom exception'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_app_fails_with_custom_exception_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('app.failsWithCustomException', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'app.failsWithCustomExceptionNotRegistered',
            'app.failsWithCustomExceptionNotRegistered(_string: String) -> Null',
            '',
        )
    ],
)
def test_app_fails_with_custom_exception_not_registered_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('app.failsWithCustomExceptionNotRegistered', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test'},
            {'jsonrpc': '2.0', 'method': 'app.failsWithCustomExceptionNotRegistered', 'params': {'_string': 'Test'}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'example of fail with custom exception that will not be handled'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'app.failsWithCustomExceptionNotRegistered', 'params': {}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'example of fail with custom exception that will not be handled'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_app_fails_with_custom_exception_not_registered_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('app.failsWithCustomExceptionNotRegistered', test_input, request_expected, response_expected)
