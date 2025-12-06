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
from enum import IntEnum
import typing as t
from decimal import Decimal
from numbers import Number
from collections import OrderedDict, deque, defaultdict

from typing_extensions import Buffer, TypedDict

from flask_jsonrpc import JSONRPCBlueprint

jsonrpc = JSONRPCBlueprint('types__python_stds', __name__)


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


@jsonrpc.method('types.python_stds.boolType')
def bool_type(yes: bool) -> bool:
    return yes


@jsonrpc.method('types.python_stds.strType')
def str_type(st: str) -> str:
    return st


@jsonrpc.method('types.python_stds.bytesType')
def bytes_type(b: bytes) -> bytes:
    return b


@jsonrpc.method('types.python_stds.bytearrayType')
def bytearray_type(b: bytearray) -> bytearray:
    return b


@jsonrpc.method('types.python_stds.bufferType')
def buffer_type(b: Buffer) -> Buffer:
    return b


@jsonrpc.method('types.python_stds.intType')
def int_type(n: int) -> int:
    return n


@jsonrpc.method('types.python_stds.floatType')
def float_type(n: float) -> float:
    return n


@jsonrpc.method('types.python_stds.numberType')
def number_type(n: Number) -> Number:
    return n


@jsonrpc.method('types.python_stds.intEnumType')
def enum_int_type(e: ColorIntEnum) -> ColorIntEnum:
    return e


@jsonrpc.method('types.python_stds.decimalType')
def decimal_type(n: Decimal) -> Decimal:
    return n


@jsonrpc.method('types.python_stds.listType')
def list_type(lst: list[int]) -> list[int]:
    return lst


@jsonrpc.method('types.python_stds.tupleType')
def tuple_type(tn: tuple[int, int]) -> tuple[tuple[int, int], int]:
    return tn, 200


@jsonrpc.method('types.python_stds.namedtupleType')
def namedtuple_type(tn: EmployeeNamedTuple) -> tuple[EmployeeNamedTuple, int]:
    return tn, 200


@jsonrpc.method('types.python_stds.setType')
def set_type(s: set[int]) -> set[int]:
    return s


@jsonrpc.method('types.python_stds.frozensetType')
def fronzenset_type(s: frozenset[int]) -> frozenset[int]:
    return s


@jsonrpc.method('types.python_stds.setAbcType')
def set_abc_type(s: t.Set[int]) -> t.Set[int]:  # noqa: UP006
    return s


@jsonrpc.method('types.python_stds.mutableSetType')
def mutable_set_type(s: t.MutableSet[int]) -> t.MutableSet[int]:
    return s


@jsonrpc.method('types.python_stds.dequeType')
def deque_type(d: deque[int]) -> deque[int]:
    return d


@jsonrpc.method('types.python_stds.sequenceType')
def sequence_type(s: t.Sequence[int]) -> t.Sequence[int]:
    return s


@jsonrpc.method('types.python_stds.mutableSequenceType')
def mutable_sequence_type(s: t.MutableSequence[int]) -> t.MutableSequence[int]:
    return s


@jsonrpc.method('types.python_stds.collectionType')
def collection_type(s: t.Collection[int]) -> t.Collection[int]:
    return s


@jsonrpc.method('types.python_stds.dictType')
def dict_type(d: dict[str, int]) -> dict[str, int]:
    return d


@jsonrpc.method('types.python_stds.orderedDictType')
def ordered_dict_type(d: OrderedDict[str, int]) -> OrderedDict[str, int]:
    return d


@jsonrpc.method('types.python_stds.defaultdictType')
def defaultdict_type(d: defaultdict[str, int]) -> defaultdict[str, int]:
    return d


@jsonrpc.method('types.python_stds.mappingType')
def mapping_type(d: t.Mapping[str, int]) -> t.Mapping[str, int]:
    return d


@jsonrpc.method('types.python_stds.mutableMappingType')
def mutable_mapping_type(d: t.MutableMapping[str, int]) -> t.MutableMapping[str, int]:
    return d


@jsonrpc.method('types.python_stds.typedDictType')
def typeddict_type(user: UserTypedDict) -> UserTypedDict:
    return user


@jsonrpc.method('types.python_stds.optional')
def optional(n: int | None = None) -> int | None:
    return n


@jsonrpc.method('types.python_stds.unionWithTwoTypes')
def union_with_two_types(n: int | float) -> int | float:
    return n


@jsonrpc.method('types.python_stds.unionWithTwoTypesAndNone')
def union_with_two_types_and_none(n: int | float | None = None) -> int | float | None:
    return n


@jsonrpc.method('types.python_stds.literalType')
def literal_type(x: t.Literal['X']) -> t.Literal['X']:
    return x


@jsonrpc.method('types.python_stds.finalType')
def final_type(x: t.Final[str] = 'FinalValue') -> t.Final[str]:  # type: ignore
    return x


@jsonrpc.method('types.python_stds.anyType')
def any_type(obj: t.Any) -> t.Any:  # noqa: ANN401
    return obj


@jsonrpc.method('types.python_stds.noneType')
def none_type(obj: None = None) -> None:  # noqa: ANN401
    return obj


@jsonrpc.method('types.python_stds.noReturnType')
def no_return_type(s: str) -> t.NoReturn:  # noqa: ANN401
    raise ValueError(s)


@jsonrpc.method('types.python_stds.literalNoneType')
def literal_none_type(x: t.Literal[None] = None) -> t.Literal[None]:  # noqa: ANN401
    return x
