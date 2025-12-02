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
    [('objects.python_classes.createColor', 'objects.python_classes.createColor(color: Object) -> Object', '')],
)
def test_python_classes_create_color_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_classes.createColor', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'color': {'name': 'Red', 'tag': 'primary'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createColor',
                'params': {'color': {'name': 'Red', 'tag': 'primary'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Red', 'tag': 'primary'}},
        ),
        (
            {'color': {'name': 'Blue', 'tag': 'secondary'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createColor',
                'params': {'color': {'name': 'Blue', 'tag': 'secondary'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'secondary'}},
        ),
        (
            {'color': {'name': 'Green', 'tag': 'nature'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createColor',
                'params': {'color': {'name': 'Green', 'tag': 'nature'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Green', 'tag': 'nature'}},
        ),
        (
            {'color': {'name': 'Yellow', 'tag': 'bright'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createColor',
                'params': {'color': {'name': 'Yellow', 'tag': 'bright'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Yellow', 'tag': 'bright'}},
        ),
        (
            {'color': {'name': 'Purple', 'tag': 'royal'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createColor',
                'params': {'color': {'name': 'Purple', 'tag': 'royal'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Purple', 'tag': 'royal'}},
        ),
        (
            {'color': {'name': 'Complex Color Name with Special Characters !@#', 'tag': 'unique'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createColor',
                'params': {'color': {'name': 'Complex Color Name with Special Characters !@#', 'tag': 'unique'}},
            },
            {
                'jsonrpc': '2.0',
                'result': {'id': 1, 'name': 'Complex Color Name with Special Characters !@#', 'tag': 'unique'},
            },
        ),
    ],
)
def test_python_classes_create_color_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_classes.createColor', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'objects.python_classes.createManyColor',
            ('objects.python_classes.createManyColor(colors: Array, color: Object) -> Array'),
            '',
        )
    ],
)
def test_python_classes_create_many_color_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_classes.createManyColor', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'colors': [{'name': 'Red', 'tag': 'primary'}, {'name': 'Blue', 'tag': 'primary'}]},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyColor',
                'params': {'colors': [{'name': 'Red', 'tag': 'primary'}, {'name': 'Blue', 'tag': 'primary'}]},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Red', 'tag': 'primary'}, {'id': 1, 'name': 'Blue', 'tag': 'primary'}],
            },
        ),
        (
            {'colors': [{'name': 'Green', 'tag': 'nature'}], 'color': {'name': 'Yellow', 'tag': 'bright'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyColor',
                'params': {
                    'colors': [{'name': 'Green', 'tag': 'nature'}],
                    'color': {'name': 'Yellow', 'tag': 'bright'},
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Green', 'tag': 'nature'}, {'id': 1, 'name': 'Yellow', 'tag': 'bright'}],
            },
        ),
        (
            {'colors': []},
            {'jsonrpc': '2.0', 'method': 'objects.python_classes.createManyColor', 'params': {'colors': []}},
            {'jsonrpc': '2.0', 'result': []},
        ),
        (
            {'colors': [{'name': 'Solo', 'tag': 'single'}]},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyColor',
                'params': {'colors': [{'name': 'Solo', 'tag': 'single'}]},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 0, 'name': 'Solo', 'tag': 'single'}]},
        ),
        (
            {
                'colors': [
                    {'name': 'Orange', 'tag': 'warm'},
                    {'name': 'Violet', 'tag': 'cool'},
                    {'name': 'Indigo', 'tag': 'deep'},
                ]
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyColor',
                'params': {
                    'colors': [
                        {'name': 'Orange', 'tag': 'warm'},
                        {'name': 'Violet', 'tag': 'cool'},
                        {'name': 'Indigo', 'tag': 'deep'},
                    ]
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Orange', 'tag': 'warm'},
                    {'id': 1, 'name': 'Violet', 'tag': 'cool'},
                    {'id': 2, 'name': 'Indigo', 'tag': 'deep'},
                ],
            },
        ),
        (
            {
                'colors': [{'name': 'Base Color', 'tag': 'test'}],
                'color': {'name': 'Additional Color with Long Name', 'tag': 'special'},
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyColor',
                'params': {
                    'colors': [{'name': 'Base Color', 'tag': 'test'}],
                    'color': {'name': 'Additional Color with Long Name', 'tag': 'special'},
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Base Color', 'tag': 'test'},
                    {'id': 1, 'name': 'Additional Color with Long Name', 'tag': 'special'},
                ],
            },
        ),
    ],
)
def test_python_classes_create_many_color_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_classes.createManyColor', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'objects.python_classes.createManyFixColor',
            'objects.python_classes.createManyFixColor(colors: Object) -> Array',
            '',
        )
    ],
)
def test_python_classes_create_many_fix_color_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_classes.createManyFixColor', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'colors': {'1': {'name': 'Red', 'tag': 'primary'}, '2': {'name': 'Blue', 'tag': 'primary'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyFixColor',
                'params': {'colors': {'1': {'name': 'Red', 'tag': 'primary'}, '2': {'name': 'Blue', 'tag': 'primary'}}},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 1, 'name': 'Red', 'tag': 'primary'}, {'id': 2, 'name': 'Blue', 'tag': 'primary'}],
            },
        ),
        (
            {'colors': {'5': {'name': 'Green', 'tag': 'nature'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyFixColor',
                'params': {'colors': {'5': {'name': 'Green', 'tag': 'nature'}}},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 5, 'name': 'Green', 'tag': 'nature'}]},
        ),
        (
            {'colors': {}},
            {'jsonrpc': '2.0', 'method': 'objects.python_classes.createManyFixColor', 'params': {'colors': {}}},
            {'jsonrpc': '2.0', 'result': []},
        ),
        (
            {'colors': {'10': {'name': 'Solo Color', 'tag': 'unique'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyFixColor',
                'params': {'colors': {'10': {'name': 'Solo Color', 'tag': 'unique'}}},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 10, 'name': 'Solo Color', 'tag': 'unique'}]},
        ),
        (
            {
                'colors': {
                    '3': {'name': 'Orange', 'tag': 'warm'},
                    '7': {'name': 'Purple', 'tag': 'royal'},
                    '9': {'name': 'Cyan', 'tag': 'cool'},
                }
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyFixColor',
                'params': {
                    'colors': {
                        '3': {'name': 'Orange', 'tag': 'warm'},
                        '7': {'name': 'Purple', 'tag': 'royal'},
                        '9': {'name': 'Cyan', 'tag': 'cool'},
                    }
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 3, 'name': 'Orange', 'tag': 'warm'},
                    {'id': 7, 'name': 'Purple', 'tag': 'royal'},
                    {'id': 9, 'name': 'Cyan', 'tag': 'cool'},
                ],
            },
        ),
        (
            {'colors': {'100': {'name': 'Complex Color Name with Special Characters !@#', 'tag': 'exotic'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.createManyFixColor',
                'params': {
                    'colors': {'100': {'name': 'Complex Color Name with Special Characters !@#', 'tag': 'exotic'}}
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 100, 'name': 'Complex Color Name with Special Characters !@#', 'tag': 'exotic'}],
            },
        ),
    ],
)
def test_python_classes_create_many_fix_color_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_classes.createManyFixColor', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('objects.python_classes.removeColor', 'objects.python_classes.removeColor(color: Object) -> Object', '')],
)
def test_python_classes_remove_color_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_classes.removeColor', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'color': {'id': 5, 'name': 'Red', 'tag': 'primary'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.removeColor',
                'params': {'color': {'id': 5, 'name': 'Red', 'tag': 'primary'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 5, 'name': 'Red', 'tag': 'primary'}},
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'objects.python_classes.removeColor', 'params': {}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'color': {'id': 15, 'name': 'Error Color', 'tag': 'test'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.removeColor',
                'params': {'color': {'id': 15, 'name': 'Error Color', 'tag': 'test'}},
            },
            {
                'error': {
                    'code': -32000,
                    'data': {'color_id': 15, 'reason': 'The color with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'color': {'id': 1, 'name': 'Blue', 'tag': 'primary'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.removeColor',
                'params': {'color': {'id': 1, 'name': 'Blue', 'tag': 'primary'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Blue', 'tag': 'primary'}},
        ),
        (
            {'color': {'id': 10, 'name': 'Max ID Color', 'tag': 'limit'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.removeColor',
                'params': {'color': {'id': 10, 'name': 'Max ID Color', 'tag': 'limit'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 10, 'name': 'Max ID Color', 'tag': 'limit'}},
        ),
        (
            {'color': {'id': 50, 'name': 'High ID Color with Long Name', 'tag': 'error_test'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_classes.removeColor',
                'params': {'color': {'id': 50, 'name': 'High ID Color with Long Name', 'tag': 'error_test'}},
            },
            {
                'error': {
                    'code': -32000,
                    'data': {'color_id': 50, 'reason': 'The color with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_python_classes_remove_color_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_classes.removeColor', test_input, request_expected, response_expected)
