# -*- coding: utf-8 -*-
# Copyright (c) 2020-2020, Cenobit Technologies, Inc. http://cenobit.es/
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
from flask import Flask

from flask_jsonrpc import JSONRPC, JSONRPCBlueprint


def test_browse_create():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc.method('app.fn2')
    def fn1(s: str) -> str:
        return 'Foo {0}'.format(s)

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200

        rv = client.get('/api/browse')
        assert rv.status_code == 308

        rv = client.get('/api/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/packages.json')
        assert rv.json == {
            'app': [
                {
                    'name': 'app.fn2',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                }
            ]
        }
        assert rv.status_code == 200

        rv = client.get('/api/browse/app.fn2.json')
        assert rv.json == {
            'name': 'app.fn2',
            'params': [{'name': 's', 'type': 'String'}],
            'return': {'type': 'String'},
            'summary': None,
        }
        assert rv.status_code == 200

        rv = client.get('/api/browse/partials/dashboard.html')
        assert b'Welcome to web browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/partials/response_object.html')
        assert b'module_dialog.html' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200


def test_browse_create_without_register_app():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc = JSONRPC(service_url='/api', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc.method('app.fn2')
    def fn1(s: str) -> str:
        return 'Foo {0}'.format(s)

    jsonrpc.init_app(app)

    with app.test_client() as client:
        rv = client.get('/api/browse/packages.json')
        assert rv.json == {
            'app': [
                {
                    'name': 'app.fn2',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                }
            ]
        }
        assert rv.status_code == 200

        rv = client.get('/api/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200


def test_browse_create_multiple_jsonrpc_versions():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc_v1 = JSONRPC(app, '/api/v1', enable_web_browsable_api=True)
    jsonrpc_v2 = JSONRPC(app, '/api/v2', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc_v1.method('app.fn2')
    def fn1_v1(s: str) -> str:
        return 'v1: Foo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc_v1.method('app.fn3')
    def fn3(s: str) -> str:
        return 'Poo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc_v2.method('app.fn2')
    def fn1_v2(s: str) -> str:
        return 'v2: Foo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc_v2.method('app.fn1')
    def fn2(s: str) -> str:
        return 'Bar {0}'.format(s)

    with app.test_client() as client:
        rv = client.get('/api/v1/browse/packages.json')
        assert rv.json == {
            'app': [
                {
                    'name': 'app.fn2',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'app.fn3',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
            ]
        }
        assert rv.status_code == 200

        rv = client.get('/api/v1/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/v1/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/v2/browse/packages.json')
        assert rv.json == {
            'app': [
                {
                    'name': 'app.fn1',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'app.fn2',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
            ]
        }
        assert rv.status_code == 200

        rv = client.get('/api/v2/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/v2/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200


def test_browse_create_modular_apps():
    jsonrpc_api_1 = JSONRPCBlueprint('jsonrpc_api_1', __name__)

    # pylint: disable=W0612
    @jsonrpc_api_1.method('blue1.fn2')
    def fn1_b1(s: str) -> str:
        return 'b1: Foo {0}'.format(s)

    jsonrpc_api_2 = JSONRPCBlueprint('jsonrpc_api_2', __name__)

    # pylint: disable=W0612
    @jsonrpc_api_2.method('blue2.fn2')
    def fn1_b2(s: str) -> str:
        return 'b2: Foo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc_api_2.method('blue2.fn1')
    def fn2_b2(s: str) -> str:
        return 'b2: Bar {0}'.format(s)

    jsonrpc_api_3 = JSONRPCBlueprint('jsonrpc_api_3', __name__)

    # pylint: disable=W0612
    @jsonrpc_api_3.method('blue3.fn2')
    def fn1_b3(s: str) -> str:
        return 'b3: Foo {0}'.format(s)

    app = Flask(__name__, instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_1, url_prefix='/b1', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_2, url_prefix='/b2', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_3, url_prefix='/b3')

    with app.test_client() as client:
        rv = client.get('/api/b1/browse/packages.json')
        assert rv.json == {
            'blue1': [
                {
                    'name': 'blue1.fn2',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                }
            ]
        }
        assert rv.status_code == 200

        rv = client.get('/api/b1/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/b1/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/b2/browse/packages.json')
        assert rv.json == {
            'blue2': [
                {
                    'name': 'blue2.fn1',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
                {
                    'name': 'blue2.fn2',
                    'params': [{'name': 's', 'type': 'String'}],
                    'return': {'type': 'String'},
                    'summary': None,
                },
            ]
        }
        assert rv.status_code == 200

        rv = client.get('/api/b2/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/b2/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/b3/browse/packages.json')
        assert rv.status_code == 404
