# -*- coding: utf-8 -*-
# Copyright (c) 2020-2020, Cenobit Technologies, Inc. http://cenobit.es/
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
from typing import Any, Dict, List, Text, Tuple, Union, TypeVar, NamedTuple
from numbers import Real, Integral, Rational
from collections import OrderedDict, defaultdict
from collections.abc import Mapping

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
    from .typing_inspect import get_args  # type: ignore

# Python 3.5.4+ / 3.6.2+
try:
    from typing import get_origin  # pylint: disable=C0412
except ImportError:  # pragma: no cover
    from .typing_inspect import get_origin  # type: ignore

# Python 3.5.4+ / 3.6.2+
try:
    from typing_extensions import NoReturn  # pylint: disable=C0412
except ImportError:  # pragma: no cover
    try:
        from typing import NoReturn  # pylint: disable=C0412
    except ImportError:
        NoReturn = None  # type: ignore


class JSONRPCNewType:
    def __init__(self, name: str, *types: Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]]) -> None:
        self.name = name
        self.types = types

    def check_expected_type(self, expected_type: type) -> bool:
        return any(expected_type is tp for tp in self.types)

    def check_expected_types(self, expected_types: Any) -> bool:
        return all(any(expt_tp is tp for tp in self.types) for expt_tp in expected_types)

    def check_type_var(self, expected_type: type) -> bool:
        bound_type = getattr(expected_type, '__bound__', None)
        if bound_type is None:
            expected_types = getattr(expected_type, '__constraints__', None)
            if not expected_types:
                return self is Object
            return self.check_expected_types(expected_types)
        return self.check_expected_type(bound_type)

    def check_union(self, expected_type: type) -> bool:
        expected_types = [expt_tp for expt_tp in get_args(expected_type) if expt_tp is not type(None)]  # noqa: E721
        return self.check_expected_types(expected_types)

    def check_literal(self, expected_type: type) -> bool:
        expected_types = get_args(expected_type)
        return self.check_expected_types(expected_types)

    def check_final(self, expected_type: type) -> bool:
        expected_types = get_args(expected_type)
        return self.check_expected_types(expected_types)

    def check_type(self, o: type) -> bool:  # pylint: disable=R0911
        expected_type = o
        if expected_type is Any:
            return self is Object

        if type(expected_type) is TypeVar:  # pylint: disable=C0123
            return self.check_type_var(expected_type)

        if expected_type is None or expected_type is NoReturn:
            expected_type = type(None)

        origin_type = get_origin(expected_type)
        if origin_type is not None:
            if origin_type is Union:
                return self.check_union(expected_type)

            if origin_type is Tuple or origin_type is tuple:
                return self is Array

            if origin_type is Literal:
                return self.check_literal(expected_type)

            if origin_type is Final:
                return self.check_final(expected_type)

            expected_type = origin_type

        return self.check_expected_type(expected_type)

    def __str__(self) -> str:
        return self.name


String = JSONRPCNewType('String', str, bytes, Text)
Number = JSONRPCNewType('Number', int, float, Real, Rational, Integral)
Object = JSONRPCNewType('Object', dict, Dict, defaultdict, OrderedDict, Mapping)
Array = JSONRPCNewType('Array', list, tuple, List, NamedTuple)
Boolean = JSONRPCNewType('Boolean', bool)
Null = JSONRPCNewType('Null', type(None))
Types = [String, Number, Object, Array, Boolean, Null]
