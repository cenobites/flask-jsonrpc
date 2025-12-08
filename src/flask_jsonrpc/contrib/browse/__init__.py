# Copyright (c) 2012-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
from functools import wraps
import contextlib
from collections import ChainMap

# Added in version 3.11.
from typing_extensions import Self

from flask import Flask, Blueprint, g, typing as ft, request, render_template

from jinja2 import BaseLoader, TemplateNotFound

from flask_jsonrpc.conf import settings
from flask_jsonrpc.helpers import Node, urn
from flask_jsonrpc.encoders import jsonify, serializable

if t.TYPE_CHECKING:
    from flask.wrappers import Request, Response

    from jinja2.environment import Environment

    from flask_jsonrpc.site import JSONRPCSite
    from flask_jsonrpc.typing import Method


def register_middleware(
    name: str,
) -> t.Callable[
    [t.Callable[[Request], t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]]],
    t.Callable[[Request], t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]],
]:
    """Register a browse middleware.

    If a middleware returns:
        - True: the middleware will be kept for after_request and teardown_request processing.
        - False: the middleware will be skipped for after_request and teardown_request processing.
        - A Response: the response will be returned immediately, skipping further processing.

    Args:
        name (str): The name of the middleware.

    Returns:
        typing.Callable: The middleware decorator.

    Examples:
        Inject a custom header into the response using a middleware:

        >>> import pytest
        >>> pytest.skip('The global context causes issues with testing.')
        >>>
        >>> from flask import Flask, Response
        >>> from flask_jsonrpc.contrib.browse import JSONRPCBrowse, register_middleware
        >>>
        >>> app = Flask(__name__)
        >>> browse = JSONRPCBrowse(app)
        >>>
        >>> @register_middleware('example_middleware')
        ... def example_middleware(request):
        ...     response = yield
        ...     response.headers['X-Example'] = 'Value'
        ...     yield response
        >>>
        >>> with app.test_client() as client:
        ...     response = client.get('/api/browse/')
        ...     assert response.headers.get('X-Example') == 'Value'
    """

    def decorator(
        fn: t.Callable[
            [Request], t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]
        ],
    ) -> t.Callable[
        [Request], t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]
    ]:
        @wraps(fn)
        def wrapper(
            request: Request,
        ) -> t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]:
            gen = fn(request)
            if not hasattr(gen, '__next__'):
                raise TypeError("middleware function must be a generator (must use 'yield')")
            return gen

        settings.BROWSE_MIDDLEWARE.append((name, wrapper))
        return wrapper

    return decorator


def _before_request_middleware() -> ft.ResponseReturnValue | None:
    """Execute before request middlewares.

    If a middleware returns:
        - True: the middleware will be kept for after_request and teardown_request processing.
        - False: the middleware will be skipped for after_request and teardown_request processing.
        - A Response: the response will be returned immediately, skipping further processing.

    Returns:
        flask.typing.ResponseReturnValue | None: The response if a middleware returns a response, otherwise None.

    Examples:
        >>> import pytest
        >>> pytest.skip('The global context causes issues with testing.')
        >>>
        >>> from flask import Flask, Response
        >>> from flask_jsonrpc.contrib.browse import JSONRPCBrowse, register_middleware
        >>>
        >>> app = Flask(__name__)
        >>> browse = JSONRPCBrowse(app)
        >>>
        >>> @register_middleware('example_middleware')
        ... def example_middleware(request):
        ...     # Perform some checks before processing the request
        ...     if not request.headers.get('X-Allowed'):
        ...         yield Response('Forbidden', status=403)
        ...     yield False  # Continue processing the request
        >>>
        >>> with app.test_client() as client:
        ...     response = client.get('/api/browse/')
        ...     assert response.status_code == 403
        ...
        ...     response = client.get('/api/browse/', headers={'X-Allowed': '1'})
        ...     assert response.status_code == 200
    """
    middlewares: list[
        tuple[
            str,
            t.Callable[
                [Request], t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]
            ],
        ]
    ] = settings.BROWSE_MIDDLEWARE
    g._jsonrpc_browse_mw = {}
    for name, middleware in middlewares:
        gen = middleware(request)
        rv = next(gen, None)
        if rv is False:
            continue
        if rv is True:
            g._jsonrpc_browse_mw[name] = gen
            continue
        if rv is not None:
            return rv
        g._jsonrpc_browse_mw[name] = gen
    return None


