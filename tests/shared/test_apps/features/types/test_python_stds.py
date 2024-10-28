# Copyright (c) 2024-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
        f'{api_url}/types/python-stds', json={'jsonrpc': '2.0', 'method': 'jsonrpc.boolType', 'params': [True], 'id': 1}
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': True, 'id': 1}


def test_str_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.strType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_bytes_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.bytesType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_bytearray_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.bytearrayType', 'params': ['Hello'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'Hello', 'id': 1}


def test_int_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds', json={'jsonrpc': '2.0', 'method': 'jsonrpc.intType', 'params': [42], 'id': 1}
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 42, 'id': 1}


def test_float_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.floatType', 'params': [3.14], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 3.14, 'id': 1}


def test_enum_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds', json={'jsonrpc': '2.0', 'method': 'jsonrpc.intEnumType', 'params': [1], 'id': 1}
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 1, 'id': 1}


def test_decimal_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.decimalType', 'params': [1.5], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': '1.5', 'id': 1}


def test_list_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.listType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_tuple_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.tupleType', 'params': [[1, 2]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2], 'id': 1}


def test_namedtuple_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.namedtupleType', 'params': [{'name': 'Alice', 'id': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': ['Alice', 1], 'id': 1}


def test_set_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.setType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_frozenset_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.frozensetType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_deque_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.dequeType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_sequence_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.sequenceType', 'params': [[1, 2, 3]], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': [1, 2, 3], 'id': 1}


def test_dict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.dictType', 'params': [{'key': 1}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 1}, 'id': 1}


def test_typedict_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.typedDictType', 'params': [{'name': 'Alice', 'id': 1}], 'id': 1},
    )
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': {'id': 1, 'name': 'Alice'}}


def test_optional(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds', json={'jsonrpc': '2.0', 'method': 'jsonrpc.optional', 'params': [None], 'id': 1}
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}

    rv = session.post(
        f'{api_url}/types/python-stds', json={'jsonrpc': '2.0', 'method': 'jsonrpc.optional', 'params': [1], 'id': 1}
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 1, 'id': 1}


def test_union_with_two_types(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.unionWithTwoTypes', 'params': [42], 'id': 1},
    )
    assert rv.json() == {
        'jsonrpc': '2.0',
        'id': 1,
        'error': {
            'code': -32602,
            'data': {
                'message': 'the only type of union that is supported is: typing.Union[T, ' 'None] or typing.Optional[T]'
            },
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }

    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.unionWithTwoTypes', 'params': [3.14], 'id': 1},
    )
    assert rv.json() == {
        'jsonrpc': '2.0',
        'id': 1,
        'error': {
            'code': -32602,
            'data': {
                'message': 'the only type of union that is supported is: typing.Union[T, ' 'None] or typing.Optional[T]'
            },
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }


def test_union_with_two_types_and_none(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.unionWithTwoTypesAndNone', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_literal_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.literalType', 'params': ['X'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'X', 'id': 1}


def test_final_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.finalType', 'params': ['FinalValue'], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': 'FinalValue', 'id': 1}


def test_any_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.anyType', 'params': [{'key': 'value'}], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': {'key': 'value'}, 'id': 1}


def test_none_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds', json={'jsonrpc': '2.0', 'method': 'jsonrpc.noneType', 'params': [None], 'id': 1}
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_no_return_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.noReturnType', 'params': ['no return'], 'id': 1},
    )
    assert rv.json() == {
        'jsonrpc': '2.0',
        'id': 1,
        'error': {'code': -32000, 'data': {'message': 'no return'}, 'message': 'Server error', 'name': 'ServerError'},
    }


def test_literal_none_type(session: 'Session', api_url: str) -> None:
    rv = session.post(
        f'{api_url}/types/python-stds',
        json={'jsonrpc': '2.0', 'method': 'jsonrpc.literalNoneType', 'params': [None], 'id': 1},
    )
    assert rv.json() == {'jsonrpc': '2.0', 'result': None, 'id': 1}


def test_app_system_describe(session: 'Session', api_url: str) -> None:
    rv = session.post(f'{api_url}/types/python-stds', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.describe'})
    data = rv.json()
    assert data['id'] == 1
    assert data['jsonrpc'] == '2.0'
    assert data['result']['name'] == 'Flask-JSONRPC'
    assert data['result']['version'] == '2.0'
    assert data['result']['servers'] is not None
    assert 'url' in data['result']['servers'][0]
    assert data['result']['methods'] == {
        'jsonrpc.anyType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'obj', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.boolType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'yes', 'type': 'Boolean'}],
            'returns': {'type': 'Boolean'},
            'type': 'method',
        },
        'jsonrpc.bytearrayType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'b', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.bytesType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'b', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.decimalType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.dequeType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'd', 'type': 'Array'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.dictType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'd', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.finalType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'x', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.floatType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'jsonrpc.frozensetType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.intEnumType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'e', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.intType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'jsonrpc.listType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'lst', 'type': 'Array'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.literalNoneType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'x', 'type': 'Null'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'jsonrpc.literalType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'x', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.namedtupleType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'tn', 'type': 'Object'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.noReturnType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'jsonrpc.noneType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'obj', 'type': 'Null'}],
            'returns': {'type': 'Null'},
            'type': 'method',
        },
        'jsonrpc.optional': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'jsonrpc.sequenceType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.setType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 's', 'type': 'Array'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.strType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'st', 'type': 'String'}],
            'returns': {'type': 'String'},
            'type': 'method',
        },
        'jsonrpc.tupleType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'tn', 'type': 'Array'}],
            'returns': {'type': 'Array'},
            'type': 'method',
        },
        'jsonrpc.typedDictType': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'user', 'type': 'Object'}],
            'returns': {'type': 'Object'},
            'type': 'method',
        },
        'jsonrpc.unionWithTwoTypes': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'jsonrpc.unionWithTwoTypesAndNone': {
            'options': {'notification': True, 'validate': True},
            'params': [{'name': 'n', 'type': 'Number'}],
            'returns': {'type': 'Number'},
            'type': 'method',
        },
        'rpc.describe': {'options': {}, 'params': [], 'returns': {'type': 'Object'}, 'type': 'method'},
    }
