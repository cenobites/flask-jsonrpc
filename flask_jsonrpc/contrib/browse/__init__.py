# -*- coding: utf-8 -*-
# Copyright (c) 2012-2020, Cenobit Technologies, Inc. http://cenobit.es/
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
from typing import TYPE_CHECKING, Any, Dict

from flask import Blueprint, jsonify, request, render_template

if TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite


def create_browse(name: str, jsonrpc_site: 'JSONRPCSite') -> Blueprint:
    browse = Blueprint(name, __name__, template_folder='templates', static_folder='static')

    # pylint: disable=W0612
    @browse.route('/')
    def index() -> str:
        url_prefix = request.script_root + request.path
        url_prefix = url_prefix.rstrip('/')
        service_url = url_prefix.replace('/browse', '')
        return render_template('browse/index.html', service_url=service_url, url_prefix=url_prefix)

    # pylint: disable=W0612
    @browse.route('/packages.json')
    def json_packages() -> Any:
        jsonrpc_describe = jsonrpc_site.describe()
        packages = sorted(jsonrpc_describe['procs'], key=lambda proc: proc['name'])
        packages_tree: Dict[str, Any] = {}
        for package in packages:
            package_name = package['name'].split('.')[0]
            packages_tree.setdefault(package_name, []).append(package)
        return jsonify(packages_tree)

    # pylint: disable=W0612
    @browse.route('/<method_name>.json')
    def json_method(method_name: str) -> Any:
        jsonrpc_describe = jsonrpc_site.describe()
        method = [method for method in jsonrpc_describe['procs'] if method['name'] == method_name][0]
        return jsonify(method)

    # pylint: disable=W0612
    @browse.route('/partials/dashboard.html')
    def partials_dashboard() -> str:
        return render_template('browse/partials/dashboard.html')

    # pylint: disable=W0612
    @browse.route('/partials/response_object.html')
    def partials_response_object() -> str:
        return render_template('browse/partials/response_object.html')

    return browse