def _after_request_middleware(response: Response) -> ft.ResponseReturnValue:
    """Execute after request middlewares.

    If a middleware returns:
        - True: the middleware will be kept for teardown_request processing.
        - False: the middleware will be skipped for teardown_request processing.
        - A Response: the response will be returned immediately, skipping further processing.

    Args:
        response (flask.wrappers.Response): The response object.

    Returns:
        flask.typing.ResponseReturnValue: The modified response object.

    Examples:
        >>> import pytest
        >>> pytest.skip('The global context causes issues with testing.')
        >>>
        >>> from flask import Flask, Response
        >>> from flask_jsonrpc.contrib.browse import JSONRPCBrowse, register_middleware
        >>>
        >>> app = Flask(__name__)
        >>> browse = JSONRPCBrowse(app)
        >>>
        >>> @register_middleware('example_middleware')
        ... def example_middleware(request):
        ...     response = yield
        ...     response.headers['X-Example'] = 'Value'
        ...     yield response
        >>>
        >>> with app.test_client() as client:
        ...     response = client.get('/api/browse/#/')
        ...     assert response.headers.get('X-Example') == 'Value', response.headers
    """
    middlewares: list[
        tuple[
            str,
            t.Callable[
                [Request], t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]
            ],
        ]
    ] = settings.BROWSE_MIDDLEWARE
    gens = g.pop('_jsonrpc_browse_mw', {})
    for name, _ in reversed(middlewares):
        gen = gens.pop(name, None)
        if gen is None:
            continue
        gen.send(response)
        rv = next(gen, None)
        with contextlib.suppress(BaseException):
            gen.close()
        if rv is False:
            continue
        if rv is True:
            continue
        if rv is not None:
            g._jsonrpc_browse_mw = {}
            return t.cast(ft.ResponseReturnValue, rv)
    return response


def _teardown_request_middleware(exception: BaseException | None) -> None:
    """Execute teardown request middlewares.

    Args:
        exception (BaseException | None): The exception if any occurred during request processing.
    """
    gens = g.pop('_jsonrpc_browse_mw', {})
    for gen in gens.values():
        with contextlib.suppress(BaseException):
            gen.close()


def build_package_tree(service_methods: dict[str, Method]) -> dict[str, t.Any]:
    """Build a package tree from service methods.

    Args:
        service_methods (dict[str, flask_jsonrpc.typing.Method]): The service methods.

    Returns:
        dict[str, typing.Any]: The package tree as a dictionary.
    """
    package_tree = Node(name=None)
    for package, service_method in service_methods.items():
        default_package_name = package.split('.')[0]
        tags = service_method.tags or [default_package_name]
        nodes = [Node(name=tag) for tag in tags]
        nodes[-1].insert_item(serializable(service_method))
        current_node = package_tree
        for node in nodes:
            child = current_node.find_child(t.cast(str, node.name))
            if child is not None:
                current_node = child
                if len(node.items) > 0:
                    child.insert_item(node.items[0])
                continue
            current_node.add_child(node)
            current_node = node
    package_tree.clean()
    package_tree.sort()
    return package_tree.to_dict() if package_tree.children else {}


class JSONRPCBrowseTemplateLoader(BaseLoader):
    """Custom Jinja2 template loader that tries to load templates from the application first,
    then falls back to the browse templates.

    Args:
        app_jinja_loader (jinja2.BaseLoader): The application's Jinja2 template loader.
        browse_jinja_loader (jinja2.BaseLoader): The browse's Jinja2 template loader.

    Attributes:
        app_jinja_loader (jinja2.BaseLoader): The application's Jinja2 template loader.
        browse_jinja_loader (jinja2.BaseLoader): The browse's Jinja2 template loader.
    """

    def __init__(self, app_jinja_loader: BaseLoader, browse_jinja_loader: BaseLoader) -> None:
        self.app_jinja_loader = app_jinja_loader
        self.browse_jinja_loader = browse_jinja_loader

    def get_source(
        self, environment: Environment, template: str
    ) -> tuple[str, str | None, t.Callable[[], bool] | None]:
        """Get the source of a template.

        If the template is not found in the application loader, it tries to load it from the browse loader.

        Args:
            environment (jinja2.Environment): The Jinja2 environment.
            template (str): The name of the template.

        Returns:
            tuple[str, str | None, typing.Callable[[], bool] | None]: The template source
        """
        try:
            return self.app_jinja_loader.get_source(environment, template)
        except TemplateNotFound:
            return self.browse_jinja_loader.get_source(environment, template)


