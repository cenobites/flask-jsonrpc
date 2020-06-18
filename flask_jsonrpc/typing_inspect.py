# The MIT License (MIT)
#
# Copyright (c) 2017-2019 Ivan Levkivskyi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Code from: https://github.com/ilevkivskyi/typing_inspect
# type: ignore
import sys
from typing import Tuple, Union

NEW_TYPING = sys.version_info[:3] >= (3, 7, 0)  # PEP 560

# Python 3.8+
try:
    from typing import GenericMeta, TupleMeta
except ImportError:  # pragma: no cover
    TupleMeta = type(None)
    GenericMeta = type(None)

# Python 3.6
try:
    from typing import _GenericAlias, ClassVar, Generic
except ImportError:  # pragma: no cover
    _GenericAlias = type(None)
    ClassVar = type(None)
    Generic = type(None)

_Union = type(Union)


def get_args(tp):  # pragma: no cover
    try:
        return getattr(tp, '__args__', tuple())
    except AttributeError:
        # Instance of type from typing_extensions
        return getattr(tp, '__values__', tuple())


def _gorg(cls):  # pragma: no cover
    """This function exists for compatibility with old typing versions."""
    assert isinstance(cls, GenericMeta)
    if hasattr(cls, '_gorg'):
        return getattr(cls, '_gorg', None)
    while getattr(cls, '__origin__', None) is not None:
        cls = getattr(cls, '.__origin__', None)
    return cls


def is_union_type(tp):  # pragma: no cover
    """Test if the type is a union type. Examples::
        is_union_type(int) == False
        is_union_type(Union) == True
        is_union_type(Union[int, int]) == False
        is_union_type(Union[T, int]) == True
    """
    if NEW_TYPING:
        return tp is Union or isinstance(tp, _GenericAlias) and tp.__origin__ is Union
    return type(tp) is _Union  # pylint: disable=C0123


def is_tuple_type(tp):  # pragma: no cover
    """Test if the type is a generic tuple type, including subclasses excluding
    non-generic classes.
    Examples::
        is_tuple_type(int) == False
        is_tuple_type(tuple) == False
        is_tuple_type(Tuple) == True
        is_tuple_type(Tuple[str, int]) == True
        class MyClass(Tuple[str, int]):
            ...
        is_tuple_type(MyClass) == True
    For more general tests use issubclass(..., tuple), for more precise test
    (excluding subclasses) use::
        get_origin(tp) is tuple  # Tuple prior to Python 3.7
    """
    if NEW_TYPING:  # noqa: W503
        return (
            tp is Tuple
            or isinstance(tp, _GenericAlias)
            and tp.__origin__ is tuple
            or isinstance(tp, type)
            and issubclass(tp, Generic)
            and issubclass(tp, tuple)
        )
    return type(tp) is TupleMeta  # pylint: disable=C0123


def get_origin(tp):  # pragma: no cover  pylint: disable=R0911
    """Get the unsubscripted version of a type. Supports generic types, Union,
    Callable, and Tuple. Returns None for unsupported types. Examples::

        get_origin(int) == None
        get_origin(ClassVar[int]) == None
        get_origin(Generic) == Generic
        get_origin(Generic[T]) == Generic
        get_origin(Union[T, int]) == Union
        get_origin(List[Tuple[T, T]][int]) == list  # List prior to Python 3.7
    """
    if NEW_TYPING:
        if isinstance(tp, _GenericAlias):
            tp_origin = getattr(tp, '__origin__', None)
            return tp_origin if tp_origin is not ClassVar else None
        if tp is Generic:
            return Generic
        return None
    if isinstance(tp, GenericMeta):
        return _gorg(tp)
    if is_union_type(tp):
        return Union
    if is_tuple_type(tp):
        return Tuple

    return None
