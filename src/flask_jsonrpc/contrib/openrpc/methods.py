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
from functools import lru_cache
from collections import OrderedDict

from flask_jsonrpc.encoders import serializable
from flask_jsonrpc.contrib.openrpc import typing as st
from flask_jsonrpc.contrib.openrpc.utils import MethodExtendSchema, extend_schema

if t.TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite

OPENRPC_DISCOVER_METHOD_NAME: str = 'rpc.discover'
OPENRPC_DISCOVER_SERVICE_METHOD_TYPE: str = 'method'


def _openrpc_discover_method(
    jsonrpc_sites: list[JSONRPCSite], *, openrpc_schema: st.OpenRPCSchema
) -> t.Callable[..., st.OpenRPCSchema]:
    """Create a cached OpenRPC discover method.

    Args:
        jsonrpc_sites (list[flask_jsonrpc.site.JSONRPCSite]): List of JSON-RPC site instances.
        openrpc_schema (flask_jsonrpc.contrib.openrpc.typing.OpenRPCSchema): The OpenRPC schema instance.

    Returns:
        typing.Callable[..., flask_jsonrpc.contrib.openrpc.typing.OpenRPCSchema]: The cached OpenRPC discover method.
    """

    @lru_cache
    @extend_schema(
        name=OPENRPC_DISCOVER_METHOD_NAME,
        description='Returns an OpenRPC schema as a description of this service',
        params=[],
        result=st.ContentDescriptor(
            name='OpenRPC Schema',
            schema_=st.Schema(ref='https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'),  # pyright: ignore
        ),
    )
    def cached_openrpc_discover_method() -> st.OpenRPCSchema:
        jsonrpc_site = jsonrpc_sites[0]
        service_describe_methods = OrderedDict(
            (name, (method_describe, jsonrpc_site.view_funcs[name]))
            for name, method_describe in jsonrpc_site.describe().methods.items()
        )
        for jsonrpc_site in jsonrpc_sites[1:]:
            service_describe_methods.update(
                OrderedDict(
                    (name, (method_describe, jsonrpc_site.view_funcs[name]))
                    for name, method_describe in jsonrpc_site.describe().methods.items()
                    # To ensure that has only one rpc.* method, the others will be disregarded.
                    if not name.startswith('rpc.')
                )
            )

        for name, (method_describe, view_func) in service_describe_methods.items():
            fn_openrpc_method_schema: MethodExtendSchema = t.cast(
                MethodExtendSchema, getattr(view_func, 'openrpc_method_schema', MethodExtendSchema())
            )
            method_schema: dict[str, t.Any] = {
                'name': fn_openrpc_method_schema.name or name,
                'description': fn_openrpc_method_schema.description or method_describe.description,
                'params': [],
                'result': {
                    'name': 'default',
                    'schema': {'type': st.SchemaDataType.from_rpc_describe_type(method_describe.returns.type)},
                },
            }
            method_params_schema: list[dict[str, t.Any]] = []
            for param in method_describe.params:
                method_params_schema.append(
                    {
                        'name': param.name,
                        'schema': {'type': st.SchemaDataType.from_rpc_describe_type(param.type)},
                        'required': param.required or None,
                    }
                )
            method_schema['params'] = method_params_schema
            method_schema_merged = st.Method(
                **{**serializable(method_schema), **serializable(fn_openrpc_method_schema)}
            )
            openrpc_schema.methods.append(method_schema_merged)
        return openrpc_schema

    return cached_openrpc_discover_method  # type: ignore[no-any-return]  # pyright: ignore


def openrpc_discover_method(
    jsonrpc_sites: list[JSONRPCSite], *, openrpc_schema: st.OpenRPCSchema | None = None
) -> t.Callable[..., st.OpenRPCSchema]:
    """Create an OpenRPC discover method.

    Args:
        jsonrpc_sites (list[flask_jsonrpc.site.JSONRPCSite]): List of JSON-RPC site instances.
        openrpc_schema (flask_jsonrpc.contrib.openrpc.typing.OpenRPCSchema | None): The OpenRPC schema instance.
            If None, a default schema will be created.

    Returns:
        typing.Callable[..., flask_jsonrpc.contrib.openrpc.typing.OpenRPCSchema]: The OpenRPC discover method.

    See Also:
        :func:`flask_jsonrpc.contrib.openrpc._openrpc_discover_method`
    """
    if openrpc_schema is None:
        jsonrpc_site = jsonrpc_sites[0]
        jsonrpc_service_describe = jsonrpc_site.describe()
        openrpc_schema = st.OpenRPCSchema(
            info=st.Info(title=jsonrpc_service_describe.name, version='0.0.1'),
            servers=st.Server(name='default', url=jsonrpc_service_describe.servers[0].url),
        )
    return _openrpc_discover_method(jsonrpc_sites, openrpc_schema=openrpc_schema)
