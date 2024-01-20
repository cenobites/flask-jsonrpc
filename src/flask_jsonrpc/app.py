# Copyright (c) 2020-2022, Cenobit Technologies, Inc. http://cenobit.es/
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
from urllib.parse import urlsplit

from flask import Flask

from .globals import default_jsonrpc_site, default_jsonrpc_site_api
from .helpers import urn
from .wrappers import JSONRPCDecoratorMixin
from .contrib.browse import JSONRPCBrowse

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if t.TYPE_CHECKING:
    from .site import JSONRPCSite
    from .views import JSONRPCView
    from .blueprints import JSONRPCBlueprint


class JSONRPC(JSONRPCDecoratorMixin):
    def __init__(
        self: Self,
        app: t.Optional[Flask] = None,
        service_url: str = '/api',
        jsonrpc_site: t.Type['JSONRPCSite'] = default_jsonrpc_site,
        jsonrpc_site_api: t.Type['JSONRPCView'] = default_jsonrpc_site_api,
        enable_web_browsable_api: bool = False,
    ) -> None:
        self.app = app
        self.path = service_url
        self.base_url: t.Optional[str] = None
        self.jsonrpc_site = jsonrpc_site()
        self.jsonrpc_site_api = jsonrpc_site_api
        self.jsonrpc_browse: t.Optional[JSONRPCBrowse] = None
        self.enable_web_browsable_api = enable_web_browsable_api
        if app:
            self.init_app(app)

    def get_jsonrpc_site(self: Self) -> 'JSONRPCSite':
        return self.jsonrpc_site

    def get_jsonrpc_site_api(self: Self) -> t.Type['JSONRPCView']:
        return self.jsonrpc_site_api

    def _make_jsonrpc_browse_url(self: Self, path: str) -> str:
        return ''.join([path.rstrip('/'), '/browse'])

    def init_app(self: Self, app: Flask) -> None:
        http_host = app.config.get('SERVER_NAME')
        app_root = app.config['APPLICATION_ROOT']
        url_scheme = app.config['PREFERRED_URL_SCHEME']
        url = urlsplit(self.path)

        self.path = f"{app_root.rstrip('/')}{url.path}"
        self.base_url = (
            f"{url.scheme or url_scheme}://{url.netloc or http_host}/{self.path.lstrip('/')}" if http_host else None
        )

        self.get_jsonrpc_site().set_path(self.path)
        self.get_jsonrpc_site().set_base_url(self.base_url)

        app.add_url_rule(
            self.path,
            view_func=self.get_jsonrpc_site_api().as_view(
                urn('app', app.name, self.path), jsonrpc_site=self.get_jsonrpc_site()
            ),
        )

        if app.config['DEBUG'] or self.enable_web_browsable_api:
            self.init_browse_app(app)

    def register(
        self: Self,
        view_func: t.Callable[..., t.Any],
        name: t.Optional[str] = None,
        **options: t.Any,  # noqa: ANN401
    ) -> None:
        self.register_view_function(view_func, name, **options)

    def register_blueprint(
        self: Self,
        app: Flask,
        jsonrpc_app: 'JSONRPCBlueprint',
        url_prefix: t.Optional[str] = None,
        enable_web_browsable_api: bool = False,
    ) -> None:
        path = ''.join([self.path, '/', url_prefix.lstrip('/')]) if url_prefix else self.path
        path_url = urlsplit(path)

        url = urlsplit(self.base_url or path)
        base_url = f"{url.scheme}://{url.netloc}/{url.path.lstrip('/')}" if self.base_url else None

        jsonrpc_app.get_jsonrpc_site().set_path(path_url.path)
        jsonrpc_app.get_jsonrpc_site().set_base_url(base_url)

        app.add_url_rule(
            path,
            view_func=jsonrpc_app.get_jsonrpc_site_api().as_view(
                urn('blueprint', app.name, jsonrpc_app.name, path), jsonrpc_site=jsonrpc_app.get_jsonrpc_site()
            ),
        )

        if app.config['DEBUG'] or enable_web_browsable_api:
            self.register_browse(jsonrpc_app)

    def init_browse_app(self: Self, app: Flask, path: t.Optional[str] = None, base_url: t.Optional[str] = None) -> None:
        browse_url = self._make_jsonrpc_browse_url(path or self.path)
        self.jsonrpc_browse = JSONRPCBrowse(app, url_prefix=browse_url, base_url=base_url or self.base_url)
        self.jsonrpc_browse.register_jsonrpc_site(self.get_jsonrpc_site())

    def register_browse(self: Self, jsonrpc_app: t.Union['JSONRPC', 'JSONRPCBlueprint']) -> None:
        if not self.jsonrpc_browse:
            raise RuntimeError(
                'You need to init the Browse app before register the Site, see JSONRPC.init_browse_app(...)'
            )
        self.jsonrpc_browse.register_jsonrpc_site(jsonrpc_app.get_jsonrpc_site())
