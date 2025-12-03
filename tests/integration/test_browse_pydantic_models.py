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
    [('objects.pydantic_models.createPet', 'objects.pydantic_models.createPet(pet: Object) -> Object', '')],
)
def test_objects_pydantic_models_create_pet_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.pydantic_models.createPet', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'pet': {'name': 'Buddy', 'tag': 'dog'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createPet',
                'params': {'pet': {'name': 'Buddy', 'tag': 'dog'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Buddy', 'tag': 'dog'}},
        ),
        (
            {'pet': {'name': 'Whiskers', 'tag': 'cat'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createPet',
                'params': {'pet': {'name': 'Whiskers', 'tag': 'cat'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Whiskers', 'tag': 'cat'}},
        ),
        (
            {'pet': {'name': 'Goldie', 'tag': 'fish'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createPet',
                'params': {'pet': {'name': 'Goldie', 'tag': 'fish'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Goldie', 'tag': 'fish'}},
        ),
        (
            {'pet': {'name': 'Max', 'tag': 'hamster'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createPet',
                'params': {'pet': {'name': 'Max', 'tag': 'hamster'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Max', 'tag': 'hamster'}},
        ),
        (
            {'pet': {'name': 'Rocco', 'tag': 'bird'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createPet',
                'params': {'pet': {'name': 'Rocco', 'tag': 'bird'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Rocco', 'tag': 'bird'}},
        ),
        (
            {'pet': {'name': 'Special Pet Name with Spaces and Numbers 123', 'tag': 'exotic'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createPet',
                'params': {'pet': {'name': 'Special Pet Name with Spaces and Numbers 123', 'tag': 'exotic'}},
            },
            {
                'jsonrpc': '2.0',
                'result': {'id': 1, 'name': 'Special Pet Name with Spaces and Numbers 123', 'tag': 'exotic'},
            },
        ),
    ],
)
def test_objects_pydantic_models_create_pet_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.pydantic_models.createPet', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'objects.pydantic_models.createManyPet',
            'objects.pydantic_models.createManyPet(pets: Array, pet: Object) -> Array',
            '',
        )
    ],
)
def test_objects_pydantic_models_create_many_pet_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.pydantic_models.createManyPet', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'pets': [{'name': 'Buddy', 'tag': 'dog'}, {'name': 'Whiskers', 'tag': 'cat'}]},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyPet',
                'params': {'pets': [{'name': 'Buddy', 'tag': 'dog'}, {'name': 'Whiskers', 'tag': 'cat'}]},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Buddy', 'tag': 'dog'}, {'id': 1, 'name': 'Whiskers', 'tag': 'cat'}],
            },
        ),
        (
            {'pets': [{'name': 'Rex', 'tag': 'dog'}], 'pet': {'name': 'Luna', 'tag': 'cat'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyPet',
                'params': {'pets': [{'name': 'Rex', 'tag': 'dog'}], 'pet': {'name': 'Luna', 'tag': 'cat'}},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 0, 'name': 'Rex', 'tag': 'dog'}, {'id': 1, 'name': 'Luna', 'tag': 'cat'}],
            },
        ),
        (
            {'pets': []},
            {'jsonrpc': '2.0', 'method': 'objects.pydantic_models.createManyPet', 'params': {'pets': []}},
            {'jsonrpc': '2.0', 'result': []},
        ),
        (
            {'pets': [{'name': 'Solo', 'tag': 'fish'}]},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyPet',
                'params': {'pets': [{'name': 'Solo', 'tag': 'fish'}]},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 0, 'name': 'Solo', 'tag': 'fish'}]},
        ),
        (
            {
                'pets': [
                    {'name': 'Alpha', 'tag': 'wolf'},
                    {'name': 'Beta', 'tag': 'wolf'},
                    {'name': 'Gamma', 'tag': 'wolf'},
                ]
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyPet',
                'params': {
                    'pets': [
                        {'name': 'Alpha', 'tag': 'wolf'},
                        {'name': 'Beta', 'tag': 'wolf'},
                        {'name': 'Gamma', 'tag': 'wolf'},
                    ]
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Alpha', 'tag': 'wolf'},
                    {'id': 1, 'name': 'Beta', 'tag': 'wolf'},
                    {'id': 2, 'name': 'Gamma', 'tag': 'wolf'},
                ],
            },
        ),
        (
            {
                'pets': [{'name': 'Multi Pet', 'tag': 'test'}],
                'pet': {'name': 'Additional Pet with Long Name', 'tag': 'special'},
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyPet',
                'params': {
                    'pets': [{'name': 'Multi Pet', 'tag': 'test'}],
                    'pet': {'name': 'Additional Pet with Long Name', 'tag': 'special'},
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 0, 'name': 'Multi Pet', 'tag': 'test'},
                    {'id': 1, 'name': 'Additional Pet with Long Name', 'tag': 'special'},
                ],
            },
        ),
    ],
)
def test_objects_pydantic_models_create_many_pet_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.pydantic_models.createManyPet', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [
        (
            'objects.pydantic_models.createManyFixPet',
            'objects.pydantic_models.createManyFixPet(pets: Object) -> Array',
            '',
        )
    ],
)
def test_objects_pydantic_models_create_many_fix_pet_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.pydantic_models.createManyFixPet', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'pets': {'1': {'name': 'Buddy', 'tag': 'dog'}, '2': {'name': 'Whiskers', 'tag': 'cat'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyFixPet',
                'params': {'pets': {'1': {'name': 'Buddy', 'tag': 'dog'}, '2': {'name': 'Whiskers', 'tag': 'cat'}}},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 1, 'name': 'Buddy', 'tag': 'dog'}, {'id': 2, 'name': 'Whiskers', 'tag': 'cat'}],
            },
        ),
        (
            {'pets': {'5': {'name': 'Charlie', 'tag': 'bird'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyFixPet',
                'params': {'pets': {'5': {'name': 'Charlie', 'tag': 'bird'}}},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 5, 'name': 'Charlie', 'tag': 'bird'}]},
        ),
        (
            {'pets': {}},
            {'jsonrpc': '2.0', 'method': 'objects.pydantic_models.createManyFixPet', 'params': {'pets': {}}},
            {'jsonrpc': '2.0', 'result': []},
        ),
        (
            {'pets': {'10': {'name': 'Solo Pet', 'tag': 'unique'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyFixPet',
                'params': {'pets': {'10': {'name': 'Solo Pet', 'tag': 'unique'}}},
            },
            {'jsonrpc': '2.0', 'result': [{'id': 10, 'name': 'Solo Pet', 'tag': 'unique'}]},
        ),
        (
            {
                'pets': {
                    '3': {'name': 'Rex', 'tag': 'dog'},
                    '7': {'name': 'Fluffy', 'tag': 'rabbit'},
                    '9': {'name': 'Spike', 'tag': 'turtle'},
                }
            },
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyFixPet',
                'params': {
                    'pets': {
                        '3': {'name': 'Rex', 'tag': 'dog'},
                        '7': {'name': 'Fluffy', 'tag': 'rabbit'},
                        '9': {'name': 'Spike', 'tag': 'turtle'},
                    }
                },
            },
            {
                'jsonrpc': '2.0',
                'result': [
                    {'id': 3, 'name': 'Rex', 'tag': 'dog'},
                    {'id': 7, 'name': 'Fluffy', 'tag': 'rabbit'},
                    {'id': 9, 'name': 'Spike', 'tag': 'turtle'},
                ],
            },
        ),
        (
            {'pets': {'100': {'name': 'Complex Pet Name with Special Characters !@#', 'tag': 'exotic'}}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.createManyFixPet',
                'params': {'pets': {'100': {'name': 'Complex Pet Name with Special Characters !@#', 'tag': 'exotic'}}},
            },
            {
                'jsonrpc': '2.0',
                'result': [{'id': 100, 'name': 'Complex Pet Name with Special Characters !@#', 'tag': 'exotic'}],
            },
        ),
    ],
)
def test_objects_pydantic_models_create_many_fix_pet_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.pydantic_models.createManyFixPet', test_input, request_expected, response_expected)


