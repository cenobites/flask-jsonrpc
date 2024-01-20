# Copyright (c) 2012-2022, Cenobit Technologies, Inc. http://cenobit.es/
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
from collections import ChainMap

from flask import Blueprint, jsonify, request, render_template

from flask_jsonrpc.helpers import urn

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if t.TYPE_CHECKING:
    from flask import Flask, typing as ft

    from flask_jsonrpc.site import JSONRPCSite
    from flask_jsonrpc.typing import ServiceMethodDescribe


class JSONRPCBrowse:
    def __init__(
        self: Self, app: t.Optional['Flask'] = None, url_prefix: str = '/api/browse', base_url: t.Optional[str] = None
    ) -> None:
        self.app = app
        self.url_prefix = url_prefix
        self.base_url = base_url
        self.jsonrpc_sites: t.Set['JSONRPCSite'] = set()
        if app:
            self.init_app(app)

    def _service_methods_desc(self: Self) -> t.Dict[str, 'ServiceMethodDescribe']:
        return dict(ChainMap(*[site.describe()['methods'] for site in self.jsonrpc_sites]))

    def init_app(self: Self, app: 'Flask') -> None:
        name = urn('browse', app.name, self.url_prefix)
        browse = Blueprint(name, __name__, template_folder='templates', static_folder='static')
        browse.add_url_rule('/', view_func=self.vf_index)
        browse.add_url_rule('/packages.json', view_func=self.vf_json_packages)
        browse.add_url_rule('/<method_name>.json', view_func=self.vf_json_method)
        browse.add_url_rule('/partials/dashboard.html', view_func=self.vf_partials_dashboard)
        browse.add_url_rule('/partials/response_object.html', view_func=self.vf_partials_response_object)

        app.register_blueprint(browse, url_prefix=self.url_prefix)
        app.add_url_rule(
            f'{self.url_prefix}/static/<path:filename>', 'urn:browse.static', view_func=app.send_static_file
        )

    def register_jsonrpc_site(self: Self, jsonrpc_site: 'JSONRPCSite') -> None:
        self.jsonrpc_sites.add(jsonrpc_site)

    def vf_index(self: Self) -> str:
        server_urls: t.Dict[str, str] = {}
        service_describes = [site.describe() for site in self.jsonrpc_sites]
        for service_describe in service_describes:
            server_urls.update({name: service_describe['servers'][0]['url'] for name in service_describe['methods']})
        url_prefix = f"{request.script_root}{request.path.rstrip('/')}"
        return render_template('browse/index.html', url_prefix=url_prefix, server_urls=server_urls)

    def vf_json_packages(self: Self) -> 'ft.ResponseReturnValue':
        service_methods = self._service_methods_desc()
        packages = sorted(service_methods.keys())
        packages_tree: t.Dict[str, t.List[t.Dict[str, t.Any]]] = {}
        for package in packages:
            package_name = package.split('.')[0]
            packages_tree.setdefault(package_name, []).append({'name': package, **service_methods[package]})
        return jsonify(packages_tree)

    def vf_json_method(self: Self, method_name: str) -> 'ft.ResponseReturnValue':
        service_procedures = self._service_methods_desc()
        if method_name not in service_procedures:
            return jsonify({'message': 'Not found'}), 404
        return jsonify({'name': method_name, **service_procedures[method_name]})

    def vf_partials_dashboard(self: Self) -> str:
        return render_template('browse/partials/dashboard.html')

    def vf_partials_response_object(self: Self) -> str:
        return render_template('browse/partials/response_object.html')
