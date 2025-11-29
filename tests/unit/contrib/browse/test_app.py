# Copyright (c) 2020-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
from flask_jsonrpc.typing import Field, Method
from flask_jsonrpc.contrib.browse import JSONRPCBrowse, build_package_tree


def test_browse_create() -> None:
    app = Flask('test_browse', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn1', validate=False)
    def fn1(s):  # noqa: ANN001,ANN202
        """Function app.fn1"""
        return f'Foo {s}'

    @jsonrpc.method('app.fn2', notification=True)
    def fn2(s: str) -> str:
        return f'Foo {s}'

    @jsonrpc.method('app.fn3', notification=False)
    def fn3(s: str) -> str:
        return f'Foo {s}'

    @jsonrpc.method('app.fn4', validate=False)
    def fn4(s, t: int, u, v: str, x, z):  # noqa: ANN001,ANN202
        return f'Not validate: {s} {t} {u} {v} {x} {z}'

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': [1]})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo 1'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn2', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn3', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'jsonrpc': '2.0', 'method': 'app.fn3', 'params': [':)']})
        assert rv.json == {
            'error': {
                'code': -32600,
                'data': {
                    'message': "The method 'app.fn3' doesn't allow Notification Request object (without an 'id' member)"
                },
                'message': 'Invalid Request',
                'name': 'InvalidRequestError',
            },
            'id': None,
            'jsonrpc': '2.0',
        }
        assert rv.status_code == 400

        rv = client.post(
            '/api',
            json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn4', 'params': [':)', 1, 3.2, ':D', [1, 2, 3], {1: 1}]},
        )
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': "Not validate: :) 1 3.2 :D [1, 2, 3] {'1': 1}"}
        assert rv.status_code == 200

        rv = client.post(
            '/api',
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'app.fn4',
                'params': {'s': ':)', 't': 1, 'u': 3.2, 'v': ':D', 'x': [1, 2, 3], 'z': {1: 1}},
            },
        )
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': "Not validate: :) 1 3.2 :D [1, 2, 3] {'1': 1}"}
        assert rv.status_code == 200

        rv = client.get('/api/browse')
        assert rv.status_code == 308

        rv = client.get('/api/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert b'/api' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/packages.json')
        assert rv.json == {
            'children': [
                {
                    'children': [],
                    'items': [
                        {
                            'description': 'Function app.fn1',
                            'name': 'app.fn1',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'Object'}],
                            'returns': {'name': 'default', 'type': 'Object'},
                            'type': 'method',
                            'validation': False,
                        },
                        {
                            'name': 'app.fn2',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                        {
                            'name': 'app.fn3',
                            'notification': False,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                        {
                            'name': 'app.fn4',
                            'notification': True,
                            'params': [
                                {'name': 's', 'type': 'Object'},
                                {'name': 't', 'type': 'Number'},
                                {'name': 'u', 'type': 'Object'},
                                {'name': 'v', 'type': 'String'},
                                {'name': 'x', 'type': 'Object'},
                                {'name': 'z', 'type': 'Object'},
                            ],
                            'returns': {'name': 'default', 'type': 'Object'},
                            'type': 'method',
                            'validation': False,
                        },
                    ],
                    'name': 'app',
                }
            ],
            'items': [],
            'name': None,
        }

        assert rv.status_code == 200

        rv = client.get('/api/browse/app.fn2.json')
        assert rv.json == {
            'name': 'app.fn2',
            'type': 'method',
            'notification': True,
            'validation': True,
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
        }
        assert rv.status_code == 200

        rv = client.get('/api/browse/app.not_found.json')
        assert rv.status_code == 404

        rv = client.get('/api/browse/partials/menu_tree.html')
        assert b'menu-tree' in rv.data
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


