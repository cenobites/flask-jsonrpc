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
from pathlib import Path
from collections import deque
from dataclasses import dataclass

from pydantic.main import BaseModel

from flask_jsonrpc.encoders import serializable

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class EnumType(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'


class GenericClass:
    def __init__(self: Self) -> None:
        self.attr1 = 'value1'
        self.attr2 = 2


@dataclass
class DataClassType:
    x: str
    y: int
    z: t.List[str]


class PydanticType(BaseModel):
    x: str
    y: int
    z: t.List[str]


def test_serializable() -> None:
    assert serializable(None) is None
    assert serializable('') == ''
    assert serializable(1) == 1
    assert serializable(EnumType.X) == 'x'
    assert serializable(Path('/')) == '/'
    assert serializable({'key1': 'value1', 'key2': EnumType.X}) == {'key1': 'value1', 'key2': 'x'}
    assert serializable([1, 2, EnumType.X, Path('/another/path')]) == [1, 2, 'x', '/another/path']
    assert serializable(deque(['a', 'b', EnumType.X])) == ['a', 'b', 'x']
    assert serializable(GenericClass()) == {'attr1': 'value1', 'attr2': 2}
    assert serializable(
        {
            'str': 'x',
            'int': 1,
            'none': None,
            'list': [1, '2', []],
            'dict': {'1': 2, '3': 4},
            'dataclass': DataClassType(x='str', y=1, z=['0', '1', '2']),
            'pydantic': PydanticType(x='str', y=1, z=['0', '1', '2']),
        }
    ) == {
        'dataclass': {'x': 'str', 'y': 1, 'z': ['0', '1', '2']},
        'dict': {'1': 2, '3': 4},
        'int': 1,
        'list': [1, '2', []],
        'none': None,
        'pydantic': {'x': 'str', 'y': 1, 'z': ['0', '1', '2']},
        'str': 'x',
    }
    assert serializable(
        [
            'x',
            1,
            None,
            [1, '2', []],
            {'1': 2, '3': 4},
            DataClassType(x='str', y=1, z=['0', '1', '2']),
            PydanticType(x='str', y=1, z=['0', '1', '2']),
        ]
    ) == [
        'x',
        1,
        None,
        [1, '2', []],
        {'1': 2, '3': 4},
        {'x': 'str', 'y': 1, 'z': ['0', '1', '2']},
        {'x': 'str', 'y': 1, 'z': ['0', '1', '2']},
    ]
