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

if t.TYPE_CHECKING:
    from requests import Session


def test_bool_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.boolType', 'params': [True], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': True, 'id': 1}


def test_str_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.strType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_bytes_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytesType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_bytearray_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.bytearrayType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_int_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intType', 'params': [42], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 42, 'id': 1}


def test_float_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.floatType', 'params': [3.14], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 3.14, 'id': 1}


def test_enum_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.intEnumType', 'params': [1], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 1, 'id': 1}


def test_decimal_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.decimalType', 'params': [1.5], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': '1.5', 'id': 1}


def test_list_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.listType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_tuple_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.tupleType', 'params': [[1, 2]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2], 'id': 1}


def test_namedtuple_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={
            'jsonrpc': '2.0',
            'method': 'types.python_stds_annotated.namedtupleType',
            'params': [{'name': 'Alice', 'id': 1}],
            'id': 1,
        },
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': ['Alice', 1], 'id': 1}


def test_set_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.setType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert sorted(rv.json()['result']) == [1, 2, 3]


def test_frozenset_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.frozensetType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert sorted(rv.json()['result']) == [1, 2, 3]


def test_deque_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.dequeType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_sequence_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.sequenceType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_dict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.dictType', 'params': [{'key': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 1}, 'id': 1}


def test_typedict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={
            'jsonrpc': '2.0',
            'method': 'types.python_stds_annotated.typedDictType',
            'params': [{'name': 'Alice', 'id': 1}],
            'id': 1,
        },
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Alice'}}


def test_optional(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}

    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.optional', 'params': [1], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 1, 'id': 1}


def test_union(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.union', 'params': [42], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 42, 'id': 1}

    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.union', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_union_with_two_types(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.unionWithTwoTypes', 'params': [42], 'id': 1},
    )
    assert rv.json() == {
        'jsonrpc': '2.0',
        'id': 1,
        'error': {
            'code': -32602,
            'data': {
                'message': 'the only type of union that is supported is: typing.Union[T, None] or typing.Optional[T]'
            },
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }


def test_literal_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalType', 'params': ['X'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'X', 'id': 1}


def test_none_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.noneType', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_no_return_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.noReturnType', 'params': ['no return'], 'id': 1},
    )
    assert rv.json()['error']['data']['message'] == 'no return'


