# Copyright (c) 2020-2022, Cenobit Technologies, Inc. http://cenobit.es/
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
from numbers import Real, Integral, Rational
from collections import OrderedDict, defaultdict
from collections.abc import Mapping

from typing_inspect import is_new_type  # type: ignore

# Python 3.10+
try:
    from types import NoneType, UnionType
except ImportError:  # pragma: no cover
    UnionType = None  # type: ignore
    NoneType = type(None)  # type: ignore

# Python 3.8+
try:
    from typing_extensions import Literal
except ImportError:  # pragma: no cover
    from typing import Literal  # type: ignore  # pylint: disable=C0412

# Python 3.8+
try:
    from typing_extensions import Final
except ImportError:  # pragma: no cover
    from typing import Final  # type: ignore  # pylint: disable=C0412

# Python 3.5.4+ / 3.6.2+
try:
    from typing import get_args  # pylint: disable=C0412
except ImportError:  # pragma: no cover
    from typing_inspect import get_args  # type: ignore  # pylint: disable=C0412

# Python 3.5.4+ / 3.6.2+
try:
    from typing import get_origin  # pylint: disable=C0412
except ImportError:  # pragma: no cover
    from typing_inspect import get_origin  # type: ignore  # pylint: disable=C0412

# Python 3.5.4+ / 3.6.2+
try:
    from typing_extensions import NoReturn  # pylint: disable=C0412
except ImportError:  # pragma: no cover
    try:
        from typing import NoReturn  # pylint: disable=C0412
    except ImportError:
        NoReturn = None  # type: ignore


class JSONRPCNewType:
    def __init__(self, name: str, *types: t.Union[type, t.Tuple[t.Union[type, t.Tuple[type, ...]], ...]]) -> None:
        self.name = name
        self.types = types

    def check_expected_type(self, expected_type: t.Any) -> bool:
        return any(expected_type is tp for tp in self.types)

    def check_expected_types(self, expected_types: t.Any) -> bool:
        return all(any(expt_tp is tp for tp in self.types) for expt_tp in expected_types)

    def check_type_var(self, expected_type: t.Any) -> bool:  # pragma: no cover py3.6
        bound_type = getattr(expected_type, '__bound__', None)
        if bound_type is None:
            expected_types = getattr(expected_type, '__constraints__', None)
            if not expected_types:
                return self is Object
            return self.check_expected_types(expected_types)
        return self.check_expected_type(bound_type)

    def check_new_type(self, expected_type: t.Any) -> bool:  # pragma: no cover py3.6
        super_type = getattr(expected_type, '__supertype__', None)
        return self.check_expected_type(super_type)

    def check_union(self, expected_type: t.Any) -> bool:
        expected_types = [expt_tp for expt_tp in get_args(expected_type) if expt_tp is not type(None)]  # noqa: E721
        return self.check_expected_types(expected_types)

    def check_args_type(self, expected_type: t.Any) -> bool:  # pragma: no cover py3.6
        expected_types = get_args(expected_type)
        return self.check_expected_types(expected_types)

    def check_type(self, o: t.Any) -> bool:  # pylint: disable=R0911
        expected_type = o
        if expected_type is t.Any:
            return self is Object

        if expected_type is None or expected_type is NoReturn:
            expected_type = type(None)

        if type(expected_type) is t.TypeVar:  # pylint: disable=C0123
            return self.check_type_var(expected_type)

        if is_new_type(expected_type):
            return self.check_new_type(expected_type)

        origin_type = get_origin(expected_type)
        if origin_type is not None:
            if origin_type is t.Union or origin_type is UnionType:
                return self.check_union(expected_type)

            if origin_type is t.Tuple or origin_type is tuple:
                return self is Array

            if origin_type is Literal:  # pragma: no cover py3.6
                return self.check_args_type(expected_type)

            if origin_type is Final:  # pragma: no cover py3.6
                return self.check_args_type(expected_type)

            expected_type = origin_type

        return self.check_expected_type(expected_type)

    def __str__(self) -> str:
        return self.name


String = JSONRPCNewType('String', str, bytes, bytearray)
Number = JSONRPCNewType('Number', int, float, Real, Rational, Integral)
Object = JSONRPCNewType('Object', dict, t.Dict, defaultdict, OrderedDict, Mapping)
Array = JSONRPCNewType('Array', list, set, t.Set, tuple, t.List, t.NamedTuple, frozenset, t.FrozenSet)
Boolean = JSONRPCNewType('Boolean', bool)
Null = JSONRPCNewType('Null', type(None), NoneType)
Types = [String, Number, Object, Array, Boolean, Null]
