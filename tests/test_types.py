import sys
from typing import (
    Any,
    Set,
    Dict,
    List,
    Tuple,
    Union,
    AnyStr,
    Mapping,
    NewType,
    TypeVar,
    NoReturn,
    Optional,
    FrozenSet,
    NamedTuple,
    DefaultDict,
    get_type_hints,
)
from numbers import Real, Number, Complex, Integral, Rational

import pytest

from flask_jsonrpc import types

try:
    from typing import OrderedDict  # pylint: disable=C0412
except ImportError:
    from collections import OrderedDict


def test_types():
    assert types.String.check_type(str)
    assert types.String.check_type(AnyStr)
    assert str(types.String) == 'String'

    assert types.Number.check_type(int)
    assert types.Number.check_type(float)
    assert not types.Number.check_type(complex)
    assert types.Number.check_type(Real)
    assert types.Number.check_type(Rational)
    assert types.Number.check_type(Integral)
    assert not types.Number.check_type(Complex)
    assert not types.Number.check_type(Number)
    assert str(types.Number) == 'Number'

    assert types.Object.check_type(dict)
    assert types.Object.check_type(Dict)
    assert types.Object.check_type(Any)
    assert str(types.Object) == 'Object'

    assert types.Array.check_type(list)
    assert types.Array.check_type(tuple)
    assert types.Array.check_type(set)
    assert types.Array.check_type(List)
    assert types.Array.check_type(NamedTuple)
    assert types.Array.check_type(Set)
    assert types.Array.check_type(Tuple)
    assert types.Array.check_type(frozenset)
    assert types.Array.check_type(FrozenSet)
    assert str(types.Array) == 'Array'

    assert types.Boolean.check_type(bool)
    assert str(types.Boolean) == 'Boolean'

    assert types.Null.check_type(None)
    assert types.Null.check_type(type(None))  # noqa: E721
    assert types.Null.check_type(NoReturn)
    assert str(types.Null) == 'Null'


@pytest.mark.skipif(sys.version_info < (3, 7), reason='requires python3.7 or higher')
def test_types_others():
    assert types.Object.check_type(OrderedDict)
    assert types.Object.check_type(DefaultDict)
    assert types.Object.check_type(Mapping)


@pytest.mark.skipif(sys.version_info < (3, 7), reason='requires python3.7 or higher')
def test_types_complex():
    T = TypeVar('T')
    S = TypeVar('S', int, float)
    X = TypeVar('X', bound=int)
    U = types.Literal[str]
    V = types.Final[str]

    assert types.Object.check_type(T)
    assert types.Number.check_type(S)
    assert types.String.check_type(U)
    assert types.Number.check_type(X)
    assert types.String.check_type(V)
    assert types.String.check_type(Union[str, None])
    assert types.String.check_type(Optional[str])


def test_types_from_fn():
    def fn(_a: str, _b: int, _c: Dict[str, Any], _d: List[int], _e: Any) -> bool:
        return True

    fn_annotations = get_type_hints(fn)
    assert types.String.check_type(fn_annotations['_a'])
    assert types.Number.check_type(fn_annotations['_b'])
    assert types.Object.check_type(fn_annotations['_c'])
    assert types.Array.check_type(fn_annotations['_d'])
    assert types.Object.check_type(fn_annotations['_e'])
    assert types.Boolean.check_type(fn_annotations['return'])


# pylint: disable=E1136
@pytest.mark.skipif(sys.version_info < (3, 9), reason='requires python3.9 or higher')
def test_generic_type_alias():
    T = TypeVar('T')

    assert types.Array.check_type(list[int])
    assert types.Array.check_type(list[float])
    assert types.Array.check_type(set[str])
    assert types.Array.check_type(frozenset[int])
    assert types.Array.check_type(tuple[int])
    assert types.Object.check_type(dict[int, str])
    assert types.Object.check_type(dict[int, T][str])
    assert types.Object.check_type(dict[int, list[int]])


# pylint: disable=E1131
@pytest.mark.skipif(sys.version_info < (3, 10), reason='requires python3.10 or higher')
def test_union_type_expression():
    assert types.Array.check_type(list[int | str])
    assert types.String.check_type(str | bytearray)
    assert types.String.check_type(bytearray | str)
    assert types.String.check_type(str | None)
    assert types.Number.check_type(int | float)


@pytest.mark.skipif(sys.version_info < (3, 10), reason='requires python3.10 or higher')
def test_none_type():
    assert types.Null.check_type(type(None))
    assert types.Null.check_type(types.NoneType)


def test_new_type():
    UserId = NewType('UserId', int)
    UserUid = NewType('UserUid', str)

    assert types.Number.check_type(UserId)
    assert types.String.check_type(UserUid)
    assert not types.Number.check_type(UserUid)
