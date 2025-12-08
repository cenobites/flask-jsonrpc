# Copyright (c) 2020-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc.globals import default_jsonrpc_site, default_jsonrpc_site_api
from flask_jsonrpc.wrappers import JSONRPCDecoratorMixin

if t.TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite
    from flask_jsonrpc.views import JSONRPCView


class JSONRPCBlueprint(JSONRPCDecoratorMixin):
    """JSON-RPC blueprint for Flask applications.

    Args:
        name (str): The name of the blueprint.
        import_name (str): The import name of the blueprint.
        version (str): The version of the JSON-RPC API. Default is '1.0.0'.
        jsonrpc_site (type[flask_jsonrpc.site.JSONRPCSite]): The JSON-RPC site class to use.
            Default is `flask_jsonrpc.globals.default_jsonrpc_site`.
        jsonrpc_site_api (type[flask_jsonrpc.views.JSONRPCView]): The JSON-RPC site API class to use.
            Default is `flask_jsonrpc.globals.default_jsonrpc_site_api`.

    Attributes:
        name (str): The name of the blueprint.
        import_name (str): The import name of the blueprint.
        version (str): The version of the JSON-RPC API.
        jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): The JSON-RPC site instance.
        jsonrpc_site_api (type[flask_jsonrpc.views.JSONRPCView]): The JSON-RPC site API class.

    Examples:
        >>> from flask_jsonrpc import JSONRPCBlueprint
        >>>
        >>> jsonrpc_bp = JSONRPCBlueprint('api', __name__, version='1.0.0')
        >>>
        >>> # Disable automatic validation for typechecking limitations with doctests
        >>> # We always recommend to use validation in real applications
        >>> @jsonrpc_bp.method('my_method', validate=False)
        ... def my_method(param1: int) -> str:
        ...     return str(param1)
    """

    def __init__(
        self: Self,
        name: str,
        import_name: str,
        version: str = '1.0.0',
        jsonrpc_site: type[JSONRPCSite] = default_jsonrpc_site,
        jsonrpc_site_api: type[JSONRPCView] = default_jsonrpc_site_api,
    ) -> None:
        self.name = name
        self.import_name = import_name
        self.version = version
        self.jsonrpc_site = jsonrpc_site(version=version)
        self.jsonrpc_site_api = jsonrpc_site_api

    def get_jsonrpc_site(self: Self) -> JSONRPCSite:
        """Get the JSON-RPC site instance.

        Returns:
            flask_jsonrpc.site.JSONRPCSite: The JSON-RPC site instance.
        """
        return self.jsonrpc_site

    def get_jsonrpc_site_api(self: Self) -> type[JSONRPCView]:
        """Get the JSON-RPC site API class.

        Returns:
            type[flask_jsonrpc.views.JSONRPCView]: The JSON-RPC site API class.
        """
        return self.jsonrpc_site_api

    def register(
        self: Self,
        view_func: t.Callable[..., t.Any],
        name: str | None = None,
        **options: t.Any,  # noqa: ANN401
    ) -> None:
        """Register a view function with the JSON-RPC blueprint.

        Args:
            view_func (typing.Callable[..., typing.Any]): The view function to register.
            name (str | None): The name of the method. If None, the function's __name__ is used.
            **options (typing.Any): Additional options for the method registration.

        Examples:
            >>> from flask_jsonrpc import JSONRPCBlueprint
            >>>
            >>> jsonrpc_bp = JSONRPCBlueprint('api', __name__, version='1.0.0')
            >>>
            ... def my_method(param1: int) -> str:
            ...     return str(param1)
            >>>
            >>> # Disable automatic validation for typechecking limitations with doctests
            >>> # We always recommend to use validation in real applications
            >>> jsonrpc_bp.register(my_method, name='my_method', validate=False)
        """
        self.register_view_function(view_func, name, **options)
