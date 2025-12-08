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

from pydantic import ConfigDict
from pydantic.main import BaseModel as PydanticModel

from flask_jsonrpc.contrib.openrpc import typing as st


class BaseModel(PydanticModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


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
    """Decorator to extend the schema of a JSON-RPC method.

    Args:
        name (str | None): The name of the method.
        params (list[flask_jsonrpc.contrib.openrpc.typing.ContentDescriptor] | None): The list of parameter descriptors.
        tags (list[flask_jsonrpc.contrib.openrpc.typing.Tag] | None): The list of tags.
        summary (str | None): The summary of the method.
        description (str | None): The description of the method.
        external_docs (flask_jsonrpc.contrib.openrpc.typing.ExternalDocumentation | None): The external documentation.
        result (flask_jsonrpc.contrib.openrpc.typing.ContentDescriptor | None): The result descriptor.
        deprecated (bool | None): Whether the method is deprecated.
        servers (list[flask_jsonrpc.contrib.openrpc.typing.Server] | None): The list of servers.
        errors (list[flask_jsonrpc.contrib.openrpc.typing.Error] | None): The list of errors.
        links (list[flask_jsonrpc.contrib.openrpc.typing.Link] | None): The list of links.
        param_structure (flask_jsonrpc.contrib.openrpc.typing.ParamStructure | None): The parameter structure.
        examples (list[flask_jsonrpc.contrib.openrpc.typing.ExamplePairing] | None): The list of example pairings.
        x_security (dict[str, list[str]] | None): The security requirements.

    Returns:
        typing.Callable[..., typing.Any]: The decorator function.
    """

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
