# Copyright (c) 2020-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
from __future__ import annotations

from types import GeneratorType
import typing as t
import inspect
from numbers import Real, Integral, Rational
from collections import OrderedDict, deque, defaultdict
from collections.abc import Mapping

import typing_inspect

# Added in version 3.11.
from typing_extensions import Self


class JSONRPCNewType:
    def __init__(self: Self, name: str, *types: type | tuple[type | tuple[type, ...], ...]) -> None:
        self.name = name
        self.types = types

    def _check_expected_type(self: Self, expected_type: t.Any) -> bool:  # noqa: ANN401
        return any(expected_type is tp for tp in self.types)

    def _check_expected_types(self: Self, expected_types: t.Any) -> bool:  # noqa: ANN401
        return all(self.check_type(expt_tp) for expt_tp in expected_types)

    def _check_type_var(self: Self, expected_type: t.Any) -> bool:  # noqa: ANN401
        bound_type = getattr(expected_type, '__bound__', None)
        if bound_type is None:
            expected_types = getattr(expected_type, '__constraints__', None)
            if not expected_types:
                return self is Object
            return self._check_expected_types(expected_types)
        return self._check_expected_type(bound_type)

    def _check_new_type(self: Self, expected_type: t.Any) -> bool:  # noqa: ANN401
        super_type = getattr(expected_type, '__supertype__', None)
        return self._check_expected_type(super_type)

    def _check_union(self: Self, expected_type: t.Any) -> bool:  # noqa: ANN401
        expected_types = [expt_tp for expt_tp in t.get_args(expected_type) if expt_tp is not type(None)]  # noqa: E721
        return self._check_expected_types(expected_types)

    def _check_args_type(self: Self, expected_type: t.Any) -> bool:  # noqa: ANN401
        args = t.get_args(expected_type)
        expected_types = [arg if inspect.isclass(arg) else type(arg) for arg in args]
        return self._check_expected_types(expected_types)

    def check_type(self: Self, o: t.Any) -> bool:  # noqa: ANN401
        expected_type = o
        if expected_type is t.Any:
            return self is Object

        if expected_type is None or expected_type is t.NoReturn:
            expected_type = type(None)

        if typing_inspect.is_tuple_type(expected_type):
            return self is Array

        if typing_inspect.is_typevar(expected_type):
            return self._check_type_var(expected_type)

        if typing_inspect.is_new_type(expected_type) or hasattr(expected_type, '__supertype__'):
            return self._check_new_type(expected_type)

        if typing_inspect.is_union_type(expected_type):
            return self._check_union(expected_type)

        if typing_inspect.is_literal_type(expected_type):
            return self._check_args_type(expected_type)

        if typing_inspect.is_final_type(expected_type):
            return self._check_args_type(expected_type)

        origin_type = t.get_origin(expected_type)
        if origin_type is not None:
            expected_type = origin_type

        return self._check_expected_type(expected_type)

    def __str__(self: Self) -> str:
        return self.name


String = JSONRPCNewType('String', str, bytes, bytearray)
Number = JSONRPCNewType('Number', int, float, Real, Rational, Integral)
Object = JSONRPCNewType('Object', dict, t.Dict, defaultdict, OrderedDict, Mapping)  # noqa: UP006
Array = JSONRPCNewType('Array', list, t.List, set, t.Set, tuple, t.Tuple, frozenset, t.FrozenSet, GeneratorType, deque)  # type: ignore[arg-type]  # noqa: UP006
Boolean = JSONRPCNewType('Boolean', bool)
Null = JSONRPCNewType('Null', type(None), t.Literal[None])  # type: ignore[arg-type]
Types = [Null, String, Number, Boolean, Array, Object]
