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
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
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
from enum import IntEnum
import typing as t
from decimal import Decimal
from collections import deque

from typing_extensions import TypedDict

from flask_jsonrpc import JSONRPCBlueprint
import flask_jsonrpc.types.params as tp
import flask_jsonrpc.types.methods as tm

jsonrpc = JSONRPCBlueprint('types__python_stds_annotated', __name__)


class ColorIntEnum(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3


class UserTypedDict(TypedDict):
    name: str
    id: int


class EmployeeNamedTuple(t.NamedTuple):
    name: str
    id: int = 3


@jsonrpc.method(
    'types.python_stds_annotated.boolType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a boolean type'),
        tm.Description('This method accepts a boolean value and returns it.'),
        tm.Tag(
            name='types', summary='Types related methods', description='Methods that demonstrate various Python types.'
        ),
        tm.Error(code=-32000, message='The value must be a boolean.', status_code=500),
        tm.Example(
            name='Example of boolean type',
            summary='An example of a boolean type',
            description='This method demonstrates how to use a boolean type in JSON-RPC.',
            params=[tm.ExampleField(name='yes', value=True, description='A boolean value that is True.')],
            returns=tm.ExampleField(name='result', value=True, description='The same boolean value returned.'),
        ),
    ],
)
def bool_type(
    yes: t.Annotated[
        bool,
        tp.Summary('A boolean value'),
        tp.Description('This parameter should be a boolean value.'),
        tp.Example(name='yes', value=True),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    bool,
    tp.Summary('A boolean value'),
    tp.Description('This is the same boolean value returned.'),
    tp.Example(name='result', value=True),
]:
    return yes


@jsonrpc.method(
    'types.python_stds_annotated.strType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a string type'),
        tm.Description('This method accepts a string value and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of string type',
            params=[tm.ExampleField(name='st', value='Hello', description='A string value.')],
            returns=tm.ExampleField(name='result', value='Hello', description='The same string value returned.'),
        ),
    ],
)
def str_type(
    st: t.Annotated[
        str,
        tp.Summary('A string value'),
        tp.Description('This parameter should be a string value.'),
        tp.Example(name='st', value='Hello'),
        tp.Required(True),
        tp.Nullable(False),
        tp.MinLength(1),
        tp.MaxLength(100),
    ],
) -> t.Annotated[
    str,
    tp.Summary('A string value'),
    tp.Description('This is the same string value returned.'),
    tp.Example(name='result', value='Hello'),
]:
    return st


@jsonrpc.method(
    'types.python_stds_annotated.bytesType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a bytes type'),
        tm.Description('This method accepts a bytes value and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of bytes type',
            params=[tm.ExampleField(name='b', value='Hello', description='A bytes value.')],
            returns=tm.ExampleField(name='result', value='Hello', description='The same bytes value returned.'),
        ),
    ],
)
def bytes_type(
    b: t.Annotated[
        bytes,
        tp.Summary('A bytes value'),
        tp.Description('This parameter should be a bytes value.'),
        tp.Example(name='b', value='Hello'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    bytes,
    tp.Summary('A bytes value'),
    tp.Description('This is the same bytes value returned.'),
    tp.Example(name='result', value='Hello'),
]:
    return b


@jsonrpc.method(
    'types.python_stds_annotated.bytearrayType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a bytearray type'),
        tm.Description('This method accepts a bytearray value and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of bytearray type',
            params=[tm.ExampleField(name='b', value='Hello', description='A bytearray value.')],
            returns=tm.ExampleField(name='result', value='Hello', description='The same bytearray value returned.'),
        ),
    ],
)
def bytearray_type(
    b: t.Annotated[
        bytearray,
        tp.Summary('A bytearray value'),
        tp.Description('This parameter should be a bytearray value.'),
        tp.Example(name='b', value='Hello'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    bytearray,
    tp.Summary('A bytearray value'),
    tp.Description('This is the same bytearray value returned.'),
    tp.Example(name='result', value='Hello'),
]:
    return b


@jsonrpc.method(
    'types.python_stds_annotated.intType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is an int type'),
        tm.Description('This method accepts an int value and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of int type',
            params=[tm.ExampleField(name='n', value=42, description='An integer value.')],
            returns=tm.ExampleField(name='result', value=42, description='The same integer value returned.'),
        ),
    ],
)
def int_type(
    n: t.Annotated[
        int,
        tp.Summary('An integer value'),
        tp.Description('This parameter should be an integer value.'),
        tp.Example(name='n', value=42),
        tp.MaxDigits(10),
        tp.Maximum(1000000),
        tp.Minimum(0),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    int,
    tp.Summary('An integer value'),
    tp.Description('This is the same integer value returned.'),
    tp.Example(name='result', value=42),
]:
    return n


@jsonrpc.method(
    'types.python_stds_annotated.floatType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a float type'),
        tm.Description('This method accepts a float value and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of float type',
            params=[tm.ExampleField(name='n', value=3.14, description='A float value.')],
            returns=tm.ExampleField(name='result', value=3.14, description='The same float value returned.'),
        ),
    ],
)
def float_type(
    n: t.Annotated[
        float,
        tp.Summary('A float value'),
        tp.Description('This parameter should be a float value.'),
        tp.Example(name='n', value=3.14),
        tp.Required(True),
        tp.Nullable(False),
        tp.DecimalPlaces(2),
    ],
) -> t.Annotated[
    float,
    tp.Summary('A float value'),
    tp.Description('This is the same float value returned.'),
    tp.Example(name='result', value=3.14),
]:
    return n


