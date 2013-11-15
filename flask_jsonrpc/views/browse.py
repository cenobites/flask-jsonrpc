# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, render_template

from flask_jsonrpc.site import jsonrpc_site

mod = Blueprint('browse', __name__)
jsonrpc_describe = jsonrpc_site.describe()

@mod.route('/')
def index():
    return render_template('browse/index.html')

@mod.route('browse/packages.json')
def json_packages():
    packages = sorted(jsonrpc_describe['procs'], key=lambda proc: proc['name'])
    packages_tree = {}
    for package in packages:
        package_name = package['name'].split('.')[0]
        packages_tree.setdefault(package_name, []).append(package)
    return jsonify(packages_tree)

@mod.route('browse/<method_name>.json')
def json_method(method_name):
    method = [method for method in jsonrpc_describe['procs'] if method['name'] == method_name][0]
    return jsonify(method)

@mod.route('browse/partials/dashboard.html')
def partials_dashboard():
    return render_template('browse/partials/dashboard.html')

@mod.route('browse/partials/response_object.html')
def partials_response_object():
    return render_template('browse/partials/response_object.html')
