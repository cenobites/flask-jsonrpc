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
import logging
from urllib.parse import urlsplit

# Added in version 3.11.
from typing_extensions import Self

from flask import Flask
from flask.logging import has_level_handler

from flask_jsonrpc.conf import settings
from flask_jsonrpc.globals import default_jsonrpc_site, default_jsonrpc_site_api
from flask_jsonrpc.helpers import urn
from flask_jsonrpc.wrappers import JSONRPCDecoratorMixin
from flask_jsonrpc.contrib.browse import JSONRPCBrowse

if t.TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite
    from flask_jsonrpc.views import JSONRPCView
    from flask_jsonrpc.blueprints import JSONRPCBlueprint


class JSONRPC(JSONRPCDecoratorMixin):
    """Flask JSON-RPC application wrapper.

    Manages the integration of JSON-RPC functionality into a Flask application.

    Args:
        app (flask.Flask | None): The Flask application instance. If provided, the JSON-RPC
            application will be initialized with this Flask app.
        path (str): The URL path where the JSON-RPC application will be accessible. Defaults to '/api'.
        version (str): The version of the JSON-RPC application. Defaults to '1.0.0'.
        jsonrpc_site (type[flask_jsonrpc.site.JSONRPCSite]): The JSON-RPC site class to use.
            Defaults to the default JSON-RPC site.
        jsonrpc_site_api (type[flask_jsonrpc.views.JSONRPCView]): The JSON-RPC site API class to use. Defaults to the
            default JSON-RPC site API.
        enable_web_browsable_api (bool | None): Whether to enable the web browsable API. If None,
            it will be enabled in debug mode. Defaults to None.

    Attributes:
        path (str): The URL path where the JSON-RPC application is accessible.
        base_url (str | None): The base URL of the JSON-RPC application.
        version (str): The version of the JSON-RPC application.
        jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): The JSON-RPC site instance.
        jsonrpc_site_api (type[flask_jsonrpc.views.JSONRPCView]): The JSON-RPC site API class.
        jsonrpc_apps (set[flask_jsonrpc.app.JSONRPC | flask_jsonrpc.blueprints.JSONRPCBlueprint]): The set of
            registered JSON-RPC applications.
        jsonrpc_browse (flask_jsonrpc.contrib.browse.JSONRPCBrowse | None): The JSON-RPC browse application instance.
        enable_web_browsable_api (bool | None): Whether to enable the web browsable API. If None,
            it will be enabled in debug mode. Defaults to None.

    Examples:
        >>> from flask import Flask
        >>> from flask_jsonrpc import JSONRPC
        >>>
        >>> app = Flask(__name__)
        >>> jsonrpc = JSONRPC(app, path='/api', version='1.0.0')
        >>>
        >>> # Disable automatic validation for typechecking limitations with doctests
        >>> # We always recommend to use validation in real applications
        >>> @jsonrpc.method('my_method', validate=False)
        ... def my_method(param1: int) -> str:
        ...     return str(param1)
        >>>
        >>> if __name__ == '__main__':
        ...     app.run()
    """

    def __init__(
        self: Self,
        app: Flask | None = None,
        path: str = '/api',
        version: str = '1.0.0',
        jsonrpc_site: type[JSONRPCSite] = default_jsonrpc_site,
        jsonrpc_site_api: type[JSONRPCView] = default_jsonrpc_site_api,
        enable_web_browsable_api: bool | None = None,
    ) -> None:
        self.path = path
        self.base_url: str | None = None
        self.version = version
        self.jsonrpc_site = jsonrpc_site(version=version)
        self.jsonrpc_site_api = jsonrpc_site_api
        self.jsonrpc_apps: set[JSONRPC | JSONRPCBlueprint] = set()
        self.jsonrpc_browse: JSONRPCBrowse | None = None
        self.enable_web_browsable_api = enable_web_browsable_api
        if app:
            self.init_app(app)

    def _make_jsonrpc_browse_url(self: Self, path: str) -> str:
        """Create the JSON-RPC browse URL based on the given path.

        Args:
            path (str): The base path for the JSON-RPC application.

        Returns:
            str: The URL for the JSON-RPC browse interface.
        """
        return ''.join([path.rstrip('/'), '/browse'])

    def get_jsonrpc_site(self: Self) -> JSONRPCSite:
        """Get the JSON-RPC site.

        Returns:
            flask_jsonrpc.site.JSONRPCSite: The JSON-RPC site instance.
        """
        return self.jsonrpc_site

    def get_jsonrpc_site_api(self: Self) -> type[JSONRPCView]:
        """Get the JSON-RPC site API.

        Returns:
            flask_jsonrpc.views.JSONRPCView: The JSON-RPC site API type.
        """
        return self.jsonrpc_site_api

    def init_app(self: Self, app: Flask) -> None:
        """Initialize the JSON-RPC application with the given Flask app.

        Initializes the JSON-RPC application by configuring it with the provided Flask
        application instance. This includes setting up the URL rules, logging, and
        web browsable API if enabled.

        If the web browsable API is enabled, it will also initialize the browse interface.

        Args:
            app (flask.Flask): The Flask application instance.

        Examples:
            >>> from flask import Flask
            >>> from flask_jsonrpc import JSONRPC
            >>>
            >>> app = Flask(__name__)
            >>> jsonrpc = JSONRPC(path='/api', version='1.0.0')
            >>> jsonrpc.init_app(app)
        """
        for setting, value in app.config.items():
            if settings.IS_ENV_KEY(setting):
                setattr(settings, settings.ENV_TO_CONFIG(setting), value)

        http_host = app.config.get('SERVER_NAME')
        app_root = app.config['APPLICATION_ROOT']
        url_scheme = app.config['PREFERRED_URL_SCHEME']
        url = urlsplit(self.path)

        if self.logger.level == logging.NOTSET:
            self.logger.setLevel(app.logger.level)

        if not has_level_handler(self.logger):
            for handler in app.logger.handlers:
                self.logger.addHandler(handler)

        self.path = f'{app_root.rstrip("/")}{url.path}'
        self.base_url = (
            f'{url.scheme or url_scheme}://{url.netloc or http_host}/{self.path.lstrip("/")}' if http_host else None
        )

        self.get_jsonrpc_site().set_path(self.path)
        self.get_jsonrpc_site().set_base_url(self.base_url)

        app.add_url_rule(
            self.path,
            view_func=self.get_jsonrpc_site_api().as_view(
                urn('app', app.name, self.path), jsonrpc_site=self.get_jsonrpc_site()
            ),
        )

        if self.enable_web_browsable_api is True or (self.enable_web_browsable_api is None and app.config['DEBUG']):
            self.init_browse_app(app)

    def register(
        self: Self,
        view_func: t.Callable[..., t.Any],
        name: str | None = None,
        **options: t.Any,  # noqa: ANN401
    ) -> None:
        """Register a view function as a JSON-RPC method.

        Args:
            view_func (typing.Callable[..., typing.Any]): The view function to register.
            name (str | None): The name of the JSON-RPC method. If None, the function's
                __name__ attribute will be used.
            **options (typing.Any): Additional options for the JSON-RPC method.

        Examples:
            >>> from flask import Flask
            >>> from flask_jsonrpc import JSONRPC
            >>>
            >>> app = Flask(__name__)
            >>> jsonrpc = JSONRPC(app, path='/api', version='1.0.0')
            >>>
            ... def my_method(param1: int) -> str:
            ...     return str(param1)
            >>>
            >>> # Disable automatic validation for typechecking limitations with doctests
            >>> # We always recommend to use validation in real applications
            >>> jsonrpc.register(my_method, name='my_method', validate=False)
        """
        self.register_view_function(view_func, name, **options)

    def register_blueprint(
        self: Self,
        app: Flask,
        jsonrpc_app: JSONRPCBlueprint,
        url_prefix: str | None = None,
        enable_web_browsable_api: bool | None = None,
    ) -> None:
        """Register a JSON-RPC blueprint with the given Flask app.

        If the web browsable API is enabled, it will also register the browse interface
        for the blueprint.

        Args:
            app (flask.Flask): The Flask application instance.
            jsonrpc_app (flask_jsonrpc.blueprints.JSONRPCBlueprint): The JSON-RPC blueprint to register.
            url_prefix (str | None): The URL prefix for the JSON-RPC blueprint. If None,
                the blueprint's path will be used.
            enable_web_browsable_api (bool | None): Whether to enable the web browsable API. If None,
                it will be enabled in debug mode. Defaults to None.

        Examples:
            >>> from flask import Flask
            >>> from flask_jsonrpc import JSONRPC, JSONRPCBlueprint
            >>>
            >>> app = Flask(__name__)
            >>> jsonrpc = JSONRPC(app, path='/api', version='1.0.0')
            >>>
            >>> my_blueprint = JSONRPCBlueprint('my_blueprint', __name__)
            >>>
            >>> # Disable automatic validation for typechecking limitations with doctests
            >>> # We always recommend to use validation in real applications
            >>> @my_blueprint.method('my_blueprint.my_method', validate=False)
            ... def my_method(param1: int) -> str:
            ...     return str(param1)
            >>>
            >>> jsonrpc.register_blueprint(app, my_blueprint, url_prefix='/my-blueprint')
        """
        path = ''.join([self.path, '/', url_prefix.lstrip('/')]) if url_prefix else self.path
        path_url = urlsplit(path)

        url = urlsplit(self.base_url or path)
        base_url = f'{url.scheme}://{url.netloc}/{url.path.lstrip("/")}' if self.base_url else None

        jsonrpc_app.get_jsonrpc_site().set_path(path_url.path)
        jsonrpc_app.get_jsonrpc_site().set_base_url(base_url)

        app.add_url_rule(
            path,
            view_func=jsonrpc_app.get_jsonrpc_site_api().as_view(
                urn('blueprint', app.name, jsonrpc_app.name, path), jsonrpc_site=jsonrpc_app.get_jsonrpc_site()
            ),
        )

        self.jsonrpc_apps.add(jsonrpc_app)

        if enable_web_browsable_api is True or (enable_web_browsable_api is None and app.config['DEBUG']):
            self.register_browse(jsonrpc_app)

    def init_browse_app(self: Self, app: Flask, path: str | None = None, base_url: str | None = None) -> None:
        """Initialize the JSON-RPC browse application.

        Args:
            app (flask.Flask): The Flask application instance.
            path (str | None): The URL path for the JSON-RPC browse application. If None,
                the browse URL will be generated based on the JSON-RPC application's path.
            base_url (str | None): The base URL for the JSON-RPC browse application. If None,
                the base URL will be generated based on the JSON-RPC application's base URL.

        Examples:
            >>> from flask import Flask
            >>> from flask_jsonrpc import JSONRPC
            >>>
            >>> app = Flask(__name__)
            >>> jsonrpc = JSONRPC(app, path='/api', version='1.0.0')
            >>> jsonrpc.init_browse_app(
            ...     app, path='/api/browse', base_url='http://localhost/api'
            ... )
        """
        browse_url = self._make_jsonrpc_browse_url(path or self.path)
        self.jsonrpc_browse = JSONRPCBrowse(app, url_prefix=browse_url, base_url=base_url or self.base_url)
        self.jsonrpc_browse.register_jsonrpc_site(self.get_jsonrpc_site())

    def register_browse(self: Self, jsonrpc_app: JSONRPC | JSONRPCBlueprint) -> None:
        """Register the JSON-RPC browse application for a given JSON-RPC app.

        Args:
            jsonrpc_app (flask_jsonrpc.app.JSONRPC | flask_jsonrpc.blueprints.JSONRPCBlueprint):
                The JSON-RPC application or blueprint to register the browse interface for.

        Raises:
            RuntimeError: If the JSON-RPC browse application has not been initialized.

        Examples:
            >>> from flask import Flask
            >>> from flask_jsonrpc import JSONRPC, JSONRPCBlueprint
            >>>
            >>> app = Flask(__name__)
            >>> jsonrpc = JSONRPC(app, path='/api', version='1.0.0')
            >>> my_blueprint = JSONRPCBlueprint('my_blueprint', __name__)
            >>>
            >>> # Disable automatic validation for typechecking limitations with doctests
            >>> # We always recommend to use validation in real applications
            >>> @my_blueprint.method('my_blueprint.my_method', validate=False)
            ... def my_method(param1: int) -> str:
            ...     return str(param1)
            >>>
            >>> jsonrpc.register_blueprint(app, my_blueprint, url_prefix='/my-blueprint')
            >>> jsonrpc.init_browse_app(app)
            >>> jsonrpc.register_browse(my_blueprint)
        """
        if not self.jsonrpc_browse:
            raise RuntimeError(
                'you need to init the Browse app before register the Site, see JSONRPC.init_browse_app(...)'
            )
        self.jsonrpc_browse.register_jsonrpc_site(jsonrpc_app.get_jsonrpc_site())