@jsonrpc.method(
    'types.python_stds_annotated.intEnumType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is an int enum type'),
        tm.Description('This method accepts a ColorIntEnum value and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of int enum type',
            params=[tm.ExampleField(name='e', value=1, description='A ColorIntEnum value.')],
            returns=tm.ExampleField(name='result', value=1, description='The same enum value returned.'),
        ),
    ],
)
def enum_int_type(
    e: t.Annotated[
        ColorIntEnum,
        tp.Summary('A ColorIntEnum value'),
        tp.Description('This parameter should be a ColorIntEnum value.'),
        tp.Example(name='e', value=1),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    ColorIntEnum,
    tp.Summary('A ColorIntEnum value'),
    tp.Description('This is the same enum value returned.'),
    tp.Example(name='result', value=1),
]:
    return e


@jsonrpc.method(
    'types.python_stds_annotated.decimalType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a decimal type'),
        tm.Description('This method accepts a Decimal value and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of decimal type',
            params=[tm.ExampleField(name='n', value='1.5', description='A decimal value.')],
            returns=tm.ExampleField(name='result', value='1.5', description='The same decimal value returned.'),
        ),
    ],
)
def decimal_type(
    n: t.Annotated[
        Decimal,
        tp.Summary('A decimal value'),
        tp.Description('This parameter should be a decimal value.'),
        tp.Example(name='n', value='1.5'),
        tp.Required(True),
        tp.Nullable(False),
        tp.DecimalPlaces(2),
    ],
) -> t.Annotated[
    Decimal,
    tp.Summary('A decimal value'),
    tp.Description('This is the same decimal value returned.'),
    tp.Example(name='result', value='1.5'),
]:
    return n


@jsonrpc.method(
    'types.python_stds_annotated.listType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a list type'),
        tm.Description('This method accepts a list of integers and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of list type',
            params=[tm.ExampleField(name='lst', value=[1, 2, 3], description='A list of integers.')],
            returns=tm.ExampleField(name='result', value=[1, 2, 3], description='The same list returned.'),
        ),
    ],
)
def list_type(
    lst: t.Annotated[
        list[int],
        tp.Summary('A list of integers'),
        tp.Description('This parameter should be a list of integers.'),
        tp.Example(name='lst', value=[1, 2, 3]),
        tp.Required(True),
        tp.Nullable(False),
        tp.MaxLength(100),
        tp.MinLength(1),
    ],
) -> t.Annotated[
    list[int],
    tp.Summary('A list of integers'),
    tp.Description('This is the same list returned.'),
    tp.Example(name='result', value=[1, 2, 3]),
]:
    return lst


