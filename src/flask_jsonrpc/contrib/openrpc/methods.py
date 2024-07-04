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
from collections import OrderedDict

from . import typing as st
from .utils import MethodExtendSchema, extend_schema
from .helpers import openrpc_schema_to_dict, openrpc_method_schema_from_dict

# Python 3.9+
try:
    from functools import cache
except ImportError:  # pragma: no cover
    from functools import lru_cache as cache

if t.TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite

OPENRPC_DISCOVER_METHOD_NAME: str = 'rpc.discover'
OPENRPC_DISCOVER_SERVICE_METHOD_TYPE: str = 'method'


def openrpc_discover_method(
    jsonrpc_sites: t.List['JSONRPCSite'], *, openrpc_schema: t.Optional[st.OpenRPCSchema] = None
) -> t.Callable[..., t.Dict[str, t.Any]]:
    if openrpc_schema is None:
        jsonrpc_site = jsonrpc_sites[0]
        jsonrpc_service_describe = jsonrpc_site.describe()
        openrpc_schema = st.OpenRPCSchema(
            info=st.Info(
                title=jsonrpc_service_describe['name'],
                version='0.0.1',
                description=jsonrpc_service_describe['description'],
            ),
            servers=st.Server(name='default', url=jsonrpc_service_describe['servers'][0]['url']),
        )

    @cache
    @extend_schema(
        name=OPENRPC_DISCOVER_METHOD_NAME,
        description='Returns an OpenRPC schema as a description of this service',
        params=[],
        result=st.ContentDescriptor(
            name='OpenRPC Schema',
            schema=st.Schema(ref='https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'),
        ),
    )
    def openrpc_discover() -> t.Dict[str, t.Any]:
        jsonrpc_site = jsonrpc_sites[0]
        service_describe_methods = OrderedDict(
            (name, (method_describe, jsonrpc_site.view_funcs[name]))
            for name, method_describe in jsonrpc_site.service_methods_desc().items()
        )
        for jsonrpc_site in jsonrpc_sites[1:]:
            service_describe_methods.update(
                OrderedDict(
                    (name, (method_describe, jsonrpc_site.view_funcs[name]))
                    for name, method_describe in jsonrpc_site.service_methods_desc().items()
                    # To ensure that has only one rpc.* method, the others will be disregarded.
                    if not name.startswith('rpc.')
                )
            )

        for name, (method_describe, view_func) in service_describe_methods.items():
            fn_openrpc_method_schema = getattr(view_func, 'openrpc_method_schema', MethodExtendSchema())  # noqa: B010
            openrpc_method_schema = {k: v for k, v in fn_openrpc_method_schema.items() if v is not None}

            method_schema = {
                'name': openrpc_method_schema.get('name', name),
                'description': openrpc_method_schema.get('description', method_describe['description']),
                'result': {
                    'name': 'default',
                    'schema': {'type': st.SchemaDataType.of(method_describe['returns']['type'])},
                },
            }
            method_params_schema = []
            for param in method_describe['params']:
                method_params_schema.append(
                    {
                        'name': param['name'],
                        'schema': {'type': st.SchemaDataType.of(param['type'])},
                        'required': param['required'] or None,
                    }
                )
            method_schema['params'] = method_params_schema

            method_schema_merged = {**method_schema, **openrpc_method_schema}
            openrpc_schema.methods.append(openrpc_method_schema_from_dict(method_schema_merged))
        return openrpc_schema_to_dict(openrpc_schema)

    return openrpc_discover