@pytest.mark.parametrize(
    'method_title,method_signature,method_description',
    [('objects.pydantic_models.removePet', 'objects.pydantic_models.removePet(pet: Object) -> Object', '')],
)
def test_objects_pydantic_models_remove_pet_display(
    jsonrpc_page_info: t.Callable[..., Page], method_title: str, method_signature: str, method_description: str
) -> None:
    jsonrpc_page_info('objects.pydantic_models.removePet', method_title, method_signature, method_description)


@pytest.mark.parametrize(
    'test_input,request_expected,response_expected',
    [
        (
            {'pet': {'id': 5, 'name': 'Buddy', 'tag': 'dog'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.removePet',
                'params': {'pet': {'id': 5, 'name': 'Buddy', 'tag': 'dog'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 5, 'name': 'Buddy', 'tag': 'dog'}},
        ),
        (
            {},
            {'jsonrpc': '2.0', 'method': 'objects.pydantic_models.removePet', 'params': {}},
            {'jsonrpc': '2.0', 'result': None},
        ),
        (
            {'pet': {'id': 15, 'name': 'Error', 'tag': 'test'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.removePet',
                'params': {'pet': {'id': 15, 'name': 'Error', 'tag': 'test'}},
            },
            {
                'error': {
                    'code': -32000,
                    'data': {'pet_id': 15, 'reason': 'The pet with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
        (
            {'pet': {'id': 1, 'name': 'Whiskers', 'tag': 'cat'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.removePet',
                'params': {'pet': {'id': 1, 'name': 'Whiskers', 'tag': 'cat'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Whiskers', 'tag': 'cat'}},
        ),
        (
            {'pet': {'id': 10, 'name': 'Max ID', 'tag': 'limit'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.removePet',
                'params': {'pet': {'id': 10, 'name': 'Max ID', 'tag': 'limit'}},
            },
            {'jsonrpc': '2.0', 'result': {'id': 10, 'name': 'Max ID', 'tag': 'limit'}},
        ),
        (
            {'pet': {'id': 50, 'name': 'High ID Pet with Long Name', 'tag': 'error_test'}},
            {
                'jsonrpc': '2.0',
                'method': 'objects.pydantic_models.removePet',
                'params': {'pet': {'id': 50, 'name': 'High ID Pet with Long Name', 'tag': 'error_test'}},
            },
            {
                'error': {
                    'code': -32000,
                    'data': {'pet_id': 50, 'reason': 'The pet with an ID greater than 10 does not exist.'},
                    'message': 'Server error',
                    'name': 'ServerError',
                },
                'jsonrpc': '2.0',
            },
        ),
    ],
)
def test_objects_pydantic_models_remove_pet_form(
    jsonrpc_call: t.Callable[..., Page],
    test_input: dict[str, t.Any],
    request_expected: dict[str, t.Any],
    response_expected: dict[str, t.Any],
) -> None:
    jsonrpc_call('objects.pydantic_models.removePet', test_input, request_expected, response_expected)
