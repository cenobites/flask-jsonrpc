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
    [('types.python_stds_annotated.boolType', 'types.python_stds_annotated.boolType(yes*: Boolean) -> Boolean', '')],
)
def test_types_python_stds_bool_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.boolType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'yes': True},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.boolType', 'params': {'yes': True}},
            {'jsonrpc': '2.0', 'result': True},
        ),
        (
            {'yes': False},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.boolType', 'params': {'yes': False}},
            {'jsonrpc': '2.0', 'result': False},
        ),
    ],
)
def test_types_python_stds_bool_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.boolType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.strType', 'types.python_stds_annotated.strType(st*: String) -> String', '')],
)
def test_types_python_stds_str_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.strType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'st': 'Hello World'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.strType', 'params': {'st': 'Hello World'}},
            {'jsonrpc': '2.0', 'result': 'Hello World'},
        ),
        (
            {'st': 'Test String'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.strType', 'params': {'st': 'Test String'}},
            {'jsonrpc': '2.0', 'result': 'Test String'},
        ),
        (
            {'st': ''},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.strType', 'params': {}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Required',
                        'message': "cannot apply constraint Required for parameter 'st' to value None with type : "
                        "ensure the value of the parameter 'st' is not empty.",
                        'param': 'st',
                        'value': None,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'st': 'String with Numbers 123 and Special Characters !@#$%'},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.strType',
                'params': {'st': 'String with Numbers 123 and Special Characters !@#$%'},
            },
            {'jsonrpc': '2.0', 'result': 'String with Numbers 123 and Special Characters !@#$%'},
        ),
        (
            {'st': 'Unicode test: αβγδε 中文 🚀'},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.strType',
                'params': {'st': 'Unicode test: αβγδε 中文 🚀'},
            },
            {'jsonrpc': '2.0', 'result': 'Unicode test: αβγδε 中文 🚀'},
        ),
        (
            {'st': 'Multi\nline\nstring\twith\ttabs'},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.strType',
                'params': {'st': 'Multi line string\twith\ttabs'},
            },
            {'jsonrpc': '2.0', 'result': 'Multi line string\twith\ttabs'},
        ),
    ],
)
def test_types_python_stds_str_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.strType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.intType', 'types.python_stds_annotated.intType(n*: Number) -> Number', '')],
)
def test_types_python_stds_int_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.intType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'n': 123},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intType', 'params': {'n': 123}},
            {'jsonrpc': '2.0', 'result': 123},
        ),
        (
            {'n': -456},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intType', 'params': {'n': -456}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Minimum',
                        'message': "cannot apply constraint Minimum for parameter 'n' to value -456 with type : "
                        "ensure the value of the parameter 'n' is greater than or equal to 0.",
                        'param': 'n',
                        'value': -456,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 0},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intType', 'params': {'n': 0}},
            {'jsonrpc': '2.0', 'result': 0},
        ),
        (
            {'n': 99999},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intType', 'params': {'n': 99999}},
            {'jsonrpc': '2.0', 'result': 99999},
        ),
        (
            {'n': -99999},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intType', 'params': {'n': -99999}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Minimum',
                        'message': "cannot apply constraint Minimum for parameter 'n' to value -99999 with type : "
                        "ensure the value of the parameter 'n' is greater than or equal to 0.",
                        'param': 'n',
                        'value': -99999,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 1},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intType', 'params': {'n': 1}},
            {'jsonrpc': '2.0', 'result': 1},
        ),
    ],
)
def test_types_python_stds_int_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.intType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.floatType', 'types.python_stds_annotated.floatType(n*: Number) -> Number', '')],
)
def test_types_python_stds_float_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.floatType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'n': 3.14},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.floatType', 'params': {'n': 3.14}},
            {'jsonrpc': '2.0', 'result': 3.14},
        ),
        (
            {'n': -2.718},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.floatType', 'params': {'n': -2.718}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'DecimalPlaces',
                        'message': "cannot apply constraint DecimalPlaces for parameter 'n' to "
                        "value -2.718 with type : ensure the value of the parameter 'n' has a maximum "
                        'of 2 decimal places.',
                        'param': 'n',
                        'value': -2.718,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 0.0},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.floatType', 'params': {'n': 0.0}},
            {'jsonrpc': '2.0', 'result': 0.0},
        ),
        (
            {'n': 1.2345678901234567},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.floatType', 'params': {'n': 1.2345678901234567}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'DecimalPlaces',
                        'message': "cannot apply constraint DecimalPlaces for parameter 'n' to value "
                        "1.2345678901234567 with type : ensure the value of the parameter 'n' has a maximum "
                        'of 2 decimal places.',
                        'param': 'n',
                        'value': 1.2345678901234567,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': -9.876543210987654},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.floatType', 'params': {'n': -9.876543210987654}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'DecimalPlaces',
                        'message': "cannot apply constraint DecimalPlaces for parameter 'n' to value -9.876543210987654"
                        " with type : ensure the value of the parameter 'n' has a maximum of 2 decimal places.",
                        'param': 'n',
                        'value': -9.876543210987654,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 1.0000000000000002},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.floatType', 'params': {'n': 1.0000000000000002}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'DecimalPlaces',
                        'message': "cannot apply constraint DecimalPlaces for parameter 'n' to value 1.0000000000000002"
                        " with type : ensure the value of the parameter 'n' has a maximum of 2 decimal places.",
                        'param': 'n',
                        'value': 1.0000000000000002,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_types_python_stds_float_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.floatType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.listType', 'types.python_stds_annotated.listType(lst*: Array) -> Array', '')],
)
def test_types_python_stds_list_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.listType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'lst': [1, 2, 3]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.listType', 'params': {'lst': [1, 2, 3]}},
            {'jsonrpc': '2.0', 'result': [1, 2, 3]},
        ),
        (
            {'lst': ['a', 'b', 'c']},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.listType', 'params': {'lst': ['a', 'b', 'c']}},
            {
                'error': {
                    'code': -32602,
                    'data': {'message': 'item 0 of argument "lst" (list) is not an instance of int'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'lst': []},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.listType', 'params': {'lst': []}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Required',
                        'message': "cannot apply constraint Required for parameter 'lst' to value [] with type : "
                        "ensure the value of the parameter 'lst' is not empty.",
                        'param': 'lst',
                        'value': [],
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'lst': [1, 'mixed', 3.14, True, None]},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.listType',
                'params': {'lst': [1, 'mixed', 3.14, True, None]},
            },
            {'jsonrpc': '2.0', 'result': [1, 'mixed', 3.14, True, None]},
        ),
        (
            {'lst': [[1, 2], [3, 4], [5, 6]]},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.listType',
                'params': {'lst': [[1, 2], [3, 4], [5, 6]]},
            },
            {
                'error': {
                    'code': -32602,
                    'data': {'message': 'item 0 of argument "lst" (list) is not an instance of int'},
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'lst': list(range(10))},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.listType',
                'params': {'lst': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
            },
            {'jsonrpc': '2.0', 'result': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
        ),
    ],
)
def test_types_python_stds_list_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.listType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.dictType', 'types.python_stds_annotated.dictType(d*: Object) -> Object', '')],
)
def test_types_python_stds_dict_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.dictType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'d': {'key1': 1, 'key2': 2}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.dictType',
                'params': {'d': {'key1': 1, 'key2': 2}},
            },
            {'jsonrpc': '2.0', 'result': {'key1': 1, 'key2': 2}},
        ),
        (
            {'d': {}},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.dictType', 'params': {'d': {}}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Required',
                        'message': "cannot apply constraint Required for parameter 'd' to value {} with type : "
                        "ensure the value of the parameter 'd' is not empty.",
                        'param': 'd',
                        'value': {},
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'d': {'test': 42}},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.dictType', 'params': {'d': {'test': 42}}},
            {'jsonrpc': '2.0', 'result': {'test': 42}},
        ),
        (
            {'d': {'a': 100, 'b': 200, 'c': 300}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.dictType',
                'params': {'d': {'a': 100, 'b': 200, 'c': 300}},
            },
            {'jsonrpc': '2.0', 'result': {'a': 100, 'b': 200, 'c': 300}},
        ),
        (
            {'d': {'single': 999}},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.dictType', 'params': {'d': {'single': 999}}},
            {'jsonrpc': '2.0', 'result': {'single': 999}},
        ),
        (
            {'d': {'negative': -123, 'zero': 0, 'positive': 456}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.dictType',
                'params': {'d': {'negative': -123, 'zero': 0, 'positive': 456}},
            },
            {'jsonrpc': '2.0', 'result': {'negative': -123, 'zero': 0, 'positive': 456}},
        ),
    ],
)
def test_types_python_stds_dict_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.dictType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.bytesType', 'types.python_stds_annotated.bytesType(b*: String) -> String', '')],
)
def test_types_python_bytes_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.bytesType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'b': 'Hello'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytesType', 'params': {'b': 'Hello'}},
            {'jsonrpc': '2.0', 'result': 'Hello'},
        ),
        (
            {'b': 'World'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytesType', 'params': {'b': 'World'}},
            {'jsonrpc': '2.0', 'result': 'World'},
        ),
        (
            {'b': ''},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytesType', 'params': {}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Required',
                        'message': "cannot apply constraint Required for parameter 'b' to value None with type : "
                        "ensure the value of the parameter 'b' is not empty.",
                        'param': 'b',
                        'value': None,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'b': 'Test bytes with special chars !@#$%'},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.bytesType',
                'params': {'b': 'Test bytes with special chars !@#$%'},
            },
            {'jsonrpc': '2.0', 'result': 'Test bytes with special chars !@#$%'},
        ),
        (
            {'b': 'Binary data 123'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytesType', 'params': {'b': 'Binary data 123'}},
            {'jsonrpc': '2.0', 'result': 'Binary data 123'},
        ),
        (
            {'b': 'UTF-8 test'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytesType', 'params': {'b': 'UTF-8 test'}},
            {'jsonrpc': '2.0', 'result': 'UTF-8 test'},
        ),
    ],
)
def test_types_python_bytes_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.bytesType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'types.python_stds_annotated.bytearrayType',
            'types.python_stds_annotated.bytearrayType(b*: String) -> String',
            '',
        )
    ],
)
def test_types_python_bytearray_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.bytearrayType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'b': 'Hello'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytearrayType', 'params': {'b': 'Hello'}},
            {'jsonrpc': '2.0', 'result': 'Hello'},
        ),
        (
            {'b': 'Bytearray test'},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.bytearrayType',
                'params': {'b': 'Bytearray test'},
            },
            {'jsonrpc': '2.0', 'result': 'Bytearray test'},
        ),
        (
            {'b': ''},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytearrayType', 'params': {}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Required',
                        'message': "cannot apply constraint Required for parameter 'b' to value None with type : "
                        "ensure the value of the parameter 'b' is not empty.",
                        'param': 'b',
                        'value': None,
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'b': 'Mutable bytes'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytearrayType', 'params': {'b': 'Mutable bytes'}},
            {'jsonrpc': '2.0', 'result': 'Mutable bytes'},
        ),
        (
            {'b': 'Array of bytes 456'},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.bytearrayType',
                'params': {'b': 'Array of bytes 456'},
            },
            {'jsonrpc': '2.0', 'result': 'Array of bytes 456'},
        ),
        (
            {'b': 'Modified buffer'},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.bytearrayType',
                'params': {'b': 'Modified buffer'},
            },
            {'jsonrpc': '2.0', 'result': 'Modified buffer'},
        ),
    ],
)
def test_types_python_bytearray_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.bytearrayType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.intEnumType', 'types.python_stds_annotated.intEnumType(e*: Object) -> Object', '')],
)
def test_types_python_int_enum_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.intEnumType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'e': 1},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intEnumType', 'params': {'e': 1}},
            {'jsonrpc': '2.0', 'result': 1},
        ),
        (
            {'e': 2},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intEnumType', 'params': {'e': 2}},
            {'jsonrpc': '2.0', 'result': 2},
        ),
        (
            {'e': 3},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intEnumType', 'params': {'e': 3}},
            {'jsonrpc': '2.0', 'result': 3},
        ),
        (
            {'e': 1},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intEnumType', 'params': {'e': 1}},
            {'jsonrpc': '2.0', 'result': 1},
        ),
        (
            {'e': 2},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intEnumType', 'params': {'e': 2}},
            {'jsonrpc': '2.0', 'result': 2},
        ),
        (
            {'e': 3},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intEnumType', 'params': {'e': 3}},
            {'jsonrpc': '2.0', 'result': 3},
        ),
    ],
)
def test_types_python_int_enum_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.intEnumType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.decimalType', 'types.python_stds_annotated.decimalType(n*: Number) -> Number', '')],
)
def test_types_python_decimal_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.decimalType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'n': 1.5},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': {'n': 1.5}},
            {'jsonrpc': '2.0', 'result': '1.5'},
        ),
        (
            {'n': 3.14},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': {'n': 3.14}},
            {'jsonrpc': '2.0', 'result': '3.14'},
        ),
        (
            {'n': 0.00},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': {'n': 0.00}},
            {'jsonrpc': '2.0', 'result': '0'},
        ),
        (
            {'n': -2.75},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': {'n': -2.75}},
            {'jsonrpc': '2.0', 'result': '-2.75'},
        ),
        (
            {'n': 99.99},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': {'n': 99.99}},
            {'jsonrpc': '2.0', 'result': '99.99'},
        ),
        (
            {'n': 123.45},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': {'n': 123.45}},
            {'jsonrpc': '2.0', 'result': '123.45'},
        ),
        (
            {'n': 123.456},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': {'n': 123.456}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'DecimalPlaces',
                        'message': "cannot apply constraint DecimalPlaces for parameter 'n' to value "
                        '123.456 with type : ensure the value '
                        "of the parameter 'n' has a maximum of 2 decimal places.",
                        'param': 'n',
                        'value': '123.456',
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_types_python_decimal_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.decimalType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.tupleType', 'types.python_stds_annotated.tupleType(tn*: Array) -> Array', '')],
)
def test_types_python_tuple_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.tupleType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'tn': [1, 2]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.tupleType', 'params': {'tn': [1, 2]}},
            {'jsonrpc': '2.0', 'result': [1, 2]},
        ),
        (
            {'tn': [3, 4]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.tupleType', 'params': {'tn': [3, 4]}},
            {'jsonrpc': '2.0', 'result': [3, 4]},
        ),
        (
            {'tn': [0, 0]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.tupleType', 'params': {'tn': [0, 0]}},
            {'jsonrpc': '2.0', 'result': [0, 0]},
        ),
        (
            {'tn': [10, 20]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.tupleType', 'params': {'tn': [10, 20]}},
            {'jsonrpc': '2.0', 'result': [10, 20]},
        ),
        (
            {'tn': [-5, 15]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.tupleType', 'params': {'tn': [-5, 15]}},
            {'jsonrpc': '2.0', 'result': [-5, 15]},
        ),
        (
            {'tn': [100, 200]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.tupleType', 'params': {'tn': [100, 200]}},
            {'jsonrpc': '2.0', 'result': [100, 200]},
        ),
    ],
)
def test_types_python_tuple_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.tupleType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'types.python_stds_annotated.namedtupleType',
            'types.python_stds_annotated.namedtupleType(tn*: Object) -> Array',
            '',
        )
    ],
)
def test_types_python_namedtuple_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.namedtupleType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'tn': {'name': 'Alice', 'id': 1}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.namedtupleType',
                'params': {'tn': {'name': 'Alice', 'id': 1}},
            },
            {'jsonrpc': '2.0', 'result': ['Alice', 1]},
        ),
        (
            {'tn': {'name': 'Bob', 'id': 2}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.namedtupleType',
                'params': {'tn': {'name': 'Bob', 'id': 2}},
            },
            {'jsonrpc': '2.0', 'result': ['Bob', 2]},
        ),
        (
            {'tn': {'name': 'Charlie', 'id': 3}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.namedtupleType',
                'params': {'tn': {'name': 'Charlie', 'id': 3}},
            },
            {'jsonrpc': '2.0', 'result': ['Charlie', 3]},
        ),
        (
            {'tn': {'name': 'David', 'id': 10}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.namedtupleType',
                'params': {'tn': {'name': 'David', 'id': 10}},
            },
            {'jsonrpc': '2.0', 'result': ['David', 10]},
        ),
        (
            {'tn': {'name': 'Eve', 'id': 99}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.namedtupleType',
                'params': {'tn': {'name': 'Eve', 'id': 99}},
            },
            {'jsonrpc': '2.0', 'result': ['Eve', 99]},
        ),
        (
            {'tn': {'name': 'Frank'}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.namedtupleType',
                'params': {'tn': {'name': 'Frank'}},
            },
            {'jsonrpc': '2.0', 'result': ['Frank', 3]},
        ),
    ],
)
def test_types_python_namedtuple_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.namedtupleType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.setType', 'types.python_stds_annotated.setType(s*: Array) -> Array', '')],
)
def test_types_python_set_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.setType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'s': [1, 2, 3]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.setType', 'params': {'s': [1, 2, 3]}},
            {'jsonrpc': '2.0', 'result': [1, 2, 3]},
        ),
        (
            {'s': [4, 5, 6]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.setType', 'params': {'s': [4, 5, 6]}},
            {'jsonrpc': '2.0', 'result': [4, 5, 6]},
        ),
        (
            {'s': []},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.setType', 'params': {'s': []}},
            {'jsonrpc': '2.0', 'result': []},
        ),
        (
            {'s': [10]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.setType', 'params': {'s': [10]}},
            {'jsonrpc': '2.0', 'result': [10]},
        ),
        (
            {'s': [1, 1, 2, 2, 3]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.setType', 'params': {'s': [1, 1, 2, 2, 3]}},
            {'jsonrpc': '2.0', 'result': [1, 2, 3]},
        ),
        (
            {'s': [7, 8, 9, 10, 11]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.setType', 'params': {'s': [7, 8, 9, 10, 11]}},
            {'jsonrpc': '2.0', 'result': [7, 8, 9, 10, 11]},
        ),
    ],
)
def test_types_python_set_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.setType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.sequenceType', 'types.python_stds_annotated.sequenceType(s*: Array) -> Array', '')],
)
def test_types_python_sequence_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.sequenceType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'s': [1, 2, 3]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.sequenceType', 'params': {'s': [1, 2, 3]}},
            {'jsonrpc': '2.0', 'result': [1, 2, 3]},
        ),
        (
            {'s': [10, 20, 30]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.sequenceType', 'params': {'s': [10, 20, 30]}},
            {'jsonrpc': '2.0', 'result': [10, 20, 30]},
        ),
        (
            {'s': []},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.sequenceType', 'params': {'s': []}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'constraint': 'Required',
                        'message': "cannot apply constraint Required for parameter 's' to value [] with type : "
                        "ensure the value of the parameter 's' is not empty.",
                        'param': 's',
                        'value': [],
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'s': [5]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.sequenceType', 'params': {'s': [5]}},
            {'jsonrpc': '2.0', 'result': [5]},
        ),
        (
            {'s': [100, 200, 300, 400, 500]},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.sequenceType',
                'params': {'s': [100, 200, 300, 400, 500]},
            },
            {'jsonrpc': '2.0', 'result': [100, 200, 300, 400, 500]},
        ),
        (
            {'s': [-1, -2, -3]},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.sequenceType', 'params': {'s': [-1, -2, -3]}},
            {'jsonrpc': '2.0', 'result': [-1, -2, -3]},
        ),
    ],
)
def test_types_python_sequence_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.sequenceType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'types.python_stds_annotated.typedDictType',
            'types.python_stds_annotated.typedDictType(user*: Object) -> Object',
            '',
        )
    ],
)
def test_types_python_typed_dict_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.typedDictType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'user': {'name': 'Alice', 'id': 1}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.typedDictType',
                'params': {'user': {'name': 'Alice', 'id': 1}},
            },
            {'jsonrpc': '2.0', 'result': {'name': 'Alice', 'id': 1}},
        ),
        (
            {'user': {'name': 'Bob', 'id': 2}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.typedDictType',
                'params': {'user': {'name': 'Bob', 'id': 2}},
            },
            {'jsonrpc': '2.0', 'result': {'name': 'Bob', 'id': 2}},
        ),
        (
            {'user': {'name': 'Charlie', 'id': 3}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.typedDictType',
                'params': {'user': {'name': 'Charlie', 'id': 3}},
            },
            {'jsonrpc': '2.0', 'result': {'name': 'Charlie', 'id': 3}},
        ),
        (
            {'user': {'name': 'Admin', 'id': 0}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.typedDictType',
                'params': {'user': {'name': 'Admin', 'id': 0}},
            },
            {'jsonrpc': '2.0', 'result': {'name': 'Admin', 'id': 0}},
        ),
        (
            {'user': {'name': 'User123', 'id': 999}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.typedDictType',
                'params': {'user': {'name': 'User123', 'id': 999}},
            },
            {'jsonrpc': '2.0', 'result': {'name': 'User123', 'id': 999}},
        ),
        (
            {'user': {'name': 'TestUser', 'id': 42}},
            {
                'jsonrpc': '2.0',
                'method': 'types.python_stds_annotated.typedDictType',
                'params': {'user': {'name': 'TestUser', 'id': 42}},
            },
            {'jsonrpc': '2.0', 'result': {'name': 'TestUser', 'id': 42}},
        ),
    ],
)
def test_types_python_typed_dict_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.typedDictType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'types.python_stds_annotated.unionWithTwoTypes',
            'types.python_stds_annotated.unionWithTwoTypes(n*: Number) -> Number',
            '',
        )
    ],
)
def test_types_python_union_with_two_types_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info(
        'types.python_stds_annotated.unionWithTwoTypes', method_title, method_signature, method_description
    )


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'n': 42},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.unionWithTwoTypes', 'params': {'n': 42}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'message': 'the only type of union that is supported is: '
                        'typing.Union[T, None] or typing.Optional[T]'
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 3.14},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.unionWithTwoTypes', 'params': {'n': 3.14}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'message': 'the only type of union that is supported is: '
                        'typing.Union[T, None] or typing.Optional[T]'
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'n': 0},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.unionWithTwoTypes', 'params': {'n': 0}},
            {
                'error': {
                    'code': -32602,
                    'data': {
                        'message': 'the only type of union that is supported is: '
                        'typing.Union[T, None] or typing.Optional[T]'
                    },
                    'message': 'Invalid params',
                    'name': 'InvalidParamsError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_types_python_union_with_two_types_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.unionWithTwoTypes', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.literalType', 'types.python_stds_annotated.literalType(x*: String) -> String', '')],
)
def test_types_python_literal_type_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.literalType', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'x': 'X'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalType', 'params': {'x': 'X'}},
            {'jsonrpc': '2.0', 'result': 'X'},
        ),
        (
            {'x': 'X'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalType', 'params': {'x': 'X'}},
            {'jsonrpc': '2.0', 'result': 'X'},
        ),
        (
            {'x': 'X'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalType', 'params': {'x': 'X'}},
            {'jsonrpc': '2.0', 'result': 'X'},
        ),
        (
            {'x': 'X'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalType', 'params': {'x': 'X'}},
            {'jsonrpc': '2.0', 'result': 'X'},
        ),
        (
            {'x': 'X'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalType', 'params': {'x': 'X'}},
            {'jsonrpc': '2.0', 'result': 'X'},
        ),
        (
            {'x': 'X'},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalType', 'params': {'x': 'X'}},
            {'jsonrpc': '2.0', 'result': 'X'},
        ),
    ],
)
def test_types_python_literal_type_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.literalType', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('types.python_stds_annotated.optional', 'types.python_stds_annotated.optional(n: Number) -> Number', '')],
)
def test_types_python_optional_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('types.python_stds_annotated.optional', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': {}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'n': None},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': {'n': None}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'n': 42},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': {'n': 42}},
            {'jsonrpc': '2.0', 'result': 42},
        ),
        (
            {'n': 0},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': {'n': 0}},
            {'jsonrpc': '2.0', 'result': 0},
        ),
        (
            {'n': 999},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': {'n': 999}},
            {'jsonrpc': '2.0', 'result': 999},
        ),
        (
            {'n': -123},
            {'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': {'n': -123}},
            {'jsonrpc': '2.0', 'result': -123},
        ),
    ],
)
def test_types_python_optional_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('types.python_stds_annotated.optional', test_input, request_expected, response_expected)
