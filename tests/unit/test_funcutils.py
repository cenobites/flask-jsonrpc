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
from enum import Enum
import typing as t
from decimal import Decimal
from dataclasses import asdict, dataclass

from typing_extensions import Literal, LiteralString

from pydantic.main import BaseModel

import pytest

from flask_jsonrpc.funcutils import loads, bindfy

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class GenericClass:
    def __init__(self: Self, attr1: str, attr2: int) -> None:
        self.attr1 = attr1
        self.attr2 = attr2


class NamedTupleType(t.NamedTuple):
    x: str
    y: int
    z: list[str]


class EnumType(Enum):
    RED = 1
    BLUE = 2


@dataclass
class DataClassType:
    x: str
    y: int
    z: list[str]


class PydanticType(BaseModel):
    x: str
    y: int
    z: list[str]


def test_loads_simple() -> None:
    assert loads(str, None) is None
    assert loads(t.Any, None) is None
    assert loads(t.Any, 42) == 42
    assert loads(t.Any, 'test') == 'test'
    assert loads(str, 'string') == 'string'
    assert loads(bytes, 'string') == b'string'
    assert loads(int, 1) == 1


def test_loads_none() -> None:
    assert loads(None, None) is None
    assert loads(Literal[None], None) is None


def test_loads_optinal() -> None:
    assert loads(t.Optional[int], 1) == 1
    assert loads(t.Optional[int], None) is None
    assert loads(t.Optional[str], 'Lou') == 'Lou'


def test_loads_union() -> None:
    assert loads(t.Union[int, None], None) is None
    assert loads(t.Union[int, None], 1) == 1
    assert loads(t.Union[None, int], None) is None
    assert loads(t.Union[None, int], 1) == 1
    assert loads(t.Union[None, None], None) is None


def test_loads_invalid_union_types() -> None:
    with pytest.raises(
        TypeError,
        match='the only type of union that is supported is: typing.Union\\[T, None\\] or typing.Optional\\[T\\]',
    ):
        loads(t.Union[int, str, None], 1)
    with pytest.raises(
        TypeError,
        match='the only type of union that is supported is: typing.Union\\[T, None\\] or typing.Optional\\[T\\]',
    ):
        loads(t.Union[int, str], 1)


def test_loads_list() -> None:
    assert loads(list[int], [1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert loads(list[list[int]], [[1, 2], [3, 4]]) == [[1, 2], [3, 4]]


def test_loads_dict() -> None:
    assert loads(dict[str, int], {'a': 1, 'b': 2, 'c': 3}) == {'a': 1, 'b': 2, 'c': 3}
    assert loads(dict[str, dict[str, int]], {'outer': {'inner': 1}}) == {'outer': {'inner': 1}}


def test_loads_literal() -> None:
    assert loads(Literal[True], True)
    assert loads(Literal['hello', 'world'], 'hello') == 'hello'
    assert loads(LiteralString, 'hello') == 'hello'


def test_loads_final() -> None:
    assert loads(t.Final[bool], True)
    assert loads(t.Final[int], 10) == 10


def test_loads_enum() -> None:
    assert loads(EnumType, 1) == EnumType.RED


def test_loads_decimal() -> None:
    assert loads(Decimal, '1.23') == Decimal('1.23')


def test_loads_pure_class() -> None:
    assert loads(GenericClass, {'attr1': 'value1', 'attr2': 2}).__dict__ == GenericClass('value1', 2).__dict__


def test_loads_namedtuple() -> None:
    assert loads(NamedTupleType, {'x': 'str', 'y': 1, 'z': ['a', 'b', 'c']}) == NamedTupleType(
        x='str', y=1, z=['a', 'b', 'c']
    )


def test_loads_pydantic_model() -> None:
    assert (
        loads(PydanticType, {'x': 'str', 'y': 1, 'z': ['0', '1', '2']}).model_dump()
        == PydanticType(x='str', y=1, z=['0', '1', '2']).model_dump()
    )


def test_loads_invalid_pydantic_model() -> None:
    with pytest.raises(TypeError) as excinfo:
        loads(PydanticType, {'invalid_key': 'value'})
    assert "Field required [type=missing, input_value={'invalid_key': 'value'}, input_type=dict]" in str(excinfo.value)


def test_loads_complex_list() -> None:
    assert [x.model_dump() for x in loads(list[PydanticType], [{'x': 'str', 'y': 1, 'z': ['0', '1', '2']}])] == [
        PydanticType(x='str', y=1, z=['0', '1', '2']).model_dump()
    ]
    assert [asdict(x) for x in loads(list[DataClassType], [{'x': 'str', 'y': 1, 'z': ['0', '1', '2']}])] == [
        asdict(DataClassType(x='str', y=1, z=['0', '1', '2']))
    ]


def test_loads_complex_dict() -> None:
    assert {
        k: v.model_dump()
        for k, v in loads(dict[str, PydanticType], {'obj': {'x': 'str', 'y': 1, 'z': ['0', '1', '2']}}).items()
    } == {'obj': PydanticType(x='str', y=1, z=['0', '1', '2']).model_dump()}
    assert asdict(loads(DataClassType, {'x': 'str', 'y': 1, 'z': ['0', '1', '2']})) == asdict(
        DataClassType(x='str', y=1, z=['0', '1', '2'])
    )
    assert {
        k: asdict(v)
        for k, v in loads(dict[str, DataClassType], {'obj': {'x': 'str', 'y': 1, 'z': ['0', '1', '2']}}).items()
    } == {'obj': asdict(DataClassType(x='str', y=1, z=['0', '1', '2']))}
    with pytest.raises(TypeError) as excinfo:
        loads(DataClassType, {'invalid_key': 'value'})
    assert "__init__() got an unexpected keyword argument 'invalid_key'" in str(excinfo.value)


def test_bindfy() -> None:
    def view_func(name: str) -> str:
        return f'Hello {name}'

    fn_annotations = t.get_type_hints(view_func)
    setattr(view_func, 'jsonrpc_method_return', fn_annotations.pop('return', None))  # noqa: B010
    setattr(view_func, 'jsonrpc_method_params', fn_annotations)  # noqa: B010

    bindfy(view_func, {'name': 'Eve'})
