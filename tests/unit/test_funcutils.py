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
from dataclasses import asdict, dataclass

from pydantic.main import BaseModel

import pytest

from flask_jsonrpc.funcutils import loads

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class GenericClass:
    def __init__(self: Self, attr1: str, attr2: int) -> None:
        self.attr1 = attr1
        self.attr2 = attr2


@dataclass
class DataClassType:
    x: str
    y: int
    z: t.List[str]


class PydanticType(BaseModel):
    x: str
    y: int
    z: t.List[str]


def test_loads() -> None:
    assert loads(str, None) is None
    assert loads(t.Any, None) is None
    assert loads(t.Any, 42) == 42
    assert loads(t.Any, 'test') == 'test'
    assert loads(str, 'string') == 'string'
    assert loads(int, 1) == 1
    assert loads(t.Optional[int], 1) == 1
    assert loads(t.Optional[int], None) is None
    assert loads(t.Union[int, None], None) is None
    assert loads(t.Union[int, None], 1) == 1
    assert loads(t.Union[None, int], None) is None
    assert loads(t.Union[None, int], 1) == 1
    assert loads(t.Union[None, None], None) is None
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
    assert loads(t.List[int], [1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert loads(t.List[t.List[int]], [[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
    assert loads(t.Dict[str, int], {'a': 1, 'b': 2, 'c': 3}) == {'a': 1, 'b': 2, 'c': 3}
    assert loads(t.Dict[str, t.Dict[str, int]], {'outer': {'inner': 1}}) == {'outer': {'inner': 1}}
    assert loads(GenericClass, {'attr1': 'value1', 'attr2': 2}).__dict__ == GenericClass('value1', 2).__dict__
    assert (
        loads(PydanticType, {'x': 'str', 'y': 1, 'z': ['0', '1', '2']}).model_dump()
        == PydanticType(x='str', y=1, z=['0', '1', '2']).model_dump()
    )
    assert [x.model_dump() for x in loads(t.List[PydanticType], [{'x': 'str', 'y': 1, 'z': ['0', '1', '2']}])] == [
        PydanticType(x='str', y=1, z=['0', '1', '2']).model_dump()
    ]
    with pytest.raises(TypeError) as excinfo:
        loads(PydanticType, {'invalid_key': 'value'})
    assert "Field required [type=missing, input_value={'invalid_key': 'value'}, input_type=dict]" in str(excinfo.value)
    assert {
        k: v.model_dump()
        for k, v in loads(t.Dict[str, PydanticType], {'obj': {'x': 'str', 'y': 1, 'z': ['0', '1', '2']}}).items()
    } == {'obj': PydanticType(x='str', y=1, z=['0', '1', '2']).model_dump()}
    assert asdict(loads(DataClassType, {'x': 'str', 'y': 1, 'z': ['0', '1', '2']})) == asdict(
        DataClassType(x='str', y=1, z=['0', '1', '2'])
    )
    assert [asdict(x) for x in loads(t.List[DataClassType], [{'x': 'str', 'y': 1, 'z': ['0', '1', '2']}])] == [
        asdict(DataClassType(x='str', y=1, z=['0', '1', '2']))
    ]
    assert {
        k: asdict(v)
        for k, v in loads(t.Dict[str, DataClassType], {'obj': {'x': 'str', 'y': 1, 'z': ['0', '1', '2']}}).items()
    } == {'obj': asdict(DataClassType(x='str', y=1, z=['0', '1', '2']))}
    with pytest.raises(TypeError) as excinfo:
        loads(DataClassType, {'invalid_key': 'value'})
    assert "__init__() got an unexpected keyword argument 'invalid_key'" in str(excinfo.value)
