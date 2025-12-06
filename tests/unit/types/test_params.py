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
import re
import math
import typing as t
from decimal import Decimal

import pytest

from flask_jsonrpc.types.params import (
    Ok,
    Err,
    Example,
    Maximum,
    Minimum,
    Pattern,
    Summary,
    Nullable,
    Required,
    MaxDigits,
    MaxLength,
    MinLength,
    Deprecated,
    MultipleOf,
    Properties,
    AllowInfNan,
    Description,
    DecimalPlaces,
    BaseAnnotatedMetadata,
    DefaultTypeCheckMixin,
)


def test_base_annotated_metadata() -> None:
    base = BaseAnnotatedMetadata()
    assert hasattr(base, '__slots__')
    assert base.__slots__ == ()
    with pytest.raises(NotImplementedError):
        base.type_check('test', None)


def test_default_type_check_mixin() -> None:
    mixin = DefaultTypeCheckMixin()
    assert mixin.type_check('param_name', None) == Ok(None)


def test_paramannotated_type() -> None:
    assert isinstance(Maximum(maximum=10.0), Maximum)
    assert isinstance(Minimum(minimum=1.0), Minimum)
    assert isinstance(MultipleOf(multiple_of=10.0), MultipleOf)


def test_summary() -> None:
    summary = Summary('test')
    assert summary.type_check('test', 'value') == Ok('value')


def test_description() -> None:
    description = Description('test')
    assert description.type_check('test', 'value') == Ok('value')


def test_properties() -> None:
    properties = Properties(
        {
            'test1': t.Annotated[str, 'test1 metadata'],
            'test2': t.Annotated[int, 'test2 metadata'],
            'test3': t.Annotated[list[str], 'test3 metadata'],
            'test4': Properties(
                {
                    'test41': t.Annotated[str, 'test41 metadata'],
                    'test42': Properties({'test421': Properties({'test4211': t.Annotated[str, 'test4211 metadata']})}),
                }
            ),
        }
    )
    assert properties.type_check('test', 'value') == Ok('value')


def test_example() -> None:
    example = Example('test', 'test')
    assert example.type_check('test', 'value') == Ok('value')


def test_required() -> None:
    required = Required()
    assert required.type_check('test', 'value') == Ok('value')
    assert required.type_check('test', None) == Err("ensure the value of the parameter 'test' is not empty")
    no_required = Required(required=False)
    assert no_required.type_check('test', None) == Ok(None)


def test_deprecated() -> None:
    deprecated = Deprecated()
    assert deprecated.type_check('test', 'value') == Ok('value')


def test_nullable() -> None:
    nullable = Nullable(nullable=True)
    assert nullable.type_check('test', None) == Ok(None)
    assert nullable.type_check('test', 'value') == Ok('value')
    no_nullable = Nullable(nullable=False)
    assert no_nullable.type_check('test', None) == Err("ensure the parameter 'test' is not null")


def test_maximum() -> None:
    maximum = Maximum(maximum=10)
    assert maximum.type_check('test', 10) == Ok(10)
    assert maximum.type_check('test', 5) == Ok(5)
    assert maximum.type_check('test', 15) == Err("ensure the value of the parameter 'test' is less than or equal to 10")


def test_minimum() -> None:
    minimum = Minimum(minimum=5)
    assert minimum.type_check('test', 5) == Ok(5)
    assert minimum.type_check('test', 10) == Ok(10)
    assert minimum.type_check('test', 3) == Err(
        "ensure the value of the parameter 'test' is greater than or equal to 5"
    )


def test_multiple_of() -> None:
    multiple_of = MultipleOf(multiple_of=5)
    assert multiple_of.type_check('test', 10) == Ok(10)
    assert multiple_of.type_check('test', 7) == Err("ensure the value of the parameter 'test' is a multiple of 5")
    with pytest.raises(ValueError):
        MultipleOf(multiple_of=-1)


def test_max_length() -> None:
    max_length = MaxLength(max_length=5)
    assert max_length.type_check('test', 'hello') == Ok('hello')
    assert max_length.type_check('test', 'hello world') == Err(
        "ensure the value of the parameter 'test' is less than or equal to 5"
    )
    with pytest.raises(ValueError):
        MaxLength(max_length=0)


