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
from enum import IntEnum
import typing as t
from decimal import Decimal
from collections import deque

from typing_extensions import Literal, TypedDict

from flask_jsonrpc import JSONRPCBlueprint

jsonrpc = JSONRPCBlueprint('types__python_types', __name__)


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


@jsonrpc.method('jsonrpc.boolType')
def bool_type(yes: bool) -> bool:
    return yes


@jsonrpc.method('jsonrpc.strType')
def str_type(st: str) -> str:
    return st


@jsonrpc.method('jsonrpc.bytesType')
def bytes_type(b: bytes) -> bytes:
    return b


@jsonrpc.method('jsonrpc.bytearrayType')
def bytearray_type(b: bytearray) -> bytearray:
    return b


@jsonrpc.method('jsonrpc.intType')
def int_type(n: int) -> int:
    return n


@jsonrpc.method('jsonrpc.floatType')
def float_type(n: float) -> float:
    return n


@jsonrpc.method('jsonrpc.intEnumType')
def enum_int_type(e: ColorIntEnum) -> ColorIntEnum:
    return e


@jsonrpc.method('jsonrpc.decimalType')
def decimal_type(n: Decimal) -> Decimal:
    return n


@jsonrpc.method('jsonrpc.listType')
def list_type(lst: list[int]) -> list[int]:
    return lst


@jsonrpc.method('jsonrpc.tupleType')
def tuple_type(tn: tuple[int, int]) -> tuple[tuple[int, int], int]:
    return tn, 200


@jsonrpc.method('jsonrpc.namedtupleType')
def namedtuple_type(tn: EmployeeNamedTuple) -> tuple[EmployeeNamedTuple, int]:
    return tn, 200


@jsonrpc.method('jsonrpc.setType')
def set_type(s: set[int]) -> set[int]:
    return s


@jsonrpc.method('jsonrpc.frozensetType')
def fronzenset_type(s: frozenset[int]) -> frozenset[int]:
    return s


@jsonrpc.method('jsonrpc.dequeType')
def deque_type(d: deque[int]) -> deque[int]:
    return d


@jsonrpc.method('jsonrpc.sequenceType')
def sequence_type(s: t.Sequence[int]) -> t.Sequence[int]:
    return s


@jsonrpc.method('jsonrpc.dictType')
def dict_type(d: dict[str, int]) -> dict[str, int]:
    return d


@jsonrpc.method('jsonrpc.typedDictType')
def typeddict_type(user: UserTypedDict) -> UserTypedDict:
    return user


@jsonrpc.method('jsonrpc.optional')
def optional(n: t.Optional[int] = None) -> t.Optional[int]:
    return n


@jsonrpc.method('jsonrpc.unionWithTwoTypes')
def union_with_two_types(n: t.Union[int, float]) -> t.Union[int, float]:
    return n


@jsonrpc.method('jsonrpc.unionWithTwoTypesAndNone')
def union_with_two_types_and_none(n: t.Union[int, float, None] = None) -> t.Union[int, float, None]:
    return n


@jsonrpc.method('jsonrpc.literalType')
def literal_type(x: Literal['X']) -> Literal['X']:
    return x


@jsonrpc.method('jsonrpc.finalType')
def final_type(x: t.Final[str] = 'FinalValue') -> t.Final[str]:  # type: ignore
    return x


@jsonrpc.method('jsonrpc.anyType')
def any_type(obj: t.Any) -> t.Any:  # noqa: ANN401
    return obj


@jsonrpc.method('jsonrpc.noneType')
def none_type(obj: None = None) -> None:  # noqa: ANN401
    return obj


@jsonrpc.method('jsonrpc.noReturnType')
def no_return_type(s: str) -> t.NoReturn:  # noqa: ANN401
    raise ValueError(s)


@jsonrpc.method('jsonrpc.literalNoneType')
def literal_none_type(x: Literal[None] = None) -> Literal[None]:  # noqa: ANN401
    return x
