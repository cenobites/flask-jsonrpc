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
from __future__ import annotations

import sys
import typing as t
from dataclasses import dataclass

import typing_extensions

if sys.version_info < (3, 10):
    SLOTS = {}
else:  # pragma: no cover
    SLOTS = {'slots': True}

JSONRPC_Method_T = t.TypeVar('JSONRPC_Method_T')


class BaseMethodAnnotatedMetadata:
    __slots__ = ()


@dataclass(frozen=True, **SLOTS)
class Summary(BaseMethodAnnotatedMetadata):
    summary: str


@dataclass(frozen=True, **SLOTS)
class Description(BaseMethodAnnotatedMetadata):
    description: str


@dataclass(frozen=True, **SLOTS)
class Validate(BaseMethodAnnotatedMetadata):
    validate: bool = True


@dataclass(frozen=True, **SLOTS)
class Notification(BaseMethodAnnotatedMetadata):
    notification: bool = True


@dataclass(frozen=True, **SLOTS)
class Deprecated(BaseMethodAnnotatedMetadata):
    deprecated: bool = True


@dataclass(frozen=True, **SLOTS)
class Tag(BaseMethodAnnotatedMetadata):
    name: str
    summary: str | None = None
    description: str | None = None


@dataclass(frozen=True, **SLOTS)
class Error(BaseMethodAnnotatedMetadata):
    code: int
    message: str
    status_code: int = 500
    data: t.Any | None = None


@dataclass(frozen=True, **SLOTS)
class ExampleField(BaseMethodAnnotatedMetadata):
    name: str
    value: t.Any
    summary: str | None = None
    description: str | None = None


@dataclass(frozen=True, **SLOTS)
class Example(BaseMethodAnnotatedMetadata):
    name: str
    summary: str | None = None
    description: str | None = None
    params: list[ExampleField] | None = None
    returns: ExampleField | None = None


class MethodAnnotated:
    __slots__ = ()

    def __new__(cls: type[MethodAnnotated], *args: t.Any, **kwargs: t.Any) -> MethodAnnotated:  # noqa: ANN401
        raise TypeError('type MethodAnnotated cannot be instantiated')

    @t._tp_cache  # type: ignore
    def __class_getitem__(cls: type[MethodAnnotated], params: t.Any, /) -> t.Any:  # noqa: ANN401
        if not isinstance(params, tuple):
            params = (params,)
        return typing_extensions._AnnotatedAlias(JSONRPC_Method_T, params)

    def __init_subclass__(cls: type[MethodAnnotated], /, *args: t.Any, **kwargs: t.Any) -> None:  # noqa: ANN401
        raise TypeError(f'cannot subclass {getattr(cls, "__module__", cls)}.MethodAnnotated')
