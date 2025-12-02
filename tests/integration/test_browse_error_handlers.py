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
    [
        (
            'error_handlers.failsWithCustomException',
            'error_handlers.failsWithCustomException(_string: String) -> Null',
            '',
        )
    ],
)
def test_error_handlers_fails_with_custom_exception_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('error_handlers.failsWithCustomException', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test'},
            {'jsonrpc': '2.0', 'method': 'error_handlers.failsWithCustomException', 'params': {'_string': 'Test'}},
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
            {'jsonrpc': '2.0', 'method': 'error_handlers.failsWithCustomException', 'params': {}},
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
            {'jsonrpc': '2.0', 'method': 'error_handlers.failsWithCustomException', 'params': {'_string': 'Exception'}},
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
            {'_string': 'Custom Exception Handler Test'},
            {
                'jsonrpc': '2.0',
                'method': 'error_handlers.failsWithCustomException',
                'params': {'_string': 'Custom Exception Handler Test'},
            },
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
def test_error_handlers_fails_with_custom_exception_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('error_handlers.failsWithCustomException', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'error_handlers.failsWithCustomExceptionNotRegistered',
            'error_handlers.failsWithCustomExceptionNotRegistered(_string: String) -> Null',
            '',
        )
    ],
)
def test_error_handlers_fails_with_custom_exception_not_registered_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info(
        'error_handlers.failsWithCustomExceptionNotRegistered', method_title, method_signature, method_description
    )


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'_string': 'Test'},
            {
                'jsonrpc': '2.0',
                'method': 'error_handlers.failsWithCustomExceptionNotRegistered',
                'params': {'_string': 'Test'},
            },
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
            {'jsonrpc': '2.0', 'method': 'error_handlers.failsWithCustomExceptionNotRegistered', 'params': {}},
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
            {'_string': 'Unhandled'},
            {
                'jsonrpc': '2.0',
                'method': 'error_handlers.failsWithCustomExceptionNotRegistered',
                'params': {'_string': 'Unhandled'},
            },
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
            {'_string': 'Unregistered Exception Handler Test'},
            {
                'jsonrpc': '2.0',
                'method': 'error_handlers.failsWithCustomExceptionNotRegistered',
                'params': {'_string': 'Unregistered Exception Handler Test'},
            },
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
def test_error_handlers_fails_with_custom_exception_not_registered_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call(
        'error_handlers.failsWithCustomExceptionNotRegistered', test_input, request_expected, response_expected
    )
