# Copyright (c) 2024-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.boolType', 'params': [True], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': True, 'id': 1}


def test_str_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.strType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_bytes_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.bytesType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_bytearray_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.bytearrayType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_int_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.intType', 'params': [42], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 42, 'id': 1}


def test_float_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.floatType', 'params': [3.14], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 3.14, 'id': 1}


def test_enum_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.intEnumType', 'params': [1], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 1, 'id': 1}


def test_decimal_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.decimalType', 'params': [1.5], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': '1.5', 'id': 1}

    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.decimalType', 'params': [3.14], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': '3.14', 'id': 1}

    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.decimalType', 'params': [123.45], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': '123.45', 'id': 1}

    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.decimalType', 'params': ['123.45'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': '123.45', 'id': 1}


def test_list_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.listType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_tuple_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.tupleType', 'params': [[1, 2]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2], 'id': 1}


def test_namedtuple_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={
            'jsonrpc': '2.0',
            'method': 'types.python_stds.namedtupleType',
            'params': [{'name': 'Alice', 'id': 1}],
            'id': 1,
        },
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': ['Alice', 1], 'id': 1}


def test_set_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.setType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_frozenset_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.frozensetType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_deque_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.dequeType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_sequence_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.sequenceType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_dict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.dictType', 'params': [{'key': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 1}, 'id': 1}


def test_typedict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={
            'jsonrpc': '2.0',
            'method': 'types.python_stds.typedDictType',
            'params': [{'name': 'Alice', 'id': 1}],
            'id': 1,
        },
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Alice'}}


def test_optional(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.optional', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}

    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.optional', 'params': [1], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 1, 'id': 1}


def test_union_with_two_types(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.unionWithTwoTypes', 'params': [42], 'id': 1},
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

    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.unionWithTwoTypes', 'params': [3.14], 'id': 1},
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


def test_union_with_two_types_and_none(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.unionWithTwoTypesAndNone', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_literal_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.literalType', 'params': ['X'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'X', 'id': 1}


def test_final_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.finalType', 'params': ['FinalValue'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'FinalValue', 'id': 1}


def test_any_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.anyType', 'params': [{'key': 'value'}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 'value'}, 'id': 1}


def test_none_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.noneType', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_no_return_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.noReturnType', 'params': ['no return'], 'id': 1},
    )
    assert rv.json() == {
        'jsonrpc': '2.0',
        'id': 1,
        'error': {'code': -32000, 'data': {'message': 'no return'}, 'message': 'Server error', 'name': 'ServerError'},
    }


def test_literal_none_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.literalNoneType', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_buffer_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.bufferType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_number_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.numberType', 'params': [42], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 42, 'id': 1}


def test_set_abc_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.setAbcType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_mutable_set_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.mutableSetType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_mutable_sequence_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.mutableSequenceType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_collection_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.collectionType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_ordered_dict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.orderedDictType', 'params': [{'key': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 1}, 'id': 1}


def test_defaultdict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.defaultdictType', 'params': [{'key': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 1}, 'id': 1}


def test_mapping_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.mappingType', 'params': [{'key': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 1}, 'id': 1}


