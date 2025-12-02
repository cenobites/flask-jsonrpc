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
    [('jsonrpc_basic.echo', 'jsonrpc_basic.echo(string: String, _some: Object) -> String', '')],
)
def test_jsonrpc_basic_echo_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.echo', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'Hello World'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.echo', 'params': {'string': 'Hello World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World'},
        ),
        (
            {'string': 'Python'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.echo', 'params': {'string': 'Python'}},
            {'jsonrpc': '2.0', 'result': 'Python'},
        ),
        (
            {'string': 'Flask JSON-RPC'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.echo', 'params': {'string': 'Flask JSON-RPC'}},
            {'jsonrpc': '2.0', 'result': 'Flask JSON-RPC'},
        ),
        (
            {'string': ''},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.echo', 'params': {}},
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
            {'string': 'Special chars: !@#$%^&*()'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.echo', 'params': {'string': 'Special chars: !@#$%^&*()'}},
            {'jsonrpc': '2.0', 'result': 'Special chars: !@#$%^&*()'},
        ),
        (
            {'string': 'Echo Test with Multiple Words and Numbers 123'},
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.echo',
                'params': {'string': 'Echo Test with Multiple Words and Numbers 123'},
            },
            {'jsonrpc': '2.0', 'result': 'Echo Test with Multiple Words and Numbers 123'},
        ),
    ],
)
def test_jsonrpc_basic_echo_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.echo', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('jsonrpc_basic.greeting', 'jsonrpc_basic.greeting(name: String) -> String', '')],
)
def test_jsonrpc_basic_greeting_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.greeting', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'name': 'World'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.greeting', 'params': {'name': 'World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World'},
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.greeting', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'},
        ),
        (
            {'name': 'Python'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.greeting', 'params': {'name': 'Python'}},
            {'jsonrpc': '2.0', 'result': 'Hello Python'},
        ),
        (
            {'name': ''},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.greeting', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'},
        ),
        (
            {'name': 'JSON-RPC Developer'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.greeting', 'params': {'name': 'JSON-RPC Developer'}},
            {'jsonrpc': '2.0', 'result': 'Hello JSON-RPC Developer'},
        ),
        (
            {'name': 'Test User 123'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.greeting', 'params': {'name': 'Test User 123'}},
            {'jsonrpc': '2.0', 'result': 'Hello Test User 123'},
        ),
    ],
)
def test_jsonrpc_basic_greeting_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.greeting', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('jsonrpc_basic.notify', 'jsonrpc_basic.notify(_string: String) -> Null', '')],
)
def test_jsonrpc_basic_notify_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.notify', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test notification'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.notify', 'params': {'_string': 'Test notification'}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        ({}, {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.notify', 'params': {}}, {'jsonrpc': '2.0', 'result': None}),
        (
            {'_string': ''},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.notify', 'params': {}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'_string': 'Notification message'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.notify', 'params': {'_string': 'Notification message'}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'_string': 'Complex notification with special chars: !@#$%'},
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.notify',
                'params': {'_string': 'Complex notification with special chars: !@#$%'},
            },
            {'jsonrpc': '2.0', 'result': None},
        ),
    ],
)
def test_jsonrpc_basic_notify_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.notify', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('jsonrpc_basic.not_allow_notify', 'jsonrpc_basic.not_allow_notify(_string: String) -> String', '')],
)
def test_jsonrpc_basic_not_allow_notify_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.not_allow_notify', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.not_allow_notify', 'params': {'_string': 'Test'}},
            {'jsonrpc': '2.0', 'result': 'Not allow notify'},
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.not_allow_notify', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Not allow notify'},
        ),
        (
            {'_string': 'None'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.not_allow_notify', 'params': {'_string': 'None'}},
            {'jsonrpc': '2.0', 'result': 'Not allow notify'},
        ),
        (
            {'_string': ''},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.not_allow_notify', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Not allow notify'},
        ),
        (
            {'_string': 'Different input'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.not_allow_notify', 'params': {'_string': 'Different input'}},
            {'jsonrpc': '2.0', 'result': 'Not allow notify'},
        ),
        (
            {'_string': 'No notification allowed test'},
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.not_allow_notify',
                'params': {'_string': 'No notification allowed test'},
            },
            {'jsonrpc': '2.0', 'result': 'Not allow notify'},
        ),
    ],
)
def test_jsonrpc_basic_not_allow_notify_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.not_allow_notify', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('jsonrpc_basic.fails', 'jsonrpc_basic.fails(n: Number) -> Number', '')],
)
def test_jsonrpc_basic_fails_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.fails', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'n': 2},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.fails', 'params': {'n': 2}},
            {'jsonrpc': '2.0', 'result': 2},
        ),
        (
            {'n': 4},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.fails', 'params': {'n': 4}},
            {'jsonrpc': '2.0', 'result': 4},
        ),
        (
            {'n': 1},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.fails', 'params': {'n': 1}},
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
            {'n': 0},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.fails', 'params': {'n': 0}},
            {'jsonrpc': '2.0', 'result': 0},
        ),
        (
            {'n': 3},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.fails', 'params': {'n': 3}},
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
            {'n': 100},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.fails', 'params': {'n': 100}},
            {'jsonrpc': '2.0', 'result': 100},
        ),
    ],
)
def test_jsonrpc_basic_fails_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.fails', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('jsonrpc_basic.sum', 'jsonrpc_basic.sum(a: Number, b: Number) -> Number', '')],
)
def test_jsonrpc_basic_sum_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.sum', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'a': 1.0, 'b': 2.0},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.sum', 'params': {'a': 1.0, 'b': 2.0}},
            {'jsonrpc': '2.0', 'result': 3.0},
        ),
        (
            {'a': 0.0, 'b': 0.0},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.sum', 'params': {'a': 0.0, 'b': 0.0}},
            {'jsonrpc': '2.0', 'result': 0.0},
        ),
        (
            {'a': -1.5, 'b': 2.5},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.sum', 'params': {'a': -1.5, 'b': 2.5}},
            {'jsonrpc': '2.0', 'result': 1.0},
        ),
        (
            {'a': 10.25, 'b': 5.75},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.sum', 'params': {'a': 10.25, 'b': 5.75}},
            {'jsonrpc': '2.0', 'result': 16.0},
        ),
        (
            {'a': 100.0, 'b': -50.0},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.sum', 'params': {'a': 100.0, 'b': -50.0}},
            {'jsonrpc': '2.0', 'result': 50.0},
        ),
        (
            {'a': 3.14159, 'b': 2.71828},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.sum', 'params': {'a': 3.14159, 'b': 2.71828}},
            {'jsonrpc': '2.0', 'result': 5.85987},
        ),
    ],
)
def test_jsonrpc_basic_sum_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.sum', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'jsonrpc_basic.strangeEcho',
            (
                'jsonrpc_basic.strangeEcho(string: String, omg: Object, wtf: Array, '
                'nowai: Number, yeswai: String) -> Array'
            ),
            '',
        )
    ],
)
def test_jsonrpc_basic_strange_echo_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.strangeEcho', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'test', 'omg': {'key': 'value'}, 'wtf': ['item1', 'item2'], 'nowai': 42},
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.strangeEcho',
                'params': {'string': 'test', 'omg': {'key': 'value'}, 'wtf': ['item1', 'item2'], 'nowai': 42},
            },
            {'jsonrpc': '2.0', 'result': ['test', {'key': 'value'}, ['item1', 'item2'], 42, 'Default']},
        ),
        (
            {
                'string': 'hello',
                'omg': {'name': 'test', 'id': 1},
                'wtf': ['a', 'b', 'c'],
                'nowai': 123,
                'yeswai': 'Custom',
            },
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.strangeEcho',
                'params': {
                    'string': 'hello',
                    'omg': {'name': 'test', 'id': 1},
                    'wtf': ['a', 'b', 'c'],
                    'nowai': 123,
                    'yeswai': 'Custom',
                },
            },
            {'jsonrpc': '2.0', 'result': ['hello', {'name': 'test', 'id': 1}, ['a', 'b', 'c'], 123, 'Custom']},
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.strangeEcho', 'params': {}},
            {
                'error': {
                    'code': -32602,
                    'data': {'message': ('argument "string" (None) is not an instance of str')},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'string': 'complex', 'omg': {'nested': {'deep': 'value'}}, 'wtf': ['x', 'y'], 'nowai': -1},
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.strangeEcho',
                'params': {'string': 'complex', 'omg': {'nested': {'deep': 'value'}}, 'wtf': ['x', 'y'], 'nowai': -1},
            },
            {'jsonrpc': '2.0', 'result': ['complex', {'nested': {'deep': 'value'}}, ['x', 'y'], -1, 'Default']},
        ),
        (
            {'string': 'test2', 'omg': {'bool': 'true'}, 'wtf': ['single'], 'nowai': 999, 'yeswai': ''},
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.strangeEcho',
                'params': {'string': 'test2', 'omg': {'bool': 'true'}, 'wtf': ['single'], 'nowai': 999},
            },
            {'jsonrpc': '2.0', 'result': ['test2', {'bool': 'true'}, ['single'], 999, 'Default']},
        ),
        (
            {
                'string': 'comprehensive test',
                'omg': {'multiple': 'keys', 'number': 42, 'array': [1, 2, 3]},
                'wtf': ['alpha', 'beta', 'gamma', 'delta'],
                'nowai': 2024,
                'yeswai': 'Complete test case',
            },
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.strangeEcho',
                'params': {
                    'string': 'comprehensive test',
                    'omg': {'multiple': 'keys', 'number': 42, 'array': [1, 2, 3]},
                    'wtf': ['alpha', 'beta', 'gamma', 'delta'],
                    'nowai': 2024,
                    'yeswai': 'Complete test case',
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    'comprehensive test',
                    {'multiple': 'keys', 'number': 42, 'array': [1, 2, 3]},
                    ['alpha', 'beta', 'gamma', 'delta'],
                    2024,
                    'Complete test case',
                ],
            },
        ),
    ],
)
def test_jsonrpc_basic_strange_echo_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.strangeEcho', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('jsonrpc_basic.noReturn', 'jsonrpc_basic.noReturn(_string: String) -> Null', '')],
)
def test_jsonrpc_basic_no_return_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('jsonrpc_basic.noReturn', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.noReturn', 'params': {'_string': 'Test'}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'no return'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.noReturn', 'params': {}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'no return'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'_string': ''},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.noReturn', 'params': {}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'no return'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'_string': 'Error test'},
            {'jsonrpc': '2.0', 'method': 'jsonrpc_basic.noReturn', 'params': {'_string': 'Error test'}},
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'no return'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'_string': 'No return function test with long string'},
            {
                'jsonrpc': '2.0',
                'method': 'jsonrpc_basic.noReturn',
                'params': {'_string': 'No return function test with long string'},
            },
            {
                'error': {
                    'code': -32000,
                    'data': {'message': 'no return'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_jsonrpc_basic_no_return_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('jsonrpc_basic.noReturn', test_input, request_expected, response_expected)