@jsonrpc.method(
    'types.python_stds_annotated.tupleType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a tuple type'),
        tm.Description('This method accepts a tuple of two integers and returns it with 200.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of tuple type',
            params=[tm.ExampleField(name='tn', value=[1, 2], description='A tuple of two integers.')],
            returns=tm.ExampleField(name='result', value=[[1, 2], 200], description='The tuple and 200 returned.'),
        ),
    ],
)
def tuple_type(
    tn: t.Annotated[
        tuple[int, int],
        tp.Summary('A tuple of two integers'),
        tp.Description('This parameter should be a tuple of two integers.'),
        tp.Example(name='tn', value=[1, 2]),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    tuple[tuple[int, int], int],
    tp.Summary('A tuple and an integer'),
    tp.Description('Returns the tuple and 200.'),
    tp.Example(name='result', value=[[1, 2], 200]),
]:
    return tn, 200


@jsonrpc.method(
    'types.python_stds_annotated.namedtupleType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a named tuple type'),
        tm.Description('This method accepts an EmployeeNamedTuple and returns it with 200.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of namedtuple type',
            params=[tm.ExampleField(name='tn', value={'name': 'Alice', 'id': 1}, description='An EmployeeNamedTuple.')],
            returns=tm.ExampleField(
                name='result', value=[['Alice', 1], 200], description='The namedtuple and 200 returned.'
            ),
        ),
    ],
)
def namedtuple_type(
    tn: t.Annotated[
        EmployeeNamedTuple,
        tp.Summary('An EmployeeNamedTuple'),
        tp.Description('This parameter should be an EmployeeNamedTuple.'),
        tp.Example(name='tn', value={'name': 'Alice', 'id': 1}),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    tuple[EmployeeNamedTuple, int],
    tp.Summary('A tuple of EmployeeNamedTuple and int'),
    tp.Description('Returns the namedtuple and 200.'),
    tp.Example(name='result', value=[['Alice', 1], 200]),
]:
    return tn, 200


@jsonrpc.method(
    'types.python_stds_annotated.setType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a set type'),
        tm.Description('This method accepts a set of integers and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of set type',
            params=[tm.ExampleField(name='s', value=[1, 2, 3], description='A set of integers.')],
            returns=tm.ExampleField(name='result', value=[1, 2, 3], description='The same set returned.'),
        ),
    ],
)
def set_type(
    s: t.Annotated[
        set[int],
        tp.Summary('A set of integers'),
        tp.Description('This parameter should be a set of integers.'),
        tp.Example(name='s', value=[1, 2, 3]),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    set[int],
    tp.Summary('A set of integers'),
    tp.Description('This is the same set returned.'),
    tp.Example(name='result', value=[1, 2, 3]),
]:
    return s


@jsonrpc.method(
    'types.python_stds_annotated.frozensetType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a frozenset type'),
        tm.Description('This method accepts a frozenset of integers and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of frozenset type',
            params=[tm.ExampleField(name='s', value=[1, 2, 3], description='A frozenset of integers.')],
            returns=tm.ExampleField(name='result', value=[1, 2, 3], description='The same frozenset returned.'),
        ),
    ],
)
def frozenset_type(
    s: t.Annotated[
        frozenset[int],
        tp.Summary('A frozenset of integers'),
        tp.Description('This parameter should be a frozenset of integers.'),
        tp.Example(name='s', value=[1, 2, 3]),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    frozenset[int],
    tp.Summary('A frozenset of integers'),
    tp.Description('This is the same frozenset returned.'),
    tp.Example(name='result', value=[1, 2, 3]),
]:
    return s


@jsonrpc.method(
    'types.python_stds_annotated.dequeType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a deque type'),
        tm.Description('This method accepts a deque of integers and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of deque type',
            params=[tm.ExampleField(name='d', value=[1, 2, 3], description='A deque of integers.')],
            returns=tm.ExampleField(name='result', value=[1, 2, 3], description='The same deque returned.'),
        ),
    ],
)
def deque_type(
    d: t.Annotated[
        deque[int],
        tp.Summary('A deque of integers'),
        tp.Description('This parameter should be a deque of integers.'),
        tp.Example(name='d', value=[1, 2, 3]),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    deque[int],
    tp.Summary('A deque of integers'),
    tp.Description('This is the same deque returned.'),
    tp.Example(name='result', value=[1, 2, 3]),
]:
    return d


@jsonrpc.method(
    'types.python_stds_annotated.sequenceType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a sequence type'),
        tm.Description('This method accepts a sequence of integers and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of sequence type',
            params=[tm.ExampleField(name='s', value=[1, 2, 3], description='A sequence of integers.')],
            returns=tm.ExampleField(name='result', value=[1, 2, 3], description='The same sequence returned.'),
        ),
    ],
)
def sequence_type(
    s: t.Annotated[
        t.Sequence[int],
        tp.Summary('A sequence of integers'),
        tp.Description('This parameter should be a sequence of integers.'),
        tp.Example(name='s', value=[1, 2, 3]),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    t.Sequence[int],
    tp.Summary('A sequence of integers'),
    tp.Description('This is the same sequence returned.'),
    tp.Example(name='result', value=[1, 2, 3]),
]:
    return s


@jsonrpc.method(
    'types.python_stds_annotated.dictType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a dict type'),
        tm.Description('This method accepts a dict of str to int and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of dict type',
            params=[tm.ExampleField(name='d', value={'key': 1}, description='A dict of str to int.')],
            returns=tm.ExampleField(name='result', value={'key': 1}, description='The same dict returned.'),
        ),
    ],
)
def dict_type(
    d: t.Annotated[
        dict[str, int],
        tp.Summary('A dict of str to int'),
        tp.Description('This parameter should be a dict of str to int.'),
        tp.Example(name='d', value={'key': 1}),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    dict[str, int],
    tp.Summary('A dict of str to int'),
    tp.Description('This is the same dict returned.'),
    tp.Example(name='result', value={'key': 1}),
]:
    return d


@jsonrpc.method(
    'types.python_stds_annotated.typedDictType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a typed dict type'),
        tm.Description('This method accepts a UserTypedDict and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of typed dict type',
            params=[tm.ExampleField(name='user', value={'name': 'Alice', 'id': 1}, description='A UserTypedDict.')],
            returns=tm.ExampleField(
                name='result', value={'name': 'Alice', 'id': 1}, description='The same typed dict returned.'
            ),
        ),
    ],
)
def typeddict_type(
    user: t.Annotated[
        UserTypedDict,
        tp.Summary('A UserTypedDict'),
        tp.Description('This parameter should be a UserTypedDict.'),
        tp.Example(name='user', value={'name': 'Alice', 'id': 1}),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    UserTypedDict,
    tp.Summary('A UserTypedDict'),
    tp.Description('This is the same typed dict returned.'),
    tp.Example(name='result', value={'name': 'Alice', 'id': 1}),
]:
    return user


@jsonrpc.method(
    'types.python_stds_annotated.optional',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is an optional type'),
        tm.Description('This method accepts an optional integer and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of optional type',
            params=[tm.ExampleField(name='n', value=None, description='An optional integer.')],
            returns=tm.ExampleField(name='result', value=None, description='The same optional value returned.'),
        ),
    ],
)
def optional(
    n: t.Annotated[
        int | None,
        tp.Summary('An optional integer'),
        tp.Description('This parameter should be an optional integer.'),
        tp.Example(name='n', value=None),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    int | None,
    tp.Summary('An optional integer'),
    tp.Description('This is the same optional value returned.'),
    tp.Example(name='result', value=None),
]:
    return n


@jsonrpc.method(
    'types.python_stds_annotated.union',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a union type'),
        tm.Description('This method accepts a union of int or None and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of union type',
            params=[tm.ExampleField(name='n', value=None, description='A union of int or None.')],
            returns=tm.ExampleField(name='result', value=None, description='The same union value returned.'),
        ),
    ],
)
def union(
    n: t.Annotated[
        int | None,
        tp.Summary('A union of int or None'),
        tp.Description('This parameter should be a union of int or None.'),
        tp.Example(name='n', value=None),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    int | None,
    tp.Summary('A union of int or None'),
    tp.Description('This is the same union value returned.'),
    tp.Example(name='result', value=None),
]:
    return n


@jsonrpc.method(
    'types.python_stds_annotated.unionWithTwoTypes',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a union type with two types'),
        tm.Description('This method accepts a union of int or float and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of union with two types',
            params=[tm.ExampleField(name='n', value=42, description='A union of int or float.')],
            returns=tm.ExampleField(name='result', value=42, description='The same union value returned.'),
        ),
    ],
)
def union_with_two_types(
    n: t.Annotated[
        int | float,
        tp.Summary('A union of int or float'),
        tp.Description('This parameter should be a union of int or float.'),
        tp.Example(name='n', value=42),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    int | float,
    tp.Summary('A union of int or float'),
    tp.Description('This is the same union value returned.'),
    tp.Example(name='result', value=42),
]:
    return n


@jsonrpc.method(
    'types.python_stds_annotated.literalType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a literal type'),
        tm.Description('This method accepts a literal value "X" and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of literal type',
            params=[tm.ExampleField(name='x', value='X', description='A literal value "X".')],
            returns=tm.ExampleField(name='result', value='X', description='The same literal value returned.'),
        ),
    ],
)
def literal_type(
    x: t.Annotated[
        t.Literal['X'],
        tp.Summary('A literal value "X"'),
        tp.Description('This parameter should be a literal value "X".'),
        tp.Example(name='x', value='X'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    t.Literal['X'],
    tp.Summary('A literal value "X"'),
    tp.Description('This is the same literal value returned.'),
    tp.Example(name='result', value='X'),
]:
    return x


@jsonrpc.method(
    'types.python_stds_annotated.noneType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a none type'),
        tm.Description('This method accepts None and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of none type',
            params=[tm.ExampleField(name='obj', value=None, description='A None value.')],
            returns=tm.ExampleField(name='result', value=None, description='The same None value returned.'),
        ),
    ],
)
def none_type(
    obj: t.Annotated[
        None,
        tp.Summary('A None value'),
        tp.Description('This parameter should be None.'),
        tp.Example(name='obj', value=None),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    None,
    tp.Summary('A None value'),
    tp.Description('This is the same None value returned.'),
    tp.Example(name='result', value=None),
]:
    return obj


@jsonrpc.method(
    'types.python_stds_annotated.noReturnType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a no return type'),
        tm.Description('This method always raises an error.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of no return type',
            params=[tm.ExampleField(name='s', value='no return', description='A string value.')],
            returns=tm.ExampleField(name='result', value=None, description='No return value.'),
        ),
    ],
)
def no_return_type(
    s: t.Annotated[
        str,
        tp.Summary('A string value'),
        tp.Description('This parameter should be a string value.'),
        tp.Example(name='s', value='no return'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    t.NoReturn,
    tp.Summary('No return value'),
    tp.Description('This method does not return.'),
    tp.Example(name='result', value=None),
]:
    raise ValueError(s)


@jsonrpc.method(
    'types.python_stds_annotated.literalNoneType',
    annotation=tm.MethodAnnotated[
        tm.Summary('This is a literal none type'),
        tm.Description('This method accepts a literal None and returns it.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of literal none type',
            params=[tm.ExampleField(name='x', value=None, description='A literal None value.')],
            returns=tm.ExampleField(name='result', value=None, description='The same literal None value returned.'),
        ),
    ],
)
def literal_none_type(
    x: t.Annotated[
        t.Literal[None],
        tp.Summary('A literal None value'),
        tp.Description('This parameter should be a literal None value.'),
        tp.Example(name='x', value=None),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    t.Literal[None],
    tp.Summary('A literal None value'),
    tp.Description('This is the same literal None value returned.'),
    tp.Example(name='result', value=None),
]:
    return x
