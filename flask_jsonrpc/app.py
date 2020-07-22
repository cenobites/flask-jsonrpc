# -*- coding: utf-8 -*-
# Copyright (c) 2020-2020, Cenobit Technologies, Inc. http://cenobit.es/
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
from typing import TYPE_CHECKING, Any, Type, Union, Callable, Optional

from flask import Flask

from .globals import default_jsonrpc_site, default_jsonrpc_site_api
from .helpers import urn
from .wrappers import JSONRCPDecoratorMixin
from .contrib.browse import create_browse

if TYPE_CHECKING:
    from .site import JSONRPCSite
    from .views import JSONRPCView
    from .blueprints import JSONRPCBlueprint


class JSONRPC(JSONRCPDecoratorMixin):
    def __init__(
        self,
        app: Optional[Flask] = None,
        service_url: str = '/api',
        jsonrpc_site: Type['JSONRPCSite'] = default_jsonrpc_site,
        jsonrpc_site_api: Type['JSONRPCView'] = default_jsonrpc_site_api,
        enable_web_browsable_api: bool = False,
    ) -> None:
        self.app = app
        self.service_url = service_url
        self.jsonrpc_site = jsonrpc_site()
        self.jsonrpc_site_api = jsonrpc_site_api
        self.browse_url = self._make_browse_url(service_url)
        self.enable_web_browsable_api = enable_web_browsable_api
        if app:
            self.init_app(app)

    def get_jsonrpc_site(self) -> 'JSONRPCSite':
        return self.jsonrpc_site

    def get_jsonrpc_site_api(self) -> Type['JSONRPCView']:
        return self.jsonrpc_site_api

    def _make_browse_url(self, service_url: str) -> str:
        return ''.join([service_url, '/browse']) if not service_url.endswith('/') else ''.join([service_url, 'browse'])

    def init_app(self, app: Flask) -> None:
        app.add_url_rule(
            self.service_url,
            view_func=self.get_jsonrpc_site_api().as_view(
                urn('app', app.name, self.service_url), jsonrpc_site=self.get_jsonrpc_site()
            ),
        )
        self.register_browse(app, self)

    def register(
        self, view_func: Callable[..., Any], name: Optional[str] = None, validate: bool = True, **options: Any
    ) -> None:
        self.register_view_function(view_func, name, validate, **options)

    def register_blueprint(
        self, app: Flask, jsonrpc_app: 'JSONRPCBlueprint', url_prefix: str, enable_web_browsable_api: bool = False
    ) -> None:
        service_url = ''.join([self.service_url, url_prefix]) if url_prefix else self.service_url
        app.add_url_rule(
            service_url,
            view_func=jsonrpc_app.get_jsonrpc_site_api().as_view(
                urn('blueprint', app.name, jsonrpc_app.name, service_url), jsonrpc_site=jsonrpc_app.get_jsonrpc_site()
            ),
        )

        if enable_web_browsable_api:
            self.register_browse(app, jsonrpc_app, url_prefix=url_prefix)

    def register_browse(
        self, app: Flask, jsonrpc_app: Union['JSONRPC', 'JSONRPCBlueprint'], url_prefix: Optional[str] = None
    ) -> None:
        browse_url = ''.join([self.service_url, url_prefix, '/browse']) if url_prefix else self.browse_url
        if app.config['DEBUG'] or self.enable_web_browsable_api:
            app.register_blueprint(
                create_browse(urn('browse', app.name, browse_url), jsonrpc_app.get_jsonrpc_site()),
                url_prefix=browse_url,
            )
            app.add_url_rule(browse_url + '/static/<path:filename>', 'browse.static', view_func=app.send_static_file)
