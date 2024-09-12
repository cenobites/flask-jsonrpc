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
from urllib.parse import urlsplit

from . import typing as fjt  # pylint: disable=W0404
from .helpers import from_python_type

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if t.TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite

JSONRPC_DESCRIBE_METHOD_NAME: str = 'rpc.describe'
JSONRPC_DESCRIBE_SERVICE_METHOD_TYPE: str = 'method'


class JSONRPCServiceDescriptor:
    def __init__(self: Self, jsonrpc_site: 'JSONRPCSite') -> None:
        self.jsonrpc_site = jsonrpc_site
        self.register(jsonrpc_site)

    def register(self: Self, jsonrpc_site: 'JSONRPCSite') -> None:
        def describe() -> fjt.ServiceDescribe:
            return self.service_describe()

        fn_annotations = {'return': fjt.ServiceDescribe}
        setattr(describe, 'jsonrpc_method_name', JSONRPC_DESCRIBE_METHOD_NAME)  # noqa: B010
        setattr(describe, 'jsonrpc_method_sig', fn_annotations)  # noqa: B010
        setattr(describe, 'jsonrpc_method_return', fn_annotations.pop('return', None))  # noqa: B010
        setattr(describe, 'jsonrpc_method_params', fn_annotations)  # noqa: B010
        setattr(describe, 'jsonrpc_validate', True)  # noqa: B010
        setattr(describe, 'jsonrpc_notification', False)  # noqa: B010
        setattr(describe, 'jsonrpc_options', {})  # noqa: B010
        jsonrpc_site.register(JSONRPC_DESCRIBE_METHOD_NAME, describe)
        self.describe = describe

    def python_type_name(self: Self, pytype: t.Any) -> str:  # noqa: ANN401
        return str(from_python_type(pytype))

    def service_method_params_desc(
        self: Self, view_func: t.Callable[..., t.Any]
    ) -> t.List[fjt.ServiceMethodParamsDescribe]:
        return [
            fjt.ServiceMethodParamsDescribe(  # pytype: disable=missing-parameter
                name=name, type=self.python_type_name(tp), required=False, nullable=False
            )
            for name, tp in getattr(view_func, 'jsonrpc_method_params', {}).items()
        ]

    def service_methods_desc(self: Self) -> t.OrderedDict[str, fjt.ServiceMethodDescribe]:
        methods: t.OrderedDict[str, fjt.ServiceMethodDescribe] = OrderedDict()
        for key, view_func in self.jsonrpc_site.view_funcs.items():
            name = getattr(view_func, 'jsonrpc_method_name', key)
            methods[name] = fjt.ServiceMethodDescribe(  # pytype: disable=missing-parameter
                type=JSONRPC_DESCRIBE_SERVICE_METHOD_TYPE,
                description=getattr(view_func, '__doc__', None),
                options=getattr(view_func, 'jsonrpc_options', {}),
                params=self.service_method_params_desc(view_func),
                returns=fjt.ServiceMethodReturnsDescribe(
                    type=self.python_type_name(getattr(view_func, 'jsonrpc_method_return', type(None)))
                ),
            )
        return methods

    def service_server_url(self: Self) -> str:
        url = urlsplit(self.jsonrpc_site.base_url or self.jsonrpc_site.path)
        return (
            f"{url.scheme!r}://{url.netloc!r}/{(self.jsonrpc_site.path or '').lstrip('/')}"
            if self.jsonrpc_site.base_url
            else str(url.path)
        )

    def service_describe(self: Self) -> fjt.ServiceDescribe:
        return fjt.ServiceDescribe(
            id=f'urn:uuid:{self.jsonrpc_site.uuid}',
            version=self.jsonrpc_site.version,
            name=self.jsonrpc_site.name,
            description=self.jsonrpc_site.__doc__,
            servers=[fjt.ServiceServersDescribe(url=self.service_server_url())],  # pytype: disable=missing-parameter
            methods=self.service_methods_desc(),
        )
