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

import typing as t
import operator
from dataclasses import dataclass

# Added in version 3.11.
from typing_extensions import Self, Unpack, TypeVarTuple

SLOTS = {'slots': True}

JSONRPC_Method_T = t.TypeVar('JSONRPC_Method_T')
JSONRPC_Method_Metadata_T = t.TypeVar('JSONRPC_Method_Metadata_T', bound='BaseMethodAnnotatedMetadata')
JSONRPC_Method_Metadata_Ts = TypeVarTuple('JSONRPC_Method_Metadata_Ts')


class BaseMethodAnnotatedOrigin:
    pass


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


class _MethodAnnotated(t.Generic[JSONRPC_Method_T, Unpack[JSONRPC_Method_Metadata_Ts]]):
    pass


class _MethodAnnotatedAlias(t._GenericAlias, _root=True):  # type: ignore
    def __init__(
        self: Self, origin: type[BaseMethodAnnotatedOrigin], metadata: tuple[BaseMethodAnnotatedMetadata, ...]
    ) -> None:
        if isinstance(origin, _MethodAnnotatedAlias):
            metadata = origin.__metadata__ + metadata  # type: ignore[attr-defined]
            origin = origin.__origin__  # type: ignore[attr-defined]
        super().__init__(origin, origin)
        self.__metadata__ = metadata
        self.origin = origin
        self.metadata = metadata

    def __repr__(self: Self) -> str:
        return (
            f'flask_jsonrpc.types.methods._MethodAnnotated[{t._type_repr(self.__origin__)}, '
            f'{", ".join(repr(a) for a in self.__metadata__)}]'
        )

    def __reduce__(self: Self) -> tuple[t.Any, ...]:
        return operator.getitem, (_MethodAnnotated, (self.__origin__, *self.__metadata__))

    def __eq__(self: Self, other: object) -> bool:  # noqa: ANN204
        if not isinstance(other, _MethodAnnotatedAlias):
            return NotImplemented
        if self.__origin__ != other.__origin__:
            return False
        return self.__metadata__ == other.__metadata__

    def __hash__(self: Self) -> int:
        return hash((self.__origin__, self.__metadata__))


class _MethodAnnotatedProxy:
    def __getitem__(
        self: Self, params: BaseMethodAnnotatedMetadata | tuple[BaseMethodAnnotatedMetadata, ...]
    ) -> _MethodAnnotatedAlias:
        if not isinstance(params, tuple):
            params = (params,)
        return _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, params)


MethodAnnotated = _MethodAnnotatedProxy()
MethodAnnotatedType = _MethodAnnotatedAlias
