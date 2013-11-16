# -*- coding: utf-8 -*-
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
