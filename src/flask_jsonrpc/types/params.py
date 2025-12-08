# Copyright (c) 2024-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

import re
import math
import typing as t
from decimal import Decimal
from dataclasses import dataclass

import annotated_types

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc.utils import trait

SLOTS = {'slots': True}
EMPTY_VALUES: tuple[t.Any, ...] = (None, '', [], (), {})


def extract_digits_and_decimals(value: Decimal) -> tuple[int, int]:
    # https://github.com/django/django/blob/main/django/core/validators.py#L528
    digit_tuple, exponent = value.as_tuple()[1:]
    if exponent in {'F', 'n', 'N'}:
        raise TypeError('ensure the value of the parameter is a number')
    exponent = int(exponent)
    if exponent >= 0:
        digits = len(digit_tuple)
        if digit_tuple != (0,):
            # A positive exponent adds that many trailing zeros.
            digits += exponent
        decimals = 0
    else:
        # If the absolute value of the negative exponent is larger than the
        # number of digits, then it's the same as the number of digits,
        # because it'll consume all of the digits in digit_tuple and then
        # add abs(exponent) - len(digit_tuple) leading zeros after the
        # decimal point.
        if abs(exponent) > len(digit_tuple):
            digits = decimals = abs(exponent)
        else:
            digits = len(digit_tuple)
            decimals = abs(exponent)
    return digits, decimals


@dataclass
class Ok:
    """A successful type check result."""

    value: t.Any


@dataclass
class Err:
    """An unsuccessful type check result."""

    message: str


@trait
class BaseAnnotatedMetadata:
    """Base class for annotated metadata used in type checking."""

    __slots__ = ()

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        raise NotImplementedError('.type_check must be overridden') from None


class DefaultTypeCheckMixin:
    """Mixin class that provides a default type check implementation."""

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        """Perform a default type check that always succeeds."""
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class Summary(DefaultTypeCheckMixin, BaseAnnotatedMetadata):
    summary: str


@dataclass(frozen=True, **SLOTS)
class Description(DefaultTypeCheckMixin, BaseAnnotatedMetadata):
    description: str


@dataclass(frozen=True, **SLOTS)
class Properties(DefaultTypeCheckMixin, BaseAnnotatedMetadata):
    annotations: dict[str, t.Annotated[t.Any, ...] | t.Any]


@dataclass(frozen=True, **SLOTS)
class Example(DefaultTypeCheckMixin, BaseAnnotatedMetadata):
    name: str
    value: t.Any


@dataclass(frozen=True, **SLOTS)
class Required(BaseAnnotatedMetadata):
    required: bool = True

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        if self.required and value in EMPTY_VALUES:
            return Err(f'ensure the value of the parameter {name!r} is not empty')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class Deprecated(DefaultTypeCheckMixin, BaseAnnotatedMetadata):
    deprecated: bool = True


@dataclass(frozen=True, **SLOTS)
class Nullable(BaseAnnotatedMetadata):
    nullable: bool = True

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        if not self.nullable and value is None:
            return Err(f'ensure the parameter {name!r} is not null')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class Maximum(BaseAnnotatedMetadata):
    maximum: t.Annotated[float, annotated_types.Ge(0)]

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        if value > self.maximum:
            return Err(f'ensure the value of the parameter {name!r} is less than or equal to {self.maximum}')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class Minimum(BaseAnnotatedMetadata):
    minimum: t.Annotated[float, annotated_types.Ge(0)]

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        if value < self.minimum:
            return Err(f'ensure the value of the parameter {name!r} is greater than or equal to {self.minimum}')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class MultipleOf(BaseAnnotatedMetadata):
    multiple_of: t.Annotated[float, annotated_types.MultipleOf(0)]

    def __post_init__(self: Self) -> None:
        if self.multiple_of < 0:
            raise ValueError('invalid `multiple_of` value. The value must be greater than or equal to 0')

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        if value % self.multiple_of == 0:
            return Ok(value)
        return Err(f'ensure the value of the parameter {name!r} is a multiple of {self.multiple_of}')


@dataclass(frozen=True, **SLOTS)
class MaxLength(BaseAnnotatedMetadata):
    max_length: t.Annotated[int, annotated_types.Ge(0)]

    def __post_init__(self: Self) -> None:
        if self.max_length <= 0:
            raise ValueError('invalid `max_length` value. The value must be greater than 0')

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        cleaned = len(value)
        if value is not None and cleaned > self.max_length:
            return Err(f'ensure the value of the parameter {name!r} is less than or equal to {self.max_length}')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class MinLength(BaseAnnotatedMetadata):
    min_length: t.Annotated[int, annotated_types.Ge(0)]

    def __post_init__(self: Self) -> None:
        if self.min_length <= 0:
            raise ValueError('invalid `min_length` value. The value must be greater than 0')

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        cleaned = len(value)
        if value is not None and cleaned < self.min_length:
            return Err(f'ensure the value of the parameter {name!r} is greater than or equal to {self.min_length}')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class Pattern(BaseAnnotatedMetadata):
    pattern: t.Pattern[str] | str

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        if re.match(self.pattern, value) is None:
            return Err(f'ensure the value of the parameter {name!r} matches the valid pattern {self.pattern!r}')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class AllowInfNan(BaseAnnotatedMetadata):
    allow_inf_nan: bool = True

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        if not self.allow_inf_nan and (math.isnan(value) or math.isinf(value)):
            return Err(f'ensure the value of the parameter {name!r} is not infinity, negative infinity, or NaN')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class MaxDigits(BaseAnnotatedMetadata):
    max_digits: t.Annotated[int, annotated_types.Ge(0)]

    def __post_init__(self: Self) -> None:
        if self.max_digits <= 0:
            raise ValueError('invalid `max_digits` value. The value must be greater than 0')

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        cleaned = Decimal(str(value)) if not isinstance(value, Decimal) else value
        digits, decimals = extract_digits_and_decimals(cleaned)
        whole_digits = digits - decimals
        if whole_digits > self.max_digits:
            return Err(f'ensure the value of the parameter {name!r} has a maximum of {self.max_digits} digits')
        return Ok(value)


@dataclass(frozen=True, **SLOTS)
class DecimalPlaces(BaseAnnotatedMetadata):
    decimal_places: t.Annotated[int, annotated_types.Ge(0)]

    def __post_init__(self: Self) -> None:
        if self.decimal_places <= 0:
            raise ValueError('invalid `decimal_places` value. The value must be greater than 0')

    def type_check(self: Self, name: str, value: t.Any) -> Ok | Err:  # noqa: ANN401
        cleaned = Decimal(str(value)) if not isinstance(value, Decimal) else value
        _, decimals = extract_digits_and_decimals(cleaned)
        if decimals > self.decimal_places:
            return Err(
                f'ensure the value of the parameter {name!r} has a maximum of {self.decimal_places} decimal places'
            )
        return Ok(value)
