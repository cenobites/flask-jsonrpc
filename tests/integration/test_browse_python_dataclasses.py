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
    [('objects.python_dataclasses.createCar', 'objects.python_dataclasses.createCar(car: Object) -> Object', '')],
)
def test_objects_python_dataclasses_create_car_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_dataclasses.createCar', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'car': {'name': 'Tesla', 'tag': 'electric'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createCar',
                'params': {'car': {'name': 'Tesla', 'tag': 'electric'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Tesla', 'tag': 'electric'}},
        ),
        (
            {'car': {'name': 'BMW', 'tag': 'luxury'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createCar',
                'params': {'car': {'name': 'BMW', 'tag': 'luxury'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'BMW', 'tag': 'luxury'}},
        ),
        (
            {'car': {'name': 'Toyota', 'tag': 'reliable'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createCar',
                'params': {'car': {'name': 'Toyota', 'tag': 'reliable'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Toyota', 'tag': 'reliable'}},
        ),
        (
            {'car': {'name': 'Honda', 'tag': 'efficient'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createCar',
                'params': {'car': {'name': 'Honda', 'tag': 'efficient'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Honda', 'tag': 'efficient'}},
        ),
        (
            {'car': {'name': 'Ford', 'tag': 'american'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createCar',
                'params': {'car': {'name': 'Ford', 'tag': 'american'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Ford', 'tag': 'american'}},
        ),
        (
            {'car': {'name': 'Special Car Name with Numbers 123 and Characters !@#', 'tag': 'unique'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createCar',
                'params': {'car': {'name': 'Special Car Name with Numbers 123 and Characters !@#', 'tag': 'unique'}},
            },
            {
                'jsonrpc': '2.0',
                'result': {'id': 1, 'name': 'Special Car Name with Numbers 123 and Characters !@#', 'tag': 'unique'},
            },
        ),
    ],
)
def test_objects_python_dataclasses_create_car_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_dataclasses.createCar', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'objects.python_dataclasses.createManyCar',
            'objects.python_dataclasses.createManyCar(cars: Array, car: Object) -> Array',
            '',
        )
    ],
)
def test_objects_python_dataclasses_create_many_car_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_dataclasses.createManyCar', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'cars': [{'name': 'Tesla', 'tag': 'electric'}, {'name': 'BMW', 'tag': 'luxury'}]},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyCar',
                'params': {'cars': [{'name': 'Tesla', 'tag': 'electric'}, {'name': 'BMW', 'tag': 'luxury'}]},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Tesla', 'tag': 'electric'}, {'id': 1, 'name': 'BMW', 'tag': 'luxury'}],
            },
        ),
        (
            {'cars': [{'name': 'Honda', 'tag': 'reliable'}], 'car': {'name': 'Ford', 'tag': 'american'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyCar',
                'params': {'cars': [{'name': 'Honda', 'tag': 'reliable'}], 'car': {'name': 'Ford', 'tag': 'american'}},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Honda', 'tag': 'reliable'}, {'id': 1, 'name': 'Ford', 'tag': 'american'}],
            },
        ),
        (
            {'cars': []},
            {'jsonrpc': '2.0', 'method': 'objects.python_dataclasses.createManyCar', 'params': {'cars': []}},
            {'jsonrpc': '2.0', 'result': []},
        ),
        (
            {'cars': [{'name': 'Solo Car', 'tag': 'single'}]},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyCar',
                'params': {'cars': [{'name': 'Solo Car', 'tag': 'single'}]},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 0, 'name': 'Solo Car', 'tag': 'single'}]},
        ),
        (
            {
                'cars': [
                    {'name': 'Audi', 'tag': 'german'},
                    {'name': 'Mercedes', 'tag': 'luxury'},
                    {'name': 'Volkswagen', 'tag': 'popular'},
                ]
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyCar',
                'params': {
                    'cars': [
                        {'name': 'Audi', 'tag': 'german'},
                        {'name': 'Mercedes', 'tag': 'luxury'},
                        {'name': 'Volkswagen', 'tag': 'popular'},
                    ]
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Audi', 'tag': 'german'},
                    {'id': 1, 'name': 'Mercedes', 'tag': 'luxury'},
                    {'id': 2, 'name': 'Volkswagen', 'tag': 'popular'},
                ],
            },
        ),
        (
            {
                'cars': [{'name': 'Base Car', 'tag': 'test'}],
                'car': {'name': 'Additional Car with Long Complex Name', 'tag': 'special'},
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyCar',
                'params': {
                    'cars': [{'name': 'Base Car', 'tag': 'test'}],
                    'car': {'name': 'Additional Car with Long Complex Name', 'tag': 'special'},
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Base Car', 'tag': 'test'},
                    {'id': 1, 'name': 'Additional Car with Long Complex Name', 'tag': 'special'},
                ],
            },
        ),
    ],
)
def test_objects_python_dataclasses_create_many_car_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_dataclasses.createManyCar', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'objects.python_dataclasses.createManyFixCar',
            'objects.python_dataclasses.createManyFixCar(cars: Object) -> Array',
            '',
        )
    ],
)
def test_objects_python_dataclasses_create_many_fix_car_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_dataclasses.createManyFixCar', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'cars': {'1': {'name': 'Tesla', 'tag': 'electric'}, '2': {'name': 'BMW', 'tag': 'luxury'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyFixCar',
                'params': {'cars': {'1': {'name': 'Tesla', 'tag': 'electric'}, '2': {'name': 'BMW', 'tag': 'luxury'}}},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 1, 'name': 'Tesla', 'tag': 'electric'}, {'id': 2, 'name': 'BMW', 'tag': 'luxury'}],
            },
        ),
        (
            {'cars': {'5': {'name': 'Mercedes', 'tag': 'luxury'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyFixCar',
                'params': {'cars': {'5': {'name': 'Mercedes', 'tag': 'luxury'}}},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 5, 'name': 'Mercedes', 'tag': 'luxury'}]},
        ),
        (
            {'cars': {}},
            {'jsonrpc': '2.0', 'method': 'objects.python_dataclasses.createManyFixCar', 'params': {'cars': {}}},
            {'jsonrpc': '2.0', 'result': []},
        ),
        (
            {'cars': {'10': {'name': 'Solo Car', 'tag': 'unique'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyFixCar',
                'params': {'cars': {'10': {'name': 'Solo Car', 'tag': 'unique'}}},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 10, 'name': 'Solo Car', 'tag': 'unique'}]},
        ),
        (
            {
                'cars': {
                    '3': {'name': 'Audi', 'tag': 'german'},
                    '7': {'name': 'Honda', 'tag': 'reliable'},
                    '9': {'name': 'Toyota', 'tag': 'popular'},
                }
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyFixCar',
                'params': {
                    'cars': {
                        '3': {'name': 'Audi', 'tag': 'german'},
                        '7': {'name': 'Honda', 'tag': 'reliable'},
                        '9': {'name': 'Toyota', 'tag': 'popular'},
                    }
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 3, 'name': 'Audi', 'tag': 'german'},
                    {'id': 7, 'name': 'Honda', 'tag': 'reliable'},
                    {'id': 9, 'name': 'Toyota', 'tag': 'popular'},
                ],
            },
        ),
        (
            {'cars': {'100': {'name': 'Complex Car Name with Special Characters !@#$%', 'tag': 'exotic'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.createManyFixCar',
                'params': {
                    'cars': {'100': {'name': 'Complex Car Name with Special Characters !@#$%', 'tag': 'exotic'}}
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 100, 'name': 'Complex Car Name with Special Characters !@#$%', 'tag': 'exotic'}],
            },
        ),
    ],
)
def test_objects_python_dataclasses_create_many_fix_car_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_dataclasses.createManyFixCar', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('objects.python_dataclasses.removeCar', 'objects.python_dataclasses.removeCar(car: Object) -> Object', '')],
)
def test_objects_python_dataclasses_remove_car_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.python_dataclasses.removeCar', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'car': {'id': 5, 'name': 'Tesla', 'tag': 'electric'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.removeCar',
                'params': {'car': {'id': 5, 'name': 'Tesla', 'tag': 'electric'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 5, 'name': 'Tesla', 'tag': 'electric'}},
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'objects.python_dataclasses.removeCar', 'params': {}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'car': {'id': 15, 'name': 'Error', 'tag': 'test'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.removeCar',
                'params': {'car': {'id': 15, 'name': 'Error', 'tag': 'test'}},
            },
            {
                'error': {
                    'code': -32000,
                    'data': {'car_id': 15, 'reason': 'The car with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'car': {'id': 1, 'name': 'BMW', 'tag': 'luxury'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.removeCar',
                'params': {'car': {'id': 1, 'name': 'BMW', 'tag': 'luxury'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'BMW', 'tag': 'luxury'}},
        ),
        (
            {'car': {'id': 10, 'name': 'Max ID Car', 'tag': 'limit'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.removeCar',
                'params': {'car': {'id': 10, 'name': 'Max ID Car', 'tag': 'limit'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 10, 'name': 'Max ID Car', 'tag': 'limit'}},
        ),
        (
            {'car': {'id': 50, 'name': 'High ID Car with Long Name and Numbers 123', 'tag': 'error_test'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.python_dataclasses.removeCar',
                'params': {
                    'car': {'id': 50, 'name': 'High ID Car with Long Name and Numbers 123', 'tag': 'error_test'}
                },
            },
            {
                'error': {
                    'code': -32000,
                    'data': {'car_id': 50, 'reason': 'The car with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_objects_python_dataclasses_remove_car_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.python_dataclasses.removeCar', test_input, request_expected, response_expected)