class JSONRPCBrowse:
    """JSON-RPC Browse extension for Flask applications.

    Args:
        app (Flask | None): The Flask application to initialize the extension with.
        url_prefix (str): The URL prefix for the browse interface.
        base_url (str | None): The base URL for the browse interface.

    Attributes:
        url_prefix (str): The URL prefix for the browse interface.
        base_url (str | None): The base URL for the browse interface.
        jsonrpc_sites (set[flask_jsonrpc.site.JSONRPCSite]): The set of registered JSON-RPC sites

    Examples:
        >>> from flask import Flask
        >>> from flask_jsonrpc import JSONRPCBlueprint
        >>> from flask_jsonrpc.contrib.browse import JSONRPCBrowse
        >>>
        >>> app = Flask(__name__)
        >>> jsonrpc = JSONRPCBlueprint('example', __name__)
        >>> browse = JSONRPCBrowse(app, url_prefix='/api/browse')
        >>> browse.register_jsonrpc_site(jsonrpc)
    """

    def __init__(
        self: Self, app: Flask | None = None, url_prefix: str = '/api/browse', base_url: str | None = None
    ) -> None:
        self.url_prefix = url_prefix
        self.base_url = base_url
        self.jsonrpc_sites: set[JSONRPCSite] = set()
        if app:
            self.init_app(app)

    def _service_methods_desc(self: Self) -> dict[str, Method]:
        """Get the service methods description from all registered JSON-RPC sites.

        Returns:
            dict[str, flask_jsonrpc.typing.Method]: The service methods description.
        """
        return dict(ChainMap(*[site.describe().methods for site in self.jsonrpc_sites]))

    def _base_template_context(self: Self) -> dict[str, t.Any]:
        """Get the base template context for rendering templates.

        Returns:
            dict[str, typing.Any]: The base template context.
        """
        server_urls: dict[str, str] = {}
        service_describes = [site.describe() for site in self.jsonrpc_sites]
        for service_describe in service_describes:
            server_urls.update(dict.fromkeys(service_describe.methods, service_describe.servers[0].url))
        url_prefix = f'{request.script_root}{request.path.rstrip("/")}'
        context = {
            'url_prefix': url_prefix,
            'server_urls': server_urls,
            'browse_title': self.get_browse_title(),
            'browse_title_url': self.get_browse_title_url(),
            'browse_subtitle': self.get_browse_subtitle(),
            'browse_description': self.get_browse_description(),
            'browse_fork_me_button_enabled': self.get_browse_fork_me_button_enabled(),
            'browse_dashboard_menu_name': self.get_browse_dashboard_menu_name(),
            'browse_login_template_enabled': self.get_browse_login_template() is not None,
            'browse_logout_template_enabled': self.get_browse_logout_template() is not None,
            'browse_media_css': self.get_browse_media_css(),
            'browse_media_js': self.get_browse_media_js(),
        }
        return context

    def init_app(self: Self, app: Flask) -> None:
        """Initialize the JSON-RPC Browse extension with a Flask application.

        Middlewares for before_request, after_request, and teardown_request are registered.

        Args:
            app (flask.Flask): The Flask application.

        Examples:
            >>> from flask import Flask
            >>> from flask_jsonrpc.contrib.browse import JSONRPCBrowse
            >>>
            >>> app = Flask(__name__)
            >>> browse = JSONRPCBrowse()
            >>> browse.init_app(app)
        """
        name = urn('browse', app.name, self.url_prefix)
        browse = Blueprint(name, __name__, template_folder='templates', static_folder='static')
        browse.jinja_loader = JSONRPCBrowseTemplateLoader(
            app_jinja_loader=app.jinja_loader,  # type: ignore
            browse_jinja_loader=browse.jinja_loader,  # type: ignore
        )
        browse.before_request(_before_request_middleware)
        browse.after_request(_after_request_middleware)
        browse.teardown_request(_teardown_request_middleware)
        browse.add_url_rule('/', view_func=self.vf_index)
        browse.add_url_rule('/login', view_func=self.vf_login)
        browse.add_url_rule('/logout', view_func=self.vf_logout)
        browse.add_url_rule('/packages.json', view_func=self.vf_json_packages)
        browse.add_url_rule('/<method_name>.json', view_func=self.vf_json_method)
        browse.add_url_rule('/partials/menu_tree.html', view_func=self.vf_partials_menu_tree)
        browse.add_url_rule('/partials/dashboard.html', view_func=self.vf_partials_dashboard)
        browse.add_url_rule('/partials/field_describe.html', view_func=self.vf_partials_field_describe)
        browse.add_url_rule('/partials/response_object.html', view_func=self.vf_partials_response_object)

        app.register_blueprint(browse, url_prefix=self.url_prefix)
        app.add_url_rule(
            f'{self.url_prefix}/static/<path:filename>', 'urn:browse.static', view_func=app.send_static_file
        )
        app.teardown_appcontext(_teardown_request_middleware)

    def register_jsonrpc_site(self: Self, jsonrpc_site: JSONRPCSite) -> None:
        """Register a JSON-RPC site with the browse extension.

        Args:
            jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): The JSON-RPC site to register.
        """
        self.jsonrpc_sites.add(jsonrpc_site)

    def get_browse_title(self: Self) -> str:
        """Get the browse title.

        Register a custom title by setting BROWSE_TITLE in your settings
        or overriding this method.

        Returns:
            str: The browse title.
        """
        return t.cast(str, settings.BROWSE_TITLE)

    def get_browse_title_url(self: Self) -> str:
        """Get the browse title URL.

        Register a custom title URL by setting BROWSE_TITLE_URL in your settings
        or overriding this method.

        Returns:
            str: The browse title URL.
        """
        return t.cast(str, settings.BROWSE_TITLE_URL)

    def get_browse_subtitle(self: Self) -> str:
        """Get the browse subtitle.

        Register a custom subtitle by setting BROWSE_SUBTITLE in your settings
        or overriding this method.

        Returns:
            str: The browse subtitle.
        """
        return t.cast(str, settings.BROWSE_SUBTITLE)

    def get_browse_description(self: Self) -> str:
        """Get the browse description.

        Register a custom description by setting BROWSE_DESCRIPTION in your settings
        or overriding this method.

        Returns:
            str: The browse description.
        """
        return t.cast(str, settings.BROWSE_DESCRIPTION)

    def get_browse_fork_me_button_enabled(self: Self) -> bool:
        """Check if the "Fork me on GitHub" button is enabled.

        Register the button state by setting BROWSE_FORK_ME_BUTTON_ENABLED in your settings
        or overriding this method.

        Returns:
            bool: True if the "Fork me on GitHub" button is enabled, False otherwise.
        """
        return t.cast(bool, settings.BROWSE_FORK_ME_BUTTON_ENABLED)

    def get_browse_media_css(self: Self) -> dict[str, list[str]]:
        """Get the browse media CSS files.

        Register custom CSS files by setting BROWSE_MEDIA_CSS in your settings
        or overriding this method.

        Returns:
            dict[str, list[str]]: The browse media CSS files.
        """
        return t.cast(dict[str, list[str]], settings.BROWSE_MEDIA_CSS)

    def get_browse_media_js(self: Self) -> list[str]:
        """Get the browse media JS files.

        Register custom JS files by setting BROWSE_MEDIA_JS in your settings
        or overriding this method.

        Returns:
            list[str]: The browse media JS files.
        """
        return t.cast(list[str], settings.BROWSE_MEDIA_JS)

    def get_browse_dashboard_menu_name(self: Self) -> str:
        """Get the browse dashboard menu name.

        Register a custom dashboard menu name by setting BROWSE_DASHBOARD_MENU_NAME in your settings
        or overriding this method.

        Returns:
            str: The browse dashboard menu name.
        """
        return t.cast(str, settings.BROWSE_DASHBOARD_MENU_NAME)

    def get_browse_dashboard_partial_template(self: Self) -> str:
        """Get the browse dashboard partial template.

        Register a custom dashboard partial template by setting BROWSE_DASHBOARD_PARTIAL_TEMPLATE in your settings
        or overriding this method.

        Returns:
            str: The browse dashboard partial template.
        """
        return t.cast(str, settings.BROWSE_DASHBOARD_PARTIAL_TEMPLATE)

    def get_browse_login_template(self: Self) -> str | None:
        """Get the browse login template.

        Register a custom login template by setting BROWSE_LOGIN_TEMPLATE in your settings
        or overriding this method.

        Returns:
            str | None: The browse login template or None if not configured.
        """
        if settings.BROWSE_LOGIN_TEMPLATE is None:
            return None
        return t.cast(str, settings.BROWSE_LOGIN_TEMPLATE)

    def get_browse_logout_template(self: Self) -> str | None:
        """Get the browse logout template.

        Register a custom logout template by setting BROWSE_LOGOUT_TEMPLATE in your settings
        or overriding this method.

        Returns:
            str | None: The browse logout template or None if not configured.
        """
        if settings.BROWSE_LOGOUT_TEMPLATE is None:
            return None
        return t.cast(str, settings.BROWSE_LOGOUT_TEMPLATE)

    def vf_index(self: Self) -> str:
        """Render the index page.

        Returns:
            str: The rendered index page.
        """
        return render_template('browse/index.html', **self._base_template_context())

    def vf_login(self: Self) -> str | tuple[str, int]:
        """Render the login page.

        Returns:
            str | tuple[str, int]: The rendered login page or an error message with status code if not configured.
        """
        login_template = self.get_browse_login_template()
        if login_template is None:
            return (
                'Login not configured. To configure, set BROWSE_LOGIN_TEMPLATE '
                'in your settings or override get_browse_login_template().',
                404,
            )
        return render_template(login_template, **self._base_template_context())

    def vf_logout(self: Self) -> str | tuple[str, int]:
        """Render the logout page.

        Returns:
            str | tuple[str, int]: The rendered logout page or an error message with status code if not configured.
        """
        logout_template = self.get_browse_logout_template()
        if logout_template is None:
            return (
                'Logout not configured. To configure, set BROWSE_LOGOUT_TEMPLATE '
                'in your settings or override get_browse_logout_template().',
                404,
            )
        return render_template(logout_template, **self._base_template_context())

    def vf_json_packages(self: Self) -> ft.ResponseReturnValue:
        """Get the JSON representation of the package tree.

        Ignores methods starting with 'rpc.' as they are reserved for JSON-RPC 2.0 specification system extensions.

        Returns:
            flask.typing.ResponseReturnValue: The JSON representation of the package tree.
        """
        service_methods = {
            name: method
            for name, method in self._service_methods_desc().items()
            # The rpc. prefix is a reserved method prefix for JSON-RPC 2.0
            # specification system extensions.
            if not name.startswith('rpc.')
        }
        return jsonify(build_package_tree(service_methods))

    def vf_json_method(self: Self, method_name: str) -> ft.ResponseReturnValue:
        """Get the JSON representation of a specific method.

        Args:
            method_name (str): The name of the method.

        Returns:
            flask.typing.ResponseReturnValue: The JSON representation of the method or a 404 error if not found.
        """
        service_procedures = self._service_methods_desc()
        if method_name not in service_procedures:
            return jsonify({'message': 'Not found'}), 404
        return jsonify({'name': method_name, **serializable(service_procedures[method_name])})

    def vf_partials_menu_tree(self: Self) -> str:
        """Render the menu tree partial template.

        Returns:
            str: The rendered menu tree partial template.
        """
        return render_template('browse/partials/menu_tree.html')

    def vf_partials_dashboard(self: Self) -> str:
        """Render the dashboard partial template.

        Returns:
            str: The rendered dashboard partial template.
        """
        return render_template(self.get_browse_dashboard_partial_template())

    def vf_partials_field_describe(self: Self) -> str:
        """Render the field describe partial template.

        Returns:
            str: The rendered field describe partial template.
        """
        return render_template('browse/partials/field_describe.html')

    def vf_partials_response_object(self: Self) -> str:
        """Render the response object partial template.

        Returns:
            str: The rendered response object partial template.
        """
        return render_template('browse/partials/response_object.html')
