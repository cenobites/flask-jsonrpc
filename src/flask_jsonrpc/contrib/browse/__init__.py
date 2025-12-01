# Copyright (c) 2012-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
from collections import ChainMap

# Added in version 3.11.
from typing_extensions import Self

from flask import Blueprint, request, render_template

from jinja2 import BaseLoader, TemplateNotFound

from flask_jsonrpc.conf import settings
from flask_jsonrpc.helpers import Node, urn
from flask_jsonrpc.encoders import jsonify, serializable

if t.TYPE_CHECKING:
    from flask import Flask, typing as ft

    from jinja2.environment import Environment

    from flask_jsonrpc.site import JSONRPCSite
    from flask_jsonrpc.typing import Method


def build_package_tree(service_methods: dict[str, Method]) -> dict[str, t.Any]:
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
    def __init__(self, app_jinja_loader: BaseLoader, browse_jinja_loader: BaseLoader) -> None:
        self.app_jinja_loader = app_jinja_loader
        self.browse_jinja_loader = browse_jinja_loader

    def get_source(
        self, environment: Environment, template: str
    ) -> tuple[str, str | None, t.Callable[[], bool] | None]:
        try:
            return self.app_jinja_loader.get_source(environment, template)
        except TemplateNotFound:
            return self.browse_jinja_loader.get_source(environment, template)


class JSONRPCBrowse:
    def __init__(
        self: Self, app: Flask | None = None, url_prefix: str = '/api/browse', base_url: str | None = None
    ) -> None:
        self.app = app
        self.url_prefix = url_prefix
        self.base_url = base_url
        self.jsonrpc_sites: set[JSONRPCSite] = set()
        if app:
            self.init_app(app)

    def _service_methods_desc(self: Self) -> dict[str, Method]:
        return dict(ChainMap(*[site.describe().methods for site in self.jsonrpc_sites]))

    def init_app(self: Self, app: Flask) -> None:
        name = urn('browse', app.name, self.url_prefix)
        browse = Blueprint(name, __name__, template_folder='templates', static_folder='static')
        browse.jinja_loader = JSONRPCBrowseTemplateLoader(
            app_jinja_loader=app.jinja_loader,  # type: ignore
            browse_jinja_loader=browse.jinja_loader,  # type: ignore
        )
        browse.add_url_rule('/', view_func=self.vf_index)
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

    def register_jsonrpc_site(self: Self, jsonrpc_site: JSONRPCSite) -> None:
        self.jsonrpc_sites.add(jsonrpc_site)

    def get_browse_title(self: Self) -> str:
        return t.cast(str, settings.BROWSE_TITLE)

    def get_browse_title_url(self: Self) -> str:
        return t.cast(str, settings.BROWSE_TITLE_URL)

    def get_browse_subtitle(self: Self) -> str:
        return t.cast(str, settings.BROWSE_SUBTITLE)

    def get_browse_description(self: Self) -> str:
        return t.cast(str, settings.BROWSE_DESCRIPTION)

    def get_browse_fork_me_button_enabled(self: Self) -> bool:
        return t.cast(bool, settings.BROWSE_FORK_ME_BUTTON_ENABLED)

    def get_browse_media_css(self: Self) -> dict[str, list[str]]:
        return t.cast(dict[str, list[str]], settings.BROWSE_MEDIA_CSS)

    def get_browse_media_js(self: Self) -> list[str]:
        return t.cast(list[str], settings.BROWSE_MEDIA_JS)

    def get_browse_dashboard_menu_name(self: Self) -> str:
        return t.cast(str, settings.BROWSE_DASHBOARD_MENU_NAME)

    def get_browse_dashboard_template(self: Self) -> str:
        return t.cast(str, settings.BROWSE_DASHBOARD_TEMPLATE)

    def vf_index(self: Self) -> str:
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
            'browse_media_css': self.get_browse_media_css(),
            'browse_media_js': self.get_browse_media_js(),
        }
        return render_template('browse/index.html', **context)

    def vf_json_packages(self: Self) -> ft.ResponseReturnValue:
        service_methods = {
            name: method
            for name, method in self._service_methods_desc().items()
            # The rpc. prefix is a reserved method prefix for JSON-RPC 2.0
            # specification system extensions.
            if not name.startswith('rpc.')
        }
        return jsonify(build_package_tree(service_methods))

    def vf_json_method(self: Self, method_name: str) -> ft.ResponseReturnValue:
        service_procedures = self._service_methods_desc()
        if method_name not in service_procedures:
            return jsonify({'message': 'Not found'}), 404
        return jsonify({'name': method_name, **serializable(service_procedures[method_name])})

    def vf_partials_menu_tree(self: Self) -> str:
        return render_template('browse/partials/menu_tree.html')

    def vf_partials_dashboard(self: Self) -> str:
        return render_template(self.get_browse_dashboard_template())

    def vf_partials_field_describe(self: Self) -> str:
        return render_template('browse/partials/field_describe.html')

    def vf_partials_response_object(self: Self) -> str:
        return render_template('browse/partials/response_object.html')