def test_jsonrpc_browse_empty() -> None:
    app = Flask('test_browse', instance_relative_config=True)
    jsonrpc_browse = JSONRPCBrowse()
    jsonrpc_browse.init_app(app)

    with app.test_client() as client:
        rv = client.get('/api/browse/packages.json')
        assert rv.json == {}
        rv = client.get('/api/browse/App.index.json')
        assert rv.status_code == 404

        rv = client.get('/api/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200


def test_browse_create_without_register_app() -> None:
    app = Flask('test_browse', instance_relative_config=True)
    jsonrpc = JSONRPC(path='/api', enable_web_browsable_api=True)

    @jsonrpc.method('app.fn2')
    def fn1(s: str) -> str:
        return f'Foo {s}'

    jsonrpc.init_app(app)

    with app.test_client() as client:
        rv = client.get('/api/browse/packages.json')
        assert rv.json == {
            'children': [
                {
                    'children': [],
                    'items': [
                        {
                            'name': 'app.fn2',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        }
                    ],
                    'name': 'app',
                }
            ],
            'items': [],
            'name': None,
        }
        assert rv.status_code == 200

        rv = client.get('/api/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert b'/api' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200


def test_browse_create_multiple_jsonrpc_versions() -> None:
    app = Flask('test_browse', instance_relative_config=True)
    jsonrpc_v1 = JSONRPC(app, '/api/v1', enable_web_browsable_api=True)
    jsonrpc_v2 = JSONRPC(app, '/api/v2', enable_web_browsable_api=True)

    @jsonrpc_v1.method('app.fn2')
    def fn1_v1(s: str) -> str:
        return f'v1: Foo {s}'

    @jsonrpc_v1.method('app.fn3')
    def fn3(s: str) -> str:
        return f'Poo {s}'

    @jsonrpc_v2.method('app.fn2')
    def fn1_v2(s: str) -> str:
        return f'v2: Foo {s}'

    @jsonrpc_v2.method('app.fn1')
    def fn2(s: str) -> str:
        return f'Bar {s}'

    with app.test_client() as client:
        rv = client.get('/api/v1/browse/packages.json')
        assert rv.json == {
            'children': [
                {
                    'children': [],
                    'items': [
                        {
                            'name': 'app.fn2',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                        {
                            'name': 'app.fn3',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                    ],
                    'name': 'app',
                }
            ],
            'items': [],
            'name': None,
        }
        assert rv.status_code == 200

        rv = client.get('/api/v1/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert b'/api/v1' in rv.data
        assert b'/api/v2' not in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/v1/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/v1/browse/app.fn3.json')
        assert rv.json == {
            'name': 'app.fn3',
            'type': 'method',
            'notification': True,
            'validation': True,
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
        }
        assert rv.status_code == 200

        rv = client.get('/api/v1/browse/app.fn1.json')
        assert rv.status_code == 404

        rv = client.get('/api/v2/browse/packages.json')
        assert rv.json == {
            'children': [
                {
                    'children': [],
                    'items': [
                        {
                            'name': 'app.fn1',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                        {
                            'name': 'app.fn2',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                    ],
                    'name': 'app',
                }
            ],
            'items': [],
            'name': None,
        }
        assert rv.status_code == 200

        rv = client.get('/api/v2/browse/app.fn1.json')
        assert rv.json == {
            'name': 'app.fn1',
            'type': 'method',
            'notification': True,
            'validation': True,
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
        }
        assert rv.status_code == 200

        rv = client.get('/api/v2/browse/app.fn3.json')
        assert rv.status_code == 404

        rv = client.get('/api/v2/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert b'/api/v2/browse' in rv.data
        assert b'/api/v2' in rv.data
        assert b'/api/v1/browse/static/' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/v2/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200


def test_browse_create_modular_apps() -> None:
    jsonrpc_api_1 = JSONRPCBlueprint('jsonrpc_api_1', __name__)

    @jsonrpc_api_1.method('blue1.fn2')
    def fn1_b1(s: str) -> str:
        return f'b1: Foo {s}'

    jsonrpc_api_2 = JSONRPCBlueprint('jsonrpc_api_2', __name__)

    @jsonrpc_api_2.method('blue2.fn2')
    def fn1_b2(s: str) -> str:
        return f'b2: Foo {s}'

    @jsonrpc_api_2.method('blue2.fn1')
    def fn2_b2(s: str) -> str:
        return f'b2: Bar {s}'

    @jsonrpc_api_2.method('blue2.not_notify', notification=False)
    def fn3_b2(s: str) -> str:
        return f'fn3 b2: Foo {s}'

    jsonrpc_api_3 = JSONRPCBlueprint('jsonrpc_api_3', __name__)

    @jsonrpc_api_3.method('blue3.fn2')
    def fn1_b3(s: str) -> str:
        return f'fn1 b3: Foo {s}'

    app = Flask('test_browse', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_1, url_prefix='/b1', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_2, url_prefix='/b2', enable_web_browsable_api=True)
    jsonrpc.register_blueprint(app, jsonrpc_api_3, url_prefix='/b3')

    with app.test_client() as client:
        rv = client.get('/api/browse/packages.json')
        assert rv.json == {
            'children': [
                {
                    'children': [],
                    'items': [
                        {
                            'name': 'blue1.fn2',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        }
                    ],
                    'name': 'blue1',
                },
                {
                    'children': [],
                    'items': [
                        {
                            'name': 'blue2.fn1',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                        {
                            'name': 'blue2.fn2',
                            'notification': True,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                        {
                            'name': 'blue2.not_notify',
                            'notification': False,
                            'params': [{'name': 's', 'type': 'String'}],
                            'returns': {'name': 'default', 'type': 'String'},
                            'type': 'method',
                            'validation': True,
                        },
                    ],
                    'name': 'blue2',
                },
            ],
            'items': [],
            'name': None,
        }
        assert rv.status_code == 200

        rv = client.get('/api/browse/')
        assert b'Flask JSON-RPC | Web Browsable API' in rv.data
        assert b'/api/b1' in rv.data
        assert b'/api/b2' in rv.data
        assert b'/api/b3' not in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/browse/static/js/main.js')
        assert b'App' in rv.data
        assert rv.status_code == 200

        rv = client.get('/api/b1/browse/packages.json')
        assert rv.status_code == 404

        rv = client.get('/api/b2/browse/packages.json')
        assert rv.status_code == 404

        rv = client.get('/api/b3/browse')
        assert rv.status_code == 404

        rv = client.get('/api/browse/blue2.fn1.json')
        assert rv.status_code == 200
        assert rv.json == {
            'name': 'blue2.fn1',
            'type': 'method',
            'notification': True,
            'validation': True,
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
        }

        rv = client.get('/api/browse/blue2.fn2.json')
        assert rv.status_code == 200
        assert rv.json == {
            'name': 'blue2.fn2',
            'type': 'method',
            'notification': True,
            'validation': True,
            'params': [{'name': 's', 'type': 'String'}],
            'returns': {'name': 'default', 'type': 'String'},
        }

        rv = client.get('/api/browse/blue3.fn3.json')
        assert rv.status_code == 404


def test_build_package_tree() -> None:
    service_methods = {
        'app.fn1': Method(
            name='app.fn1',
            tags=['tag1', 'tag2'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.fn2': Method(
            name='app.fn2',
            tags=['tag1'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.fn3': Method(
            name='app.fn3',
            tags=['tag1', 'tag3'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.fn4': Method(
            name='app.fn4',
            tags=['tag2'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.fn5': Method(
            name='app.fn5',
            tags=['tag3'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.default1': Method(
            name='app.default1',
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.fn6': Method(
            name='app.fn6',
            tags=['tag3'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.fn7': Method(
            name='app.fn7',
            tags=['tag3'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.default2': Method(
            name='app.default2',
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
        'app.fnX': Method(
            name='app.fnX',
            tags=['tag1', 'tag3'],
            params=[Field(name='s', type='Object')],
            returns=Field(name='default', type='Object'),
            type='method',
        ),
    }

    package_tree = build_package_tree(service_methods)
    assert package_tree == {
        'children': [
            {
                'children': [],
                'items': [
                    {
                        'name': 'app.default1',
                        'notification': True,
                        'params': [{'name': 's', 'type': 'Object'}],
                        'returns': {'name': 'default', 'type': 'Object'},
                        'type': 'method',
                        'validation': True,
                    },
                    {
                        'name': 'app.default2',
                        'notification': True,
                        'params': [{'name': 's', 'type': 'Object'}],
                        'returns': {'name': 'default', 'type': 'Object'},
                        'type': 'method',
                        'validation': True,
                    },
                ],
                'name': 'app',
            },
            {
                'children': [
                    {
                        'children': [],
                        'items': [
                            {
                                'name': 'app.fn1',
                                'notification': True,
                                'params': [{'name': 's', 'type': 'Object'}],
                                'returns': {'name': 'default', 'type': 'Object'},
                                'tags': ['tag1', 'tag2'],
                                'type': 'method',
                                'validation': True,
                            }
                        ],
                        'name': 'tag2',
                    },
                    {
                        'children': [],
                        'items': [
                            {
                                'name': 'app.fn3',
                                'notification': True,
                                'params': [{'name': 's', 'type': 'Object'}],
                                'returns': {'name': 'default', 'type': 'Object'},
                                'tags': ['tag1', 'tag3'],
                                'type': 'method',
                                'validation': True,
                            },
                            {
                                'name': 'app.fnX',
                                'notification': True,
                                'params': [{'name': 's', 'type': 'Object'}],
                                'returns': {'name': 'default', 'type': 'Object'},
                                'tags': ['tag1', 'tag3'],
                                'type': 'method',
                                'validation': True,
                            },
                        ],
                        'name': 'tag3',
                    },
                ],
                'items': [
                    {
                        'name': 'app.fn2',
                        'notification': True,
                        'params': [{'name': 's', 'type': 'Object'}],
                        'returns': {'name': 'default', 'type': 'Object'},
                        'tags': ['tag1'],
                        'type': 'method',
                        'validation': True,
                    }
                ],
                'name': 'tag1',
            },
            {
                'children': [],
                'items': [
                    {
                        'name': 'app.fn4',
                        'notification': True,
                        'params': [{'name': 's', 'type': 'Object'}],
                        'returns': {'name': 'default', 'type': 'Object'},
                        'tags': ['tag2'],
                        'type': 'method',
                        'validation': True,
                    }
                ],
                'name': 'tag2',
            },
            {
                'children': [],
                'items': [
                    {
                        'name': 'app.fn5',
                        'notification': True,
                        'params': [{'name': 's', 'type': 'Object'}],
                        'returns': {'name': 'default', 'type': 'Object'},
                        'tags': ['tag3'],
                        'type': 'method',
                        'validation': True,
                    },
                    {
                        'name': 'app.fn6',
                        'notification': True,
                        'params': [{'name': 's', 'type': 'Object'}],
                        'returns': {'name': 'default', 'type': 'Object'},
                        'tags': ['tag3'],
                        'type': 'method',
                        'validation': True,
                    },
                    {
                        'name': 'app.fn7',
                        'notification': True,
                        'params': [{'name': 's', 'type': 'Object'}],
                        'returns': {'name': 'default', 'type': 'Object'},
                        'tags': ['tag3'],
                        'type': 'method',
                        'validation': True,
                    },
                ],
                'name': 'tag3',
            },
        ],
        'items': [],
        'name': None,
    }
