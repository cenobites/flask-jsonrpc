# Copyright (c) 2020-2024, Cenobit Technologies, Inc. http://cenobit.es/
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

from .globals import default_jsonrpc_site, default_jsonrpc_site_api
from .wrappers import JSONRPCDecoratorMixin

if t.TYPE_CHECKING:
    from .site import JSONRPCSite
    from .views import JSONRPCView


class JSONRPCBlueprint(JSONRPCDecoratorMixin):
    def __init__(
        self: Self,
        name: str,
        import_name: str,
        jsonrpc_site: type[JSONRPCSite] = default_jsonrpc_site,
        jsonrpc_site_api: type[JSONRPCView] = default_jsonrpc_site_api,
    ) -> None:
        self.name = name
        self.import_name = import_name
        self.jsonrpc_site = jsonrpc_site()
        self.jsonrpc_site_api = jsonrpc_site_api

    def get_jsonrpc_site(self: Self) -> JSONRPCSite:
        return self.jsonrpc_site

    def get_jsonrpc_site_api(self: Self) -> type[JSONRPCView]:
        return self.jsonrpc_site_api

    def register(
        self: Self,
        view_func: t.Callable[..., t.Any],
        name: str | None = None,
        **options: t.Any,  # noqa: ANN401
    ) -> None:
        self.register_view_function(view_func, name, **options)
