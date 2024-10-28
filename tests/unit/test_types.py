# Copyright (c) 2021-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
import sys
import typing as t
from numbers import Real, Number, Complex, Integral, Rational
from collections import OrderedDict, defaultdict

from typing_extensions import Literal

import pytest

from flask_jsonrpc import types


def test_types_empty_type() -> None:
    empty_type = types.JSONRPCNewType('Empty', ())
    assert not empty_type.check_type(str)


def test_types_string() -> None:
    assert types.String.check_type(str)
    assert types.String.check_type(t.AnyStr)
    assert str(types.String) == 'String'


def test_types_number() -> None:
    assert types.Number.check_type(int)
    assert types.Number.check_type(float)
    assert not types.Number.check_type(complex)
    assert types.Number.check_type(Real)
    assert types.Number.check_type(Rational)
    assert types.Number.check_type(Integral)
    assert not types.Number.check_type(Complex)
    assert not types.Number.check_type(Number)
    assert str(types.Number) == 'Number'


def test_types_object() -> None:
    assert types.Object.check_type(dict)
    assert types.Object.check_type(dict)
    assert types.Object.check_type(t.Any)
    assert str(types.Object) == 'Object'


def test_types_array() -> None:
    assert types.Array.check_type(list)
    assert types.Array.check_type(tuple)
    assert types.Array.check_type(set)
    assert types.Array.check_type(list)
    assert types.Array.check_type(set)
    assert types.Array.check_type(tuple)
    assert types.Array.check_type(frozenset)
    assert types.Array.check_type(frozenset)
    assert str(types.Array) == 'Array'


def test_types_boolean() -> None:
    assert types.Boolean.check_type(bool)
    assert str(types.Boolean) == 'Boolean'


def test_types_null() -> None:
    assert types.Null.check_type(None)
    assert types.Null.check_type(type(None))  # noqa: E721
    assert types.Null.check_type(t.NoReturn)
    assert types.Null.check_type(Literal[None])
    assert not types.Object.check_type(Literal[None])
    assert str(types.Null) == 'Null'


def test_types_python_mapping() -> None:
    assert types.Object.check_type(OrderedDict)
    assert types.Object.check_type(defaultdict)
    assert types.Object.check_type(defaultdict)
    assert types.Object.check_type(t.Mapping)


def test_types_type_var() -> None:
    T = t.TypeVar('T')
    S = t.TypeVar('S', int, float)
    X = t.TypeVar('X', bound=int)

    assert types.Object.check_type(T)
    assert types.Number.check_type(S)
    assert types.Number.check_type(X)


def test_types_literal() -> None:
    assert types.String.check_type(Literal[str])
    assert types.String.check_type(Literal['hello', 'world'])
    assert not types.String.check_type(Literal[1, 2])


def test_types_final() -> None:
    assert types.String.check_type(t.Final[str])
    assert not types.String.check_type(t.Final[int])


def test_types_union() -> None:
    assert types.String.check_type(t.Union[str, None])
    assert types.String.check_type(t.Optional[str])
    assert not types.String.check_type(t.Union[str, int])
    assert not types.Number.check_type(t.Union[str, int])


def test_types_custom_type() -> None:
    class CustomType:
        __supertype__ = str

    custom_type = types.JSONRPCNewType('CustomType', str)
    assert custom_type.check_type(CustomType())


def test_types_from_fn() -> None:
    def fn(_a: str, _b: int, _c: dict[str, t.Any], _d: list[int], _e: t.Any) -> bool:  # noqa: ANN401
        return True

    fn_annotations = t.get_type_hints(fn)
    assert types.String.check_type(fn_annotations['_a'])
    assert types.Number.check_type(fn_annotations['_b'])
    assert types.Object.check_type(fn_annotations['_c'])
    assert types.Array.check_type(fn_annotations['_d'])
    assert types.Object.check_type(fn_annotations['_e'])
    assert types.Boolean.check_type(fn_annotations['return'])


@pytest.mark.skipif(sys.version_info < (3, 9), reason='requires python3.9 or higher')
def test_types_generic_type_alias() -> None:
    T = t.TypeVar('T')

    assert types.Array.check_type(list[int])
    assert types.Array.check_type(list[float])
    assert types.Array.check_type(set[str])
    assert types.Array.check_type(frozenset[int])
    assert types.Array.check_type(tuple[int])
    assert types.Object.check_type(dict[int, str])
    assert types.Object.check_type(dict[int, T][str])  # type: ignore
    assert types.Object.check_type(dict[int, list[int]])


@pytest.mark.skipif(sys.version_info < (3, 10), reason='requires python3.10 or higher')
def test_types_union_type_expression() -> None:
    assert types.Array.check_type(list[int | str])
    assert types.String.check_type(str | bytearray)
    assert types.String.check_type(bytearray | str)
    assert types.String.check_type(str | None)
    assert types.Number.check_type(int | float)


@pytest.mark.skipif(sys.version_info < (3, 10), reason='requires python3.10 or higher')
def test_types_none_type() -> None:
    assert types.Null.check_type(type(None))


def test_types_new_type() -> None:
    UserId = t.NewType('UserId', int)
    UserUid = t.NewType('UserUid', str)

    assert types.Number.check_type(UserId)
    assert types.String.check_type(UserUid)
    assert not types.Number.check_type(UserUid)