def test_min_length() -> None:
    min_length = MinLength(min_length=3)
    assert min_length.type_check('test', 'hi') == Err(
        "ensure the value of the parameter 'test' is greater than or equal to 3"
    )
    assert min_length.type_check('test', 'hello') == Ok('hello')
    with pytest.raises(ValueError):
        MinLength(0)


def test_pattern() -> None:
    pattern = Pattern(pattern=re.compile(r'^\d{3}-\d{2}-\d{4}$'))
    assert pattern.type_check('test', '123-45-6789') == Ok('123-45-6789')
    assert pattern.type_check('test', '123-456-789') == Err(
        "ensure the value of the parameter 'test' matches the valid pattern re.compile('^\\\\d{3}-\\\\d{2}-\\\\d{4}$')"
    )
    pattern_str = Pattern(pattern=r'^\d{3}-\d{2}-\d{4}$')
    assert pattern_str.type_check('test', '123-45-6789') == Ok('123-45-6789')
    assert pattern_str.type_check('test', '123-456-789') == Err(
        "ensure the value of the parameter 'test' matches the valid pattern '^\\\\d{3}-\\\\d{2}-\\\\d{4}$'"
    )


def test_allow_inf_nan() -> None:
    allow_inf_nan = AllowInfNan(allow_inf_nan=False)
    assert allow_inf_nan.type_check('test', 1) == Ok(1)
    assert allow_inf_nan.type_check('test', math.inf) == Err(
        "ensure the value of the parameter 'test' is not infinity, negative infinity, or NaN"
    )
    assert allow_inf_nan.type_check('test', math.nan) == Err(
        "ensure the value of the parameter 'test' is not infinity, negative infinity, or NaN"
    )


def test_max_digits() -> None:
    max_digits = MaxDigits(max_digits=5)
    assert max_digits.type_check('test', 1) == Ok(1)
    assert max_digits.type_check('test', 12345) == Ok(12345)
    assert max_digits.type_check('test', 1) == Ok(1)
    assert max_digits.type_check('test', '1.23') == Ok('1.23')
    assert max_digits.type_check('test', '4.08E+10') == Err(
        "ensure the value of the parameter 'test' has a maximum of 5 digits"
    )
    assert max_digits.type_check('test', '4.08E-10') == Ok('4.08E-10')
    assert max_digits.type_check('test', 123456) == Err(
        "ensure the value of the parameter 'test' has a maximum of 5 digits"
    )
    big_max_digits = MaxDigits(max_digits=100**100)
    assert big_max_digits.type_check('test', 10**10) == Ok(10**10)
    assert big_max_digits.type_check('test', 10 ** (-10)) == Ok(10 ** (-10))
    assert big_max_digits.type_check('test', Decimal('0E+1')) == Ok(Decimal('0E+1'))
    with pytest.raises(TypeError):
        max_digits.type_check('test', '-inf')
    with pytest.raises(ValueError):
        MaxDigits(0)


def test_decimal_places() -> None:
    decimal_places = DecimalPlaces(decimal_places=2)
    assert decimal_places.type_check('test', Decimal(12.00)) == Ok(Decimal('12.00'))
    assert decimal_places.type_check('test', 12.00) == Ok(12.00)
    assert decimal_places.type_check('test', 12.34) == Ok(12.34)
    assert decimal_places.type_check('test', 1) == Ok(1)
    assert decimal_places.type_check('test', '1.23') == Ok('1.23')
    assert decimal_places.type_check('test', '4.08E+10') == Ok('4.08E+10')
    assert decimal_places.type_check('test', '4.08E-10') == Err(
        "ensure the value of the parameter 'test' has a maximum of 2 decimal places"
    )
    assert decimal_places.type_check('test', 12.345) == Err(
        "ensure the value of the parameter 'test' has a maximum of 2 decimal places"
    )
    with pytest.raises(TypeError):
        decimal_places.type_check('test', 'inf')
    with pytest.raises(ValueError):
        DecimalPlaces(0)
