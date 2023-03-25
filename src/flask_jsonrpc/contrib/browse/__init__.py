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
from itertools import chain

from flask import Blueprint, jsonify, request, render_template

from flask_jsonrpc.helpers import urn

if t.TYPE_CHECKING:
    from flask import Flask
    from flask import typing as ft

    from flask_jsonrpc.site import JSONRPCSite, ServiceProcedureDescribe


class JSONRPCBrowse:
    def __init__(
        self, app: t.Optional['Flask'] = None, url_prefix: str = '/api/browse', base_url: t.Optional[str] = None
    ) -> None:
        self.app = app
        self.url_prefix = url_prefix
        self.base_url = base_url
        self.jsonrpc_sites: t.Set['JSONRPCSite'] = set()
        if app:
            self.init_app(app)

    def _service_desc_procedures(self) -> t.Dict[str, 'ServiceProcedureDescribe']:
        service_procs = list(chain(*[site.describe()['procs'] for site in self.jsonrpc_sites]))
        return {proc['name']: proc for proc in service_procs}

    def init_app(self, app: 'Flask') -> None:
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

    def register_jsonrpc_site(self, jsonrpc_site: 'JSONRPCSite') -> None:
        self.jsonrpc_sites.add(jsonrpc_site)

    def vf_index(self) -> str:
        server_urls = {}
        service_describes = [site.describe() for site in self.jsonrpc_sites]
        for service_describe in service_describes:
            server_urls.update(
                {
                    name: service_describe['servers'][0]['url']
                    for name in [proc['name'] for proc in service_describe['procs']]
                }
            )
        url_prefix = f"{request.script_root}{request.path.rstrip('/')}"
        return render_template('browse/index.html', url_prefix=url_prefix, server_urls=server_urls)

    def vf_json_packages(self) -> 'ft.ResponseReturnValue':
        service_procedures = self._service_desc_procedures()
        packages = sorted(service_procedures.values(), key=lambda proc: proc['name'])
        packages_tree: t.Dict[str, t.Any] = {}
        for package in packages:
            package_name = package['name'].split('.')[0]
            packages_tree.setdefault(package_name, []).append(package)
        return jsonify(packages_tree)

    def vf_json_method(self, method_name: str) -> 'ft.ResponseReturnValue':
        service_procedures = self._service_desc_procedures()
        if method_name not in service_procedures:
            return jsonify({'message': 'Not found'}), 404
        return jsonify(service_procedures[method_name])

    def vf_partials_dashboard(self) -> str:
        return render_template('browse/partials/dashboard.html')

    def vf_partials_response_object(self) -> str:
        return render_template('browse/partials/response_object.html')
