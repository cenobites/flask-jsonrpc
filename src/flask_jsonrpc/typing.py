# Copyright (c) 2023-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
import sys
import typing as t

from pydantic.main import BaseModel

# Python 3.8
if sys.version_info[:2] == (3, 8):  # pragma: no cover
    from typing import OrderedDict
else:  # pragma: no cover
    from collections import OrderedDict


class ServiceMethodParamsDescribe(BaseModel):
    type: str
    name: str
    required: t.Optional[bool] = None
    nullable: t.Optional[bool] = None
    minimum: t.Optional[int] = None
    maximum: t.Optional[int] = None
    pattern: t.Optional[str] = None
    length: t.Optional[int] = None
    description: t.Optional[str] = None


class ServiceMethodReturnsDescribe(BaseModel):
    type: str


class ServiceMethodDescribe(BaseModel):
    type: str
    description: t.Optional[str] = None
    options: t.Dict[str, t.Any] = {}
    params: t.List[ServiceMethodParamsDescribe] = []
    returns: ServiceMethodReturnsDescribe


class ServiceServersDescribe(BaseModel):
    url: str
    description: t.Optional[str] = None


class ServiceDescribe(BaseModel):
    id: str
    version: str
    name: str
    description: t.Optional[str] = None
    servers: t.List[ServiceServersDescribe]
    methods: OrderedDict[str, ServiceMethodDescribe]
