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

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc.contrib.openrpc.methods import OPENRPC_DISCOVER_METHOD_NAME, openrpc_discover_method
from flask_jsonrpc.contrib.openrpc.wrappers import OpenRPCExtendSchemaDecoratorMixin

if t.TYPE_CHECKING:
    from flask import Flask

    from flask_jsonrpc.app import JSONRPC
    from flask_jsonrpc.contrib.openrpc.typing import OpenRPCSchema


class OpenRPC(OpenRPCExtendSchemaDecoratorMixin):
    """Flask-JSONRPC OpenRPC contrib extension.

    Args:
        app (flask.Flask | None): The Flask application instance. Defaults to None.
        jsonrpc_app (flask_jsonrpc.app.JSONRPC | None): The JSON-RPC application instance. Defaults to None.
        openrpc_schema (flask_jsonrpc.contrib.openrpc.typing.OpenRPCSchema | None): The OpenRPC schema instance.
            Defaults to None.

    Attributes:
        jsonrpc_app (flask_jsonrpc.app.JSONRPC | None): The JSON-RPC application instance.
        openrpc_schema (flask_jsonrpc.contrib.openrpc.typing.OpenRPCSchema | None): The OpenRPC schema instance.
    """

    def __init__(
        self: Self,
        app: Flask | None = None,
        jsonrpc_app: JSONRPC | None = None,
        *,
        openrpc_schema: OpenRPCSchema | None = None,
    ) -> None:
        self.jsonrpc_app = jsonrpc_app
        self.openrpc_schema = openrpc_schema
        if app and jsonrpc_app:
            self.init_app(app, jsonrpc_app)

    def init_app(self: Self, app: Flask, jsonrpc_app: JSONRPC) -> None:
        """Initialize the OpenRPC extension with the Flask and JSON-RPC application instances.

        Registers the OpenRPC discover method to the JSON-RPC site.

        Args:
            app (flask.Flask): The Flask application instance.
            jsonrpc_app (flask_jsonrpc.app.JSONRPC): The JSON-RPC application instance.
        """
        jsonrpc_site = jsonrpc_app.get_jsonrpc_site()
        jsonrpc_sites = [japp.get_jsonrpc_site() for japp in jsonrpc_app.jsonrpc_apps]
        jsonrpc_app.get_jsonrpc_site().register(
            OPENRPC_DISCOVER_METHOD_NAME,
            openrpc_discover_method([jsonrpc_site] + jsonrpc_sites, openrpc_schema=self.openrpc_schema),
        )
        for site in jsonrpc_sites:
            site.register(
                OPENRPC_DISCOVER_METHOD_NAME, openrpc_discover_method([site], openrpc_schema=self.openrpc_schema)
            )
