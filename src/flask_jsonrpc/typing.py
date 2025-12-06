# Copyright (c) 2023-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
from collections import OrderedDict

from pydantic import ConfigDict
from pydantic.main import BaseModel as PydanticModel


class BaseModel(PydanticModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Field(BaseModel):
    name: str
    type: str
    summary: str | None = None
    description: str | None = None
    properties: t.Mapping[str, Field] | None = None
    examples: list[t.Any] | None = None
    required: bool | None = None
    deprecated: bool | None = None
    nullable: bool | None = None
    minimum: float | None = None
    maximum: float | None = None
    multiple_of: float | None = None
    min_length: int | None = None
    max_length: int | None = None
    pattern: str | t.Pattern[str] | None = None
    allow_inf_nan: bool | None = None
    max_digits: int | None = None
    decimal_places: int | None = None


class ExampleField(BaseModel):
    name: str
    value: t.Any
    summary: str | None = None
    description: str | None = None


class Example(BaseModel):
    name: str | None = None
    summary: str | None = None
    description: str | None = None
    params: list[ExampleField] | None = None
    returns: ExampleField | None = None


class Error(BaseModel):
    code: int
    message: str
    data: t.Any | None = None
    status_code: int


class Method(BaseModel):
    name: str
    type: str
    summary: str | None = None
    description: str | None = None
    validation: bool = True
    notification: bool = True
    deprecated: bool | None = None
    params: list[Field] = []
    returns: Field
    tags: list[str] | None = None
    errors: list[Error] | None = None
    examples: list[Example] | None = None


class Server(BaseModel):
    url: str
    description: str | None = None


class ServiceDescribe(BaseModel):
    id: str
    name: str
    version: str
    title: str | None = None
    description: str | None = None
    servers: list[Server]
    methods: OrderedDict[str, Method]
