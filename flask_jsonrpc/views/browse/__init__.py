# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013, Cenobit Technologies, Inc. http://cenobit.es/
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
from flask import Blueprint, request, jsonify, render_template

from flask_jsonrpc.site import jsonrpc_site

mod = Blueprint('browse', __name__, static_folder='static', template_folder='templates')

@mod.route('/')
def index():
    url_prefix = request.path
    url_prefix = url_prefix if not url_prefix.endswith('/') else url_prefix[:-1]
    service_url = url_prefix.replace('/browse', '')
    return render_template('browse/index.html', service_url=service_url, url_prefix=url_prefix)

@mod.route('/packages.json')
def json_packages():
    jsonrpc_describe = jsonrpc_site.describe()
    packages = sorted(jsonrpc_describe['procs'], key=lambda proc: proc['name'])
    packages_tree = {}
    for package in packages:
        package_name = package['name'].split('.')[0]
        packages_tree.setdefault(package_name, []).append(package)
    return jsonify(packages_tree)

@mod.route('/<method_name>.json')
def json_method(method_name):
    jsonrpc_describe = jsonrpc_site.describe()
    method = [method for method in jsonrpc_describe['procs'] if method['name'] == method_name][0]
    return jsonify(method)

@mod.route('/partials/dashboard.html')
def partials_dashboard():
    return render_template('browse/partials/dashboard.html')

@mod.route('/partials/response_object.html')
def partials_response_object():
    return render_template('browse/partials/response_object.html')
