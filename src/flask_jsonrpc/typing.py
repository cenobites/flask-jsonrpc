# Copyright (c) 2023-2023, Cenobit Technologies, Inc. http://cenobit.es/
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

# Python 3.8+
try:
    from typing_extensions import TypedDict
except ImportError:  # pragma: no cover
    from typing import TypedDict  # pylint: disable=C0412


class ServiceMethodParamsDescribe(TypedDict, total=False):
    type: str
    name: str
    required: bool
    nullable: bool
    minimum: t.Optional[int]
    maximum: t.Optional[int]
    pattern: t.Optional[str]
    length: t.Optional[int]
    description: t.Optional[str]


class ServiceMethodReturnsDescribe(TypedDict):
    type: str


class ServiceMethodDescribe(TypedDict):
    type: str
    description: t.Optional[str]
    options: t.Dict[str, t.Any]
    params: t.List[ServiceMethodParamsDescribe]
    returns: ServiceMethodReturnsDescribe


class ServiceServersDescribe(TypedDict, total=False):
    url: str
    description: t.Optional[str]


class ServiceDescribe(TypedDict):
    id: str
    version: str
    name: str
    description: t.Optional[str]
    servers: t.List[ServiceServersDescribe]
    methods: t.Dict[str, ServiceMethodDescribe]
