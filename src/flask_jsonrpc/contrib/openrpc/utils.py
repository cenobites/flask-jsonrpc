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

import typing as t

from pydantic.main import BaseModel

from . import typing as st


class MethodExtendSchema(BaseModel):
    name: str | None = None
    params: list[st.ContentDescriptor] | None = None
    result: st.ContentDescriptor | None = None
    tags: list[st.Tag] | None = None
    summary: str | None = None
    description: str | None = None
    external_docs: st.ExternalDocumentation | None = None
    deprecated: bool | None = None
    servers: list[st.Server] | None = None
    errors: list[st.Error] | None = None
    links: list[st.Link] | None = None
    param_structure: st.ParamStructure | None = None
    examples: list[st.ExamplePairing] | None = None
    x_security: dict[str, list[str]] | None = None


def extend_schema(
    name: str | None = None,
    params: list[st.ContentDescriptor] | None = None,
    tags: list[st.Tag] | None = None,
    summary: str | None = None,
    description: str | None = None,
    external_docs: st.ExternalDocumentation | None = None,
    result: st.ContentDescriptor | None = None,
    deprecated: bool | None = None,
    servers: list[st.Server] | None = None,
    errors: list[st.Error] | None = None,
    links: list[st.Link] | None = None,
    param_structure: st.ParamStructure | None = None,
    examples: list[st.ExamplePairing] | None = None,
    x_security: dict[str, list[str]] | None = None,
) -> t.Callable[..., t.Any]:
    def decorator(fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
        method_schema = MethodExtendSchema(
            name=name,
            params=params,
            result=result,
            tags=tags,
            summary=summary,
            description=description,
            external_docs=external_docs,
            deprecated=deprecated,
            servers=servers,
            errors=errors,
            links=links,
            param_structure=param_structure,
            examples=examples,
            x_security=x_security,
        )
        setattr(fn, 'openrpc_method_schema', method_schema)  # noqa: B010
        return fn

    return decorator
