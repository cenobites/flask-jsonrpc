from typing import (
    Any,
    Set,
    Dict,
    List,
    Text,
    Final,
    Union,
    AnyStr,
    Literal,
    Mapping,
    TypeVar,
    NoReturn,
    Optional,
    NamedTuple,
    DefaultDict,
    OrderedDict,
    get_type_hints,
)
from numbers import Real, Number, Complex, Integral, Rational

from flask_jsonrpc import types


def test_types():
    assert types.String.check_type(str)
    assert types.String.check_type(AnyStr)
    assert types.String.check_type(Text)
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
    assert types.Object.check_type(DefaultDict)
    assert types.Object.check_type(OrderedDict)
    assert types.Object.check_type(Mapping)
    assert types.Object.check_type(Any)
    assert str(types.Object) == 'Object'

    assert types.Array.check_type(list)
    assert types.Array.check_type(tuple)
    assert not types.Array.check_type(set)
    assert types.Array.check_type(List)
    assert types.Array.check_type(NamedTuple)
    assert not types.Array.check_type(Set)
    assert str(types.Array) == 'Array'

    assert types.Boolean.check_type(bool)
    assert str(types.Boolean) == 'Boolean'

    assert types.Null.check_type(None)
    assert types.Null.check_type(type(None))  # noqa: E721
    assert types.Null.check_type(NoReturn)
    assert str(types.Null) == 'Null'


def test_types_complex():
    T = TypeVar('T')
    S = TypeVar('S', int, float)
    X = TypeVar('X', bound=int)
    U = Literal[str]
    V = Final[str]

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
