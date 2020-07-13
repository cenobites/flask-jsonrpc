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
from typing import Tuple

from flask import Flask

import pytest

from flask_jsonrpc import JSONRPC, JSONRPCBlueprint


def test_app_create():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc.method('App.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    # pylint: disable=W0612
    @jsonrpc.method('app.fn0')
    def fn0():
        pass

    # pylint: disable=W0612
    @jsonrpc.method('app.fn1')
    def fn1() -> str:
        return 'Bar'

    # pylint: disable=W0612
    @jsonrpc.method('app.fn2')
    def fn2(s: str) -> str:
        return 'Foo {0}'.format(s)

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn0', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': None}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Bar'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200


def test_app_create_without_register_app():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc = JSONRPC(service_url='/api', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc.method('app.fn2')
    def fn1(s: str) -> str:
        return 'Foo {0}'.format(s)

    jsonrpc.init_app(app)

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200


def test_app_create_with_method_without_annotation():
    with pytest.raises(ValueError, match='no type annotations present to: app.fn1'):
        app = Flask(__name__, instance_relative_config=True)
        jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

        # pylint: disable=W0612
        @jsonrpc.method('app.fn1')
        def fn1(s):
            return 'Foo {0}'.format(s)

        # pylint: disable=W0612
        @jsonrpc.method('app.fn2')
        def fn2(s: str) -> str:
            return 'Bar {0}'.format(s)

        # pylint: disable=W0612
        @jsonrpc.method('app.fn3')
        def fn3(s):  # pylint: disable=W0612
            return 'Poo {0}'.format(s)


def test_app_create_with_method_without_annotation_on_params():
    with pytest.raises(ValueError, match='no type annotations present to: app.fn2'):
        app = Flask(__name__, instance_relative_config=True)
        jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

        # pylint: disable=W0612
        @jsonrpc.method('app.fn4')
        def fn4():
            pass

        # pylint: disable=W0612
        @jsonrpc.method('app.fn2')
        def fn2(s) -> str:
            return 'Foo {0}'.format(s)

        # pylint: disable=W0612
        @jsonrpc.method('app.fn1')
        def fn1(s: str) -> str:
            return 'Bar {0}'.format(s)

        # pylint: disable=W0612
        @jsonrpc.method('app.fn3')
        def fn3(s):  # pylint: disable=W0612
            return 'Poo {0}'.format(s)


def test_app_create_with_method_without_annotation_on_return():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc.method('app.fn1')
    def fn1(s: str):
        return 'Foo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc.method('app.fn2')
    def fn2(s: str) -> str:
        return 'Bar {0}'.format(s)

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': [':)']})
        assert rv.json == {
            'error': {
                'code': -32602,
                'data': {'message': 'return type of str must be a type; got NoneType instead'},
                'message': 'Invalid params',
                'name': 'InvalidParamsError',
            },
            'id': 1,
            'jsonrpc': '2.0',
        }
        assert rv.status_code == 400

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Bar :)'}
        assert rv.status_code == 200


def test_app_create_with_wrong_return():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn1')
    def fn2(s: str) -> Tuple[str, int, int, int]:  # pylint: disable=W0612
        return 'Bar {0}'.format(s), 1, 2, 3

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': [':)']})
        assert rv.json == {
            'error': {
                'code': -32000,
                'data': {
                    'message': 'The view function did not return a valid '
                    'response tuple. The tuple must have the form '
                    '(body, status, headers), (body, status), or '
                    '(body, headers).'
                },
                'message': 'Server error',
                'name': 'ServerError',
            },
            'id': 1,
            'jsonrpc': '2.0',
        }
        assert rv.status_code == 500


def test_app_create_multiple_jsonrpc_versions():
    app = Flask(__name__, instance_relative_config=True)
    jsonrpc_v1 = JSONRPC(app, '/api/v1', enable_web_browsable_api=True)
    jsonrpc_v2 = JSONRPC(app, '/api/v2', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc_v1.method('app.fn2')
    def fn1_v1(s: str) -> str:
        return 'v1: Foo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc_v2.method('app.fn2')
    def fn1_v2(s: str) -> str:
        return 'v2: Foo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc_v1.method('app.fn3')
    def fn3(s: str) -> str:
        return 'Poo {0}'.format(s)

    # pylint: disable=W0612
    @jsonrpc_v2.method('app.fn1')
    def fn2(s: str) -> str:
        return 'Bar {0}'.format(s)

    with app.test_client() as client:
        rv = client.post('/api/v1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'v1: Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api/v2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':D']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'v2: Foo :D'}
        assert rv.status_code == 200

        rv = client.post('/api/v1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn3', 'params': [';)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Poo ;)'}
        assert rv.status_code == 200

        rv = client.post('/api/v2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': ['\\oB']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Bar \\oB'}
        assert rv.status_code == 200


def test_app_create_modular_apps():
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
    jsonrpc.register_blueprint(app, jsonrpc_api_1, url_prefix='/b1')
    jsonrpc.register_blueprint(app, jsonrpc_api_2, url_prefix='/b2')
    jsonrpc.register_blueprint(app, jsonrpc_api_3, url_prefix='/b3')

    with app.test_client() as client:
        rv = client.post('/api/b1', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue1.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b1: Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api/b2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue2.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b2: Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api/b2', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue2.fn1', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b2: Bar :)'}
        assert rv.status_code == 200

        rv = client.post('/api/b3', json={'id': 1, 'jsonrpc': '2.0', 'method': 'blue3.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'b3: Foo :)'}
        assert rv.status_code == 200