def test_mutable_mapping_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'types.python_stds.mutableMappingType', 'params': [{'key': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 1}, 'id': 1}


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/types/python-stds', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '1.0.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'types.python_stds.anyType': {
            'name': 'types.python_stds.anyType',
            'notification': True,
            'params': [{'name': 'obj', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.boolType': {
            'name': 'types.python_stds.boolType',
            'notification': True,
            'params': [{'name': 'yes', 'type': 'Boolean'}],
            'returns': {'name': 'default', 'type': 'Boolean'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.bufferType': {
            'name': 'types.python_stds.bufferType',
            'notification': True,
            'params': [{'name': 'b', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.bytearrayType': {
            'name': 'types.python_stds.bytearrayType',
            'notification': True,
            'params': [{'name': 'b', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.bytesType': {
            'name': 'types.python_stds.bytesType',
            'notification': True,
            'params': [{'name': 'b', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.collectionType': {
            'name': 'types.python_stds.collectionType',
            'notification': True,
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.decimalType': {
            'name': 'types.python_stds.decimalType',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.defaultdictType': {
            'name': 'types.python_stds.defaultdictType',
            'notification': True,
            'params': [{'name': 'd', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.dequeType': {
            'name': 'types.python_stds.dequeType',
            'notification': True,
            'params': [{'name': 'd', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.dictType': {
            'name': 'types.python_stds.dictType',
            'notification': True,
            'params': [{'name': 'd', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.finalType': {
            'name': 'types.python_stds.finalType',
            'notification': True,
            'params': [{'name': 'x', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.floatType': {
            'name': 'types.python_stds.floatType',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.frozensetType': {
            'name': 'types.python_stds.frozensetType',
            'notification': True,
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.intEnumType': {
            'name': 'types.python_stds.intEnumType',
            'notification': True,
            'params': [{'name': 'e', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.intType': {
            'name': 'types.python_stds.intType',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.listType': {
            'name': 'types.python_stds.listType',
            'notification': True,
            'params': [{'name': 'lst', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.literalNoneType': {
            'name': 'types.python_stds.literalNoneType',
            'notification': True,
            'params': [{'name': 'x', 'type': 'Null'}],
            'returns': {'name': 'default', 'type': 'Null'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.literalType': {
            'name': 'types.python_stds.literalType',
            'notification': True,
            'params': [{'name': 'x', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.mappingType': {
            'name': 'types.python_stds.mappingType',
            'notification': True,
            'params': [{'name': 'd', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.mutableMappingType': {
            'name': 'types.python_stds.mutableMappingType',
            'notification': True,
            'params': [{'name': 'd', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.mutableSequenceType': {
            'name': 'types.python_stds.mutableSequenceType',
            'notification': True,
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.mutableSetType': {
            'name': 'types.python_stds.mutableSetType',
            'notification': True,
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.namedtupleType': {
            'name': 'types.python_stds.namedtupleType',
            'notification': True,
            'params': [
                {
                    'name': 'tn',
                    'properties': {'id': {'name': 'id', 'type': 'Number'}, 'name': {'name': 'name', 'type': 'String'}},
                    'type': 'Object',
                }
            ],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.noReturnType': {
            'name': 'types.python_stds.noReturnType',
            'notification': True,
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'Null'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.noneType': {
            'name': 'types.python_stds.noneType',
            'notification': True,
            'params': [{'name': 'obj', 'type': 'Null'}],
            'returns': {'name': 'default', 'type': 'Null'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.numberType': {
            'name': 'types.python_stds.numberType',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.optional': {
            'name': 'types.python_stds.optional',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.orderedDictType': {
            'name': 'types.python_stds.orderedDictType',
            'notification': True,
            'params': [{'name': 'd', 'type': 'Object'}],
            'returns': {'name': 'default', 'type': 'Object'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.sequenceType': {
            'name': 'types.python_stds.sequenceType',
            'notification': True,
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.setAbcType': {
            'name': 'types.python_stds.setAbcType',
            'notification': True,
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.setType': {
            'name': 'types.python_stds.setType',
            'notification': True,
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.strType': {
            'name': 'types.python_stds.strType',
            'notification': True,
            'params': [{'name': 'st', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.tupleType': {
            'name': 'types.python_stds.tupleType',
            'notification': True,
            'params': [{'name': 'tn', 'type': 'Array'}],
            'returns': {'name': 'default', 'type': 'Array'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.typedDictType': {
            'name': 'types.python_stds.typedDictType',
            'notification': True,
            'params': [
                {
                    'name': 'user',
                    'properties': {'id': {'name': 'id', 'type': 'Number'}, 'name': {'name': 'name', 'type': 'String'}},
                    'type': 'Object',
                }
            ],
            'returns': {
                'name': 'default',
                'properties': {'id': {'name': 'id', 'type': 'Number'}, 'name': {'name': 'name', 'type': 'String'}},
                'type': 'Object',
            },
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.unionWithTwoTypes': {
            'name': 'types.python_stds.unionWithTwoTypes',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
            'type': 'method',
            'validation': True,
        },
        'types.python_stds.unionWithTwoTypesAndNone': {
            'name': 'types.python_stds.unionWithTwoTypesAndNone',
            'notification': True,
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'name': 'default', 'type': 'Number'},
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
