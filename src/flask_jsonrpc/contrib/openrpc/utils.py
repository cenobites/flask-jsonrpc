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
import typing as t

from . import typing as st

# Python 3.8+
try:
    from typing_extensions import TypedDict
except ImportError:  # pragma: no cover
    from typing import TypedDict  # pylint: disable=C0412


class MethodExtendSchema(TypedDict, total=False):
    name: t.Optional[str]
    params: t.Optional[t.List[st.ContentDescriptor]]
    result: t.Optional[st.ContentDescriptor]
    tags: t.Optional[t.List[st.Tag]]
    summary: t.Optional[str]
    description: t.Optional[str]
    external_docs: t.Optional[st.ExternalDocumentation]
    deprecated: t.Optional[bool]
    servers: t.Optional[t.List[st.Server]]
    errors: t.Optional[t.List[st.Error]]
    links: t.Optional[t.List[st.Link]]
    param_structure: t.Optional[st.ParamStructure]
    examples: t.Optional[t.List[st.ExamplePairing]]
    x_security: t.Optional[t.Dict[str, t.List[str]]]


def extend_schema(
    name: t.Optional[str] = None,
    params: t.Optional[t.List[st.ContentDescriptor]] = None,
    tags: t.Optional[t.List[st.Tag]] = None,
    summary: t.Optional[str] = None,
    description: t.Optional[str] = None,
    external_docs: t.Optional[st.ExternalDocumentation] = None,
    result: t.Optional[st.ContentDescriptor] = None,
    deprecated: t.Optional[bool] = None,
    servers: t.Optional[t.List[st.Server]] = None,
    errors: t.Optional[t.List[st.Error]] = None,
    links: t.Optional[t.List[st.Link]] = None,
    param_structure: t.Optional[st.ParamStructure] = None,
    examples: t.Optional[t.List[st.ExamplePairing]] = None,
    x_security: t.Optional[t.Dict[str, t.List[str]]] = None,
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