def test_literal_none_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds_annotated.literalNoneType', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds-annotated', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'}
    )
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'types.python_stds_annotated.boolType': {
            'description': 'This method accepts a boolean value and returns it.',
            'errors': [{'code': -32000, 'message': 'The value must be a boolean.', 'status_code': 500}],
            'examples': [
                {
                    'description': 'This method demonstrates how to use a boolean type in JSON-RPC.',
                    'name': 'Example of boolean type',
                    'params': [{'description': 'A boolean value that is True.', 'name': 'yes', 'value': True}],
                    'returns': {'description': 'The same boolean value returned.', 'name': 'result', 'value': True},
                    'summary': 'An example of a boolean type',
                }
            ],
            'name': 'types.python_stds_annotated.boolType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a boolean value.',
                    'examples': [True],
                    'name': 'yes',
                    'nullable': False,
                    'required': True,
                    'summary': 'A boolean value',
                    'type': 'Boolean',
                }
            ],
            'returns': {
                'description': 'This is the same boolean value returned.',
                'examples': [True],
                'name': 'default',
                'summary': 'A boolean value',
                'type': 'Boolean',
            },
            'summary': 'This is a boolean type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.bytearrayType': {
            'description': 'This method accepts a bytearray value and returns it.',
            'examples': [
                {
                    'name': 'Example of bytearray type',
                    'params': [{'description': 'A bytearray value.', 'name': 'b', 'value': 'Hello'}],
                    'returns': {
                        'description': 'The same bytearray value returned.',
                        'name': 'result',
                        'value': 'Hello',
                    },
                }
            ],
            'name': 'types.python_stds_annotated.bytearrayType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a bytearray value.',
                    'examples': ['Hello'],
                    'name': 'b',
                    'nullable': False,
                    'required': True,
                    'summary': 'A bytearray value',
                    'type': 'String',
                }
            ],
            'returns': {
                'description': 'This is the same bytearray value returned.',
                'examples': ['Hello'],
                'name': 'default',
                'summary': 'A bytearray value',
                'type': 'String',
            },
            'summary': 'This is a bytearray type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.bytesType': {
            'description': 'This method accepts a bytes value and returns it.',
            'examples': [
                {
                    'name': 'Example of bytes type',
                    'params': [{'description': 'A bytes value.', 'name': 'b', 'value': 'Hello'}],
                    'returns': {'description': 'The same bytes value returned.', 'name': 'result', 'value': 'Hello'},
                }
            ],
            'name': 'types.python_stds_annotated.bytesType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a bytes value.',
                    'examples': ['Hello'],
                    'name': 'b',
                    'nullable': False,
                    'required': True,
                    'summary': 'A bytes value',
                    'type': 'String',
                }
            ],
            'returns': {
                'description': 'This is the same bytes value returned.',
                'examples': ['Hello'],
                'name': 'default',
                'summary': 'A bytes value',
                'type': 'String',
            },
            'summary': 'This is a bytes type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.decimalType': {
            'description': 'This method accepts a Decimal value and returns it.',
            'examples': [
                {
                    'name': 'Example of decimal type',
                    'params': [{'description': 'A decimal value.', 'name': 'n', 'value': '1.5'}],
                    'returns': {'description': 'The same decimal value returned.', 'name': 'result', 'value': '1.5'},
                }
            ],
            'name': 'types.python_stds_annotated.decimalType',
            'notification': True,
            'params': [
                {
                    'decimal_places': 2,
                    'description': 'This parameter should be a decimal value.',
                    'examples': ['1.5'],
                    'name': 'n',
                    'nullable': False,
                    'required': True,
                    'summary': 'A decimal value',
                    'type': 'Number',
                }
            ],
            'returns': {
                'description': 'This is the same decimal value returned.',
                'examples': ['1.5'],
                'name': 'default',
                'summary': 'A decimal value',
                'type': 'Number',
            },
            'summary': 'This is a decimal type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.dequeType': {
            'description': 'This method accepts a deque of integers and returns it.',
            'examples': [
                {
                    'name': 'Example of deque type',
                    'params': [{'description': 'A deque of integers.', 'name': 'd', 'value': [1, 2, 3]}],
                    'returns': {'description': 'The same deque returned.', 'name': 'result', 'value': [1, 2, 3]},
                }
            ],
            'name': 'types.python_stds_annotated.dequeType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a deque of integers.',
                    'examples': [[1, 2, 3]],
                    'name': 'd',
                    'nullable': False,
                    'required': True,
                    'summary': 'A deque of integers',
                    'type': 'Array',
                }
            ],
            'returns': {
                'description': 'This is the same deque returned.',
                'examples': [[1, 2, 3]],
                'name': 'default',
                'summary': 'A deque of integers',
                'type': 'Array',
            },
            'summary': 'This is a deque type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.dictType': {
            'description': 'This method accepts a dict of str to int and returns it.',
            'examples': [
                {
                    'name': 'Example of dict type',
                    'params': [{'description': 'A dict of str to int.', 'name': 'd', 'value': {'key': 1}}],
                    'returns': {'description': 'The same dict returned.', 'name': 'result', 'value': {'key': 1}},
                }
            ],
            'name': 'types.python_stds_annotated.dictType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a dict of str to int.',
                    'examples': [{'key': 1}],
                    'name': 'd',
                    'nullable': False,
                    'required': True,
                    'summary': 'A dict of str to int',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'This is the same dict returned.',
                'examples': [{'key': 1}],
                'name': 'default',
                'summary': 'A dict of str to int',
                'type': 'Object',
            },
            'summary': 'This is a dict type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.floatType': {
            'description': 'This method accepts a float value and returns it.',
            'examples': [
                {
                    'name': 'Example of float type',
                    'params': [{'description': 'A float value.', 'name': 'n', 'value': 3.14}],
                    'returns': {'description': 'The same float value returned.', 'name': 'result', 'value': 3.14},
                }
            ],
            'name': 'types.python_stds_annotated.floatType',
            'notification': True,
            'params': [
                {
                    'decimal_places': 2,
                    'description': 'This parameter should be a float value.',
                    'examples': [3.14],
                    'name': 'n',
                    'nullable': False,
                    'required': True,
                    'summary': 'A float value',
                    'type': 'Number',
                }
            ],
            'returns': {
                'description': 'This is the same float value returned.',
                'examples': [3.14],
                'name': 'default',
                'summary': 'A float value',
                'type': 'Number',
            },
            'summary': 'This is a float type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.frozensetType': {
            'description': 'This method accepts a frozenset of integers and returns it.',
            'examples': [
                {
                    'name': 'Example of frozenset type',
                    'params': [{'description': 'A frozenset of integers.', 'name': 's', 'value': [1, 2, 3]}],
                    'returns': {'description': 'The same frozenset returned.', 'name': 'result', 'value': [1, 2, 3]},
                }
            ],
            'name': 'types.python_stds_annotated.frozensetType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a frozenset of integers.',
                    'examples': [[1, 2, 3]],
                    'name': 's',
                    'nullable': False,
                    'required': True,
                    'summary': 'A frozenset of integers',
                    'type': 'Array',
                }
            ],
            'returns': {
                'description': 'This is the same frozenset returned.',
                'examples': [[1, 2, 3]],
                'name': 'default',
                'summary': 'A frozenset of integers',
                'type': 'Array',
            },
            'summary': 'This is a frozenset type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.intEnumType': {
            'description': 'This method accepts a ColorIntEnum value and returns it.',
            'examples': [
                {
                    'name': 'Example of int enum type',
                    'params': [{'description': 'A ColorIntEnum value.', 'name': 'e', 'value': 1}],
                    'returns': {'description': 'The same enum value returned.', 'name': 'result', 'value': 1},
                }
            ],
            'name': 'types.python_stds_annotated.intEnumType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a ColorIntEnum value.',
                    'examples': [1],
                    'name': 'e',
                    'nullable': False,
                    'required': True,
                    'summary': 'A ColorIntEnum value',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'This is the same enum value returned.',
                'examples': [1],
                'name': 'default',
                'summary': 'A ColorIntEnum value',
                'type': 'Object',
            },
            'summary': 'This is an int enum type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.intType': {
            'description': 'This method accepts an int value and returns it.',
            'examples': [
                {
                    'name': 'Example of int type',
                    'params': [{'description': 'An integer value.', 'name': 'n', 'value': 42}],
                    'returns': {'description': 'The same integer value returned.', 'name': 'result', 'value': 42},
                }
            ],
            'name': 'types.python_stds_annotated.intType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be an integer value.',
                    'examples': [42],
                    'max_digits': 10,
                    'maximum': 1000000,
                    'minimum': 0,
                    'name': 'n',
                    'nullable': False,
                    'required': True,
                    'summary': 'An integer value',
                    'type': 'Number',
                }
            ],
            'returns': {
                'description': 'This is the same integer value returned.',
                'examples': [42],
                'name': 'default',
                'summary': 'An integer value',
                'type': 'Number',
            },
            'summary': 'This is an int type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.listType': {
            'description': 'This method accepts a list of integers and returns it.',
            'examples': [
                {
                    'name': 'Example of list type',
                    'params': [{'description': 'A list of integers.', 'name': 'lst', 'value': [1, 2, 3]}],
                    'returns': {'description': 'The same list returned.', 'name': 'result', 'value': [1, 2, 3]},
                }
            ],
            'name': 'types.python_stds_annotated.listType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a list of integers.',
                    'examples': [[1, 2, 3]],
                    'max_length': 100,
                    'min_length': 1,
                    'name': 'lst',
                    'nullable': False,
                    'required': True,
                    'summary': 'A list of integers',
                    'type': 'Array',
                }
            ],
            'returns': {
                'description': 'This is the same list returned.',
                'examples': [[1, 2, 3]],
                'name': 'default',
                'summary': 'A list of integers',
                'type': 'Array',
            },
            'summary': 'This is a list type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.literalNoneType': {
            'description': 'This method accepts a literal None and returns it.',
            'examples': [
                {
                    'name': 'Example of literal none type',
                    'params': [{'description': 'A literal None value.', 'name': 'x'}],
                    'returns': {'description': 'The same literal None value returned.', 'name': 'result'},
                }
            ],
            'name': 'types.python_stds_annotated.literalNoneType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a literal None value.',
                    'examples': [None],
                    'name': 'x',
                    'nullable': True,
                    'summary': 'A literal None value',
                    'type': 'Null',
                }
            ],
            'returns': {
                'description': 'This is the same literal None value returned.',
                'examples': [None],
                'name': 'default',
                'summary': 'A literal None value',
                'type': 'Null',
            },
            'summary': 'This is a literal none type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.literalType': {
            'description': 'This method accepts a literal value "X" and returns it.',
            'examples': [
                {
                    'name': 'Example of literal type',
                    'params': [{'description': 'A literal value "X".', 'name': 'x', 'value': 'X'}],
                    'returns': {'description': 'The same literal value returned.', 'name': 'result', 'value': 'X'},
                }
            ],
            'name': 'types.python_stds_annotated.literalType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a literal value "X".',
                    'examples': ['X'],
                    'name': 'x',
                    'nullable': False,
                    'required': True,
                    'summary': 'A literal value "X"',
                    'type': 'String',
                }
            ],
            'returns': {
                'description': 'This is the same literal value returned.',
                'examples': ['X'],
                'name': 'default',
                'summary': 'A literal value "X"',
                'type': 'String',
            },
            'summary': 'This is a literal type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.namedtupleType': {
            'description': 'This method accepts an EmployeeNamedTuple and returns it with 200.',
            'examples': [
                {
                    'name': 'Example of namedtuple type',
                    'params': [
                        {'description': 'An EmployeeNamedTuple.', 'name': 'tn', 'value': {'id': 1, 'name': 'Alice'}}
                    ],
                    'returns': {
                        'description': 'The namedtuple and 200 returned.',
                        'name': 'result',
                        'value': [['Alice', 1], 200],
                    },
                }
            ],
            'name': 'types.python_stds_annotated.namedtupleType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be an EmployeeNamedTuple.',
                    'examples': [{'id': 1, 'name': 'Alice'}],
                    'name': 'tn',
                    'nullable': False,
                    'properties': {'id': {'name': 'id', 'type': 'Number'}, 'name': {'name': 'name', 'type': 'String'}},
                    'required': True,
                    'summary': 'An EmployeeNamedTuple',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'Returns the namedtuple and 200.',
                'examples': [[['Alice', 1], 200]],
                'name': 'default',
                'summary': 'A tuple of EmployeeNamedTuple and int',
                'type': 'Array',
            },
            'summary': 'This is a named tuple type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.noReturnType': {
            'description': 'This method always raises an error.',
            'examples': [
                {
                    'name': 'Example of no return type',
                    'params': [{'description': 'A string value.', 'name': 's', 'value': 'no return'}],
                    'returns': {'description': 'No return value.', 'name': 'result'},
                }
            ],
            'name': 'types.python_stds_annotated.noReturnType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a string value.',
                    'examples': ['no return'],
                    'name': 's',
                    'nullable': False,
                    'required': True,
                    'summary': 'A string value',
                    'type': 'String',
                }
            ],
            'returns': {
                'description': 'This method does not return.',
                'examples': [None],
                'name': 'default',
                'summary': 'No return value',
                'type': 'Null',
            },
            'summary': 'This is a no return type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.noneType': {
            'description': 'This method accepts None and returns it.',
            'examples': [
                {
                    'name': 'Example of none type',
                    'params': [{'description': 'A None value.', 'name': 'obj'}],
                    'returns': {'description': 'The same None value returned.', 'name': 'result'},
                }
            ],
            'name': 'types.python_stds_annotated.noneType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be None.',
                    'examples': [None],
                    'name': 'obj',
                    'nullable': True,
                    'summary': 'A None value',
                    'type': 'Null',
                }
            ],
            'returns': {
                'description': 'This is the same None value returned.',
                'examples': [None],
                'name': 'default',
                'summary': 'A None value',
                'type': 'Null',
            },
            'summary': 'This is a none type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.optional': {
            'description': 'This method accepts an optional integer and returns it.',
            'examples': [
                {
                    'name': 'Example of optional type',
                    'params': [{'description': 'An optional integer.', 'name': 'n'}],
                    'returns': {'description': 'The same optional value returned.', 'name': 'result'},
                }
            ],
            'name': 'types.python_stds_annotated.optional',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be an optional integer.',
                    'examples': [None],
                    'name': 'n',
                    'nullable': True,
                    'summary': 'An optional integer',
                    'type': 'Number',
                }
            ],
            'returns': {
                'description': 'This is the same optional value returned.',
                'examples': [None],
                'name': 'default',
                'summary': 'An optional integer',
                'type': 'Number',
            },
            'summary': 'This is an optional type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.sequenceType': {
            'description': 'This method accepts a sequence of integers and returns it.',
            'examples': [
                {
                    'name': 'Example of sequence type',
                    'params': [{'description': 'A sequence of integers.', 'name': 's', 'value': [1, 2, 3]}],
                    'returns': {'description': 'The same sequence returned.', 'name': 'result', 'value': [1, 2, 3]},
                }
            ],
            'name': 'types.python_stds_annotated.sequenceType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a sequence of integers.',
                    'examples': [[1, 2, 3]],
                    'name': 's',
                    'nullable': False,
                    'required': True,
                    'summary': 'A sequence of integers',
                    'type': 'Array',
                }
            ],
            'returns': {
                'description': 'This is the same sequence returned.',
                'examples': [[1, 2, 3]],
                'name': 'default',
                'summary': 'A sequence of integers',
                'type': 'Array',
            },
            'summary': 'This is a sequence type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.setType': {
            'description': 'This method accepts a set of integers and returns it.',
            'examples': [
                {
                    'name': 'Example of set type',
                    'params': [{'description': 'A set of integers.', 'name': 's', 'value': [1, 2, 3]}],
                    'returns': {'description': 'The same set returned.', 'name': 'result', 'value': [1, 2, 3]},
                }
            ],
            'name': 'types.python_stds_annotated.setType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a set of integers.',
                    'examples': [[1, 2, 3]],
                    'name': 's',
                    'nullable': False,
                    'required': True,
                    'summary': 'A set of integers',
                    'type': 'Array',
                }
            ],
            'returns': {
                'description': 'This is the same set returned.',
                'examples': [[1, 2, 3]],
                'name': 'default',
                'summary': 'A set of integers',
                'type': 'Array',
            },
            'summary': 'This is a set type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.strType': {
            'description': 'This method accepts a string value and returns it.',
            'examples': [
                {
                    'name': 'Example of string type',
                    'params': [{'description': 'A string value.', 'name': 'st', 'value': 'Hello'}],
                    'returns': {'description': 'The same string value returned.', 'name': 'result', 'value': 'Hello'},
                }
            ],
            'name': 'types.python_stds_annotated.strType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a string value.',
                    'examples': ['Hello'],
                    'max_length': 100,
                    'min_length': 1,
                    'name': 'st',
                    'nullable': False,
                    'required': True,
                    'summary': 'A string value',
                    'type': 'String',
                }
            ],
            'returns': {
                'description': 'This is the same string value returned.',
                'examples': ['Hello'],
                'name': 'default',
                'summary': 'A string value',
                'type': 'String',
            },
            'summary': 'This is a string type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.tupleType': {
            'description': 'This method accepts a tuple of two integers and returns it with 200.',
            'examples': [
                {
                    'name': 'Example of tuple type',
                    'params': [{'description': 'A tuple of two integers.', 'name': 'tn', 'value': [1, 2]}],
                    'returns': {'description': 'The tuple and 200 returned.', 'name': 'result', 'value': [[1, 2], 200]},
                }
            ],
            'name': 'types.python_stds_annotated.tupleType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a tuple of two integers.',
                    'examples': [[1, 2]],
                    'name': 'tn',
                    'nullable': False,
                    'required': True,
                    'summary': 'A tuple of two integers',
                    'type': 'Array',
                }
            ],
            'returns': {
                'description': 'Returns the tuple and 200.',
                'examples': [[[1, 2], 200]],
                'name': 'default',
                'summary': 'A tuple and an integer',
                'type': 'Array',
            },
            'summary': 'This is a tuple type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.typedDictType': {
            'description': 'This method accepts a UserTypedDict and returns it.',
            'examples': [
                {
                    'name': 'Example of typed dict type',
                    'params': [
                        {'description': 'A UserTypedDict.', 'name': 'user', 'value': {'id': 1, 'name': 'Alice'}}
                    ],
                    'returns': {
                        'description': 'The same typed dict returned.',
                        'name': 'result',
                        'value': {'id': 1, 'name': 'Alice'},
                    },
                }
            ],
            'name': 'types.python_stds_annotated.typedDictType',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a UserTypedDict.',
                    'examples': [{'id': 1, 'name': 'Alice'}],
                    'name': 'user',
                    'nullable': False,
                    'properties': {'id': {'name': 'id', 'type': 'Number'}, 'name': {'name': 'name', 'type': 'String'}},
                    'required': True,
                    'summary': 'A UserTypedDict',
                    'type': 'Object',
                }
            ],
            'returns': {
                'description': 'This is the same typed dict returned.',
                'examples': [{'id': 1, 'name': 'Alice'}],
                'name': 'default',
                'properties': {'id': {'name': 'id', 'type': 'Number'}, 'name': {'name': 'name', 'type': 'String'}},
                'summary': 'A UserTypedDict',
                'type': 'Object',
            },
            'summary': 'This is a typed dict type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.union': {
            'description': 'This method accepts a union of int or None and returns it.',
            'examples': [
                {
                    'name': 'Example of union type',
                    'params': [{'description': 'A union of int or None.', 'name': 'n'}],
                    'returns': {'description': 'The same union value returned.', 'name': 'result'},
                }
            ],
            'name': 'types.python_stds_annotated.union',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a union of int or None.',
                    'examples': [None],
                    'name': 'n',
                    'nullable': True,
                    'summary': 'A union of int or None',
                    'type': 'Number',
                }
            ],
            'returns': {
                'description': 'This is the same union value returned.',
                'examples': [None],
                'name': 'default',
                'summary': 'A union of int or None',
                'type': 'Number',
            },
            'summary': 'This is a union type',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'types.python_stds_annotated.unionWithTwoTypes': {
            'description': 'This method accepts a union of int or float and returns it.',
            'examples': [
                {
                    'name': 'Example of union with two types',
                    'params': [{'description': 'A union of int or float.', 'name': 'n', 'value': 42}],
                    'returns': {'description': 'The same union value returned.', 'name': 'result', 'value': 42},
                }
            ],
            'name': 'types.python_stds_annotated.unionWithTwoTypes',
            'notification': True,
            'params': [
                {
                    'description': 'This parameter should be a union of int or float.',
                    'examples': [42],
                    'name': 'n',
                    'nullable': False,
                    'required': True,
                    'summary': 'A union of int or float',
                    'type': 'Number',
                }
            ],
            'returns': {
                'description': 'This is the same union value returned.',
                'examples': [42],
                'name': 'default',
                'summary': 'A union of int or float',
                'type': 'Number',
            },
            'summary': 'This is a union type with two types',
            'tags': ['types'],
            'type': 'method',
            'validation': True,
        },
        'rpc.describe': {
            'name': 'rpc.describe',
            'description': 'Service description for JSON-RPC 2.0',
            'notification': False,
            'params': [],
            'returns': {
                'name': 'default',
                'properties': {
                    'description': {'name': 'description', 'type': 'String'},
                    'id': {'name': 'id', 'type': 'String'},
                    'methods': {'name': 'methods', 'type': 'Null'},
                    'name': {'name': 'name', 'type': 'String'},
                    'servers': {'name': 'servers', 'type': 'Null'},
                    'title': {'name': 'title', 'type': 'String'},
                    'version': {'name': 'version', 'type': 'String'},
                },
                'type': 'Object',
            },
            'summary': 'RPC Describe',
            'type': 'method',
            'validation': False,
        },
    }
