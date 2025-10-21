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
    'breadcrumb,method_description,method_signature,method_signature_description',
    [('decorators » decorators.decorator', '', 'decorators.decorator(string: String) -> String', '')],
)
def test_decorators_decorator_display(
    jsonrpc_page_info: t.Callable[..., Page],
    breadcrumb: str,
    method_description: str,
    method_signature: str,
    method_signature_description: str,
) -> None:
    jsonrpc_page_info(
        'decorators.decorator', breadcrumb, method_description, method_signature, method_signature_description
    )


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'World'},
            {'jsonrpc': '2.0', 'method': 'decorators.decorator', 'params': {'string': 'World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World from decorator, ;)'},
        ),
        (
            {'string': 'Test'},
            {'jsonrpc': '2.0', 'method': 'decorators.decorator', 'params': {'string': 'Test'}},
            {'jsonrpc': '2.0', 'result': 'Hello Test from decorator, ;)'},
        ),
        (
            {'string': 'Decorator'},
            {'jsonrpc': '2.0', 'method': 'decorators.decorator', 'params': {'string': 'Decorator'}},
            {'jsonrpc': '2.0', 'result': 'Hello Decorator from decorator, ;)'},
        ),
        (
            {'string': 'Python'},
            {'jsonrpc': '2.0', 'method': 'decorators.decorator', 'params': {'string': 'Python'}},
            {'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'},
        ),
        (
            {'string': ''},
            {'jsonrpc': '2.0', 'method': 'decorators.decorator', 'params': {}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'message': "jsonrpc_decorator..decorator() missing 1 required positional argument: 'string'"
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'string': 'Flask JSON-RPC'},
            {'jsonrpc': '2.0', 'method': 'decorators.decorator', 'params': {'string': 'Flask JSON-RPC'}},
            {'jsonrpc': '2.0', 'result': 'Hello Flask JSON-RPC from decorator, ;)'},
        ),
    ],
)
def test_decorators_decorator_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('decorators.decorator', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'breadcrumb,method_description,method_signature,method_signature_description',
    [('decorators » decorators.wrappedDecorator', '', 'decorators.wrappedDecorator(string: String) -> String', '')],
)
def test_decorators_wrapped_decorator_display(
    jsonrpc_page_info: t.Callable[..., Page],
    breadcrumb: str,
    method_description: str,
    method_signature: str,
    method_signature_description: str,
) -> None:
    jsonrpc_page_info(
        'decorators.wrappedDecorator', breadcrumb, method_description, method_signature, method_signature_description
    )


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'string': 'World'},
            {'jsonrpc': '2.0', 'method': 'decorators.wrappedDecorator', 'params': {'string': 'World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World from decorator, ;)'},
        ),
        (
            {'string': 'Wrapped'},
            {'jsonrpc': '2.0', 'method': 'decorators.wrappedDecorator', 'params': {'string': 'Wrapped'}},
            {'jsonrpc': '2.0', 'result': 'Hello Wrapped from decorator, ;)'},
        ),
        (
            {'string': 'Function'},
            {'jsonrpc': '2.0', 'method': 'decorators.wrappedDecorator', 'params': {'string': 'Function'}},
            {'jsonrpc': '2.0', 'result': 'Hello Function from decorator, ;)'},
        ),
        (
            {'string': 'Python Wrapped'},
            {'jsonrpc': '2.0', 'method': 'decorators.wrappedDecorator', 'params': {'string': 'Python Wrapped'}},
            {'jsonrpc': '2.0', 'result': 'Hello Python Wrapped from decorator, ;)'},
        ),
        (
            {'string': ''},
            {'jsonrpc': '2.0', 'method': 'decorators.wrappedDecorator', 'params': {}},
            {
                'error': {
                    'code': -32602,
                    'data': {'message': "wrappedDecorator() missing 1 required positional argument: 'string'"},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'string': 'Functools'},
            {'jsonrpc': '2.0', 'method': 'decorators.wrappedDecorator', 'params': {'string': 'Functools'}},
            {'jsonrpc': '2.0', 'result': 'Hello Functools from decorator, ;)'},
        ),
    ],
)
def test_decorators_wrapped_decorator_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('decorators.wrappedDecorator', test_input, request_expected, response_expected)
