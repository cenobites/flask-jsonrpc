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
    [('class_apps.index', 'class_apps.index(name: String) -> String', '')],
)
def test_class_apps_index_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('class_apps.index', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'name': ''},
            {'jsonrpc': '2.0', 'method': 'class_apps.index', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'},
        ),
        (
            {'name': 'Class User'},
            {'jsonrpc': '2.0', 'method': 'class_apps.index', 'params': {'name': 'Class User'}},
            {'jsonrpc': '2.0', 'result': 'Hello Class User'},
        ),
        (
            {'name': 'World'},
            {'jsonrpc': '2.0', 'method': 'class_apps.index', 'params': {'name': 'World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World'},
        ),
        (
            {'name': 'Python Class'},
            {'jsonrpc': '2.0', 'method': 'class_apps.index', 'params': {'name': 'Python Class'}},
            {'jsonrpc': '2.0', 'result': 'Hello Python Class'},
        ),
    ],
)
def test_class_apps_index_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('class_apps.index', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('class_apps.greeting', 'class_apps.greeting(name: String) -> String', '')],
)
def test_class_apps_greeting_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('class_apps.greeting', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'name': ''},
            {'jsonrpc': '2.0', 'method': 'class_apps.greeting', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'},
        ),
        (
            {'name': 'Class World'},
            {'jsonrpc': '2.0', 'method': 'class_apps.greeting', 'params': {'name': 'Class World'}},
            {'jsonrpc': '2.0', 'result': 'Hello Class World'},
        ),
        (
            {'name': 'Greeting'},
            {'jsonrpc': '2.0', 'method': 'class_apps.greeting', 'params': {'name': 'Greeting'}},
            {'jsonrpc': '2.0', 'result': 'Hello Greeting'},
        ),
        (
            {'name': 'Flask Class'},
            {'jsonrpc': '2.0', 'method': 'class_apps.greeting', 'params': {'name': 'Flask Class'}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask Class'},
        ),
    ],
)
def test_class_apps_greeting_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('class_apps.greeting', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('class_apps.hello', 'class_apps.hello(name: String) -> String', '')],
)
def test_class_apps_hello_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('class_apps.hello', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'name': ''},
            {'jsonrpc': '2.0', 'method': 'class_apps.hello', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC'},
        ),
        (
            {'name': 'Python'},
            {'jsonrpc': '2.0', 'method': 'class_apps.hello', 'params': {'name': 'Python'}},
            {'jsonrpc': '2.0', 'result': 'Hello Python'},
        ),
        (
            {'name': 'Class Hello'},
            {'jsonrpc': '2.0', 'method': 'class_apps.hello', 'params': {'name': 'Class Hello'}},
            {'jsonrpc': '2.0', 'result': 'Hello Class Hello'},
        ),
        (
            {'name': 'Static Method'},
            {'jsonrpc': '2.0', 'method': 'class_apps.hello', 'params': {'name': 'Static Method'}},
            {'jsonrpc': '2.0', 'result': 'Hello Static Method'},
        ),
    ],
)
def test_class_apps_hello_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('class_apps.hello', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('class_apps.echo', 'class_apps.echo(string: String, _some: Object) -> String', '')],
)
def test_class_apps_echo_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('class_apps.echo', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'Class Echo Test'},
            {'jsonrpc': '2.0', 'method': 'class_apps.echo', 'params': {'string': 'Class Echo Test'}},
            {'jsonrpc': '2.0', 'result': 'Class Echo Test'},
        ),
        (
            {'string': 'Static Echo'},
            {'jsonrpc': '2.0', 'method': 'class_apps.echo', 'params': {'string': 'Static Echo'}},
            {'jsonrpc': '2.0', 'result': 'Static Echo'},
        ),
        (
            {'string': ''},
            {'jsonrpc': '2.0', 'method': 'class_apps.echo', 'params': {}},
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
            {'jsonrpc': '2.0', 'method': 'class_apps.echo', 'params': {'string': 'Test', '_some': 'extra'}},
            {'jsonrpc': '2.0', 'result': 'Test'},
        ),
    ],
)
def test_class_apps_echo_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('class_apps.echo', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('class_apps.notify', 'class_apps.notify(_string: String) -> Null', '')],
)
def test_class_apps_notify_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('class_apps.notify', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Class Notification'},
            {'jsonrpc': '2.0', 'method': 'class_apps.notify', 'params': {'_string': 'Class Notification'}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        ({}, {'jsonrpc': '2.0', 'method': 'class_apps.notify', 'params': {}}, {'jsonrpc': '2.0', 'result': None}),
        (
            {'_string': ''},
            {'jsonrpc': '2.0', 'method': 'class_apps.notify', 'params': {}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'_string': 'Static Notify'},
            {'jsonrpc': '2.0', 'method': 'class_apps.notify', 'params': {'_string': 'Static Notify'}},
            {'jsonrpc': '2.0', 'result': None},
        ),
    ],
)
def test_class_apps_notify_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('class_apps.notify', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('class_apps.not_allow_notify', 'class_apps.not_allow_notify(_string: String) -> String', '')],
)
def test_class_apps_not_allow_notify_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('class_apps.not_allow_notify', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Not Allow Test'},
            {'jsonrpc': '2.0', 'method': 'class_apps.not_allow_notify', 'params': {'_string': 'Not Allow Test'}},
            {'jsonrpc': '2.0', 'result': 'Now allow notify'},
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'class_apps.not_allow_notify', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Now allow notify'},
        ),
        (
            {'_string': ''},
            {'jsonrpc': '2.0', 'method': 'class_apps.not_allow_notify', 'params': {}},
            {'jsonrpc': '2.0', 'result': 'Now allow notify'},
        ),
        (
            {'_string': 'Class Method'},
            {'jsonrpc': '2.0', 'method': 'class_apps.not_allow_notify', 'params': {'_string': 'Class Method'}},
            {'jsonrpc': '2.0', 'result': 'Now allow notify'},
        ),
    ],
)
def test_class_apps_not_allow_notify_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('class_apps.not_allow_notify', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('class_apps.fails', 'class_apps.fails(n: Number) -> Number', '')],
)
def test_class_apps_fails_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('class_apps.fails', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'n': 2},
            {'jsonrpc': '2.0', 'method': 'class_apps.fails', 'params': {'n': 2}},
            {'jsonrpc': '2.0', 'result': 2},
        ),
        (
            {'n': 0},
            {'jsonrpc': '2.0', 'method': 'class_apps.fails', 'params': {'n': 0}},
            {'jsonrpc': '2.0', 'result': 0},
        ),
        (
            {'n': 42},
            {'jsonrpc': '2.0', 'method': 'class_apps.fails', 'params': {'n': 42}},
            {'jsonrpc': '2.0', 'result': 42},
        ),
        (
            {'n': 1},
            {'jsonrpc': '2.0', 'method': 'class_apps.fails', 'params': {'n': 1}},
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
            {'jsonrpc': '2.0', 'method': 'class_apps.fails', 'params': {'n': 3}},
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
            {'n': 15},
            {'jsonrpc': '2.0', 'method': 'class_apps.fails', 'params': {'n': 15}},
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
def test_class_apps_fails_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('class_apps.fails', test_input, request_expected, response_expected)
