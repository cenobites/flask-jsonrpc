# Copyright (c) 2024-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
from flask_jsonrpc.contrib.openrpc import OpenRPC, typing as st


def test_openrpc_create() -> None:
    app = Flask('test_openrpc', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api')
    openrpc = OpenRPC(
        app,
        jsonrpc,
        openrpc_schema=st.OpenRPCSchema(
            info=st.Info(
                title='OpenRPC API',
                version='0.0.1',
                description='A full description of OpenRPC API',
                terms_of_service='https://github.com/cenobites/flask-jsonrpc?tab=readme-ov-file',
                contact=st.Contact(name='Foo', url='https://flask-jsonrpc.cenobit.es', email='foo@bar.com'),
                license=st.License(
                    name='BSD License', url='https://github.com/cenobites/flask-jsonrpc?tab=BSD-3-Clause-2-ov-file'
                ),
            )
        ),
    )

    @jsonrpc.method('app.fn1', validate=False)
    def fn1(s):  # noqa: ANN001,ANN202
        """Function app.fn1"""
        return f'Foo {s}'

    @openrpc.extend_schema(
        name='FN2',
        summary='Function app.fn2',
        description='Full description of app.fn2',
        params=[
            st.ContentDescriptor(
                name='s', description='The s parameter', schema_=st.Schema(type=st.SchemaDataType.STRING)
            )
        ],
        result=st.ContentDescriptor(
            name='result',
            description='The result of function app.fn2',
            schema_=st.Schema(type=st.SchemaDataType.STRING),
        ),
        examples=[
            st.ExamplePairing(
                name='default',
                summary='Default example',
                description='Full description for default example',
                params=[st.Example(name='s', value='bar')],
                result=st.Example(name='result', value='Foo bar'),
            )
        ],
        errors=[st.Error(code=-32600, message='Invalid Request', data={'s': 'Parameter is required'})],
        external_docs=st.ExternalDocumentation(
            url='https://github.com/cenobites/flask-jsonrpc?tab=readme-ov-file', description='Documentation'
        ),
        deprecated=False,
    )
    @jsonrpc.method('app.fn2', notification=True)
    def fn2(s: str) -> str:
        return f'Foo {s}'

    @openrpc.extend_schema(
        name='FN3',
        summary='Function app.fn3',
        description='Full description of app.fn3',
        params=[
            st.ContentDescriptor(
                name='s', description='The s parameter', schema_=st.Schema(type=st.SchemaDataType.STRING)
            )
        ],
        result=st.ContentDescriptor(
            name='result',
            description='The result of function app.fn3',
            schema_=st.Schema(type=st.SchemaDataType.STRING),
        ),
        examples=[
            st.ExamplePairing(
                name='default',
                summary='Default example',
                description='Full description for default example',
                params=[st.Example(name='s', value='bar')],
                result=st.Example(name='result', value='Foo bar'),
            )
        ],
        errors=[st.Error(code=-32600, message='Invalid Request', data={'s': 'Parameter is required'})],
        external_docs=st.ExternalDocumentation(
            url='https://github.com/cenobites/flask-jsonrpc?tab=readme-ov-file', description='Documentation'
        ),
        deprecated=False,
    )
    @jsonrpc.method('app.fn3', validate=False)
    def fn3(s: str) -> str:
        return f'Foo {s}'

    @openrpc.extend_schema(name='FN4')
    @jsonrpc.method('app.fn4', notification=False)
    def fn4(s: str) -> str:
        return f'Foo {s}'

    @jsonrpc.method('app.fn5', validate=False)
    def fn5(s, t: int, u, v: str, x, z):  # noqa: ANN001,ANN202
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

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn4', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200

        rv = client.post(
            '/api',
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'app.fn5',
                'params': {'s': ':)', 't': 1, 'u': 3.2, 'v': ':D', 'x': [1, 2, 3], 'z': {1: 1}},
            },
        )
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': "Not validate: :) 1 3.2 :D [1, 2, 3] {'1': 1}"}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.discover'})
        assert rv.json['id'] == 1
        assert rv.json['jsonrpc'] == '2.0'
        assert rv.json['result'] == {
            'info': {
                'contact': {'email': 'foo@bar.com', 'name': 'Foo', 'url': 'https://flask-jsonrpc.cenobit.es'},
                'description': 'A full description of OpenRPC API',
                'license': {
                    'name': 'BSD License',
                    'url': 'https://github.com/cenobites/flask-jsonrpc?tab=BSD-3-Clause-2-ov-file',
                },
                'termsOfService': 'https://github.com/cenobites/flask-jsonrpc?tab=readme-ov-file',
                'title': 'OpenRPC API',
                'version': '0.0.1',
            },
            'methods': [
                {
                    'name': 'rpc.describe',
                    'description': 'Service description for JSON-RPC 2.0',
                    'params': [],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
                {
                    'description': 'Returns an OpenRPC schema as a description of this service',
                    'name': 'rpc.discover',
                    'params': [],
                    'result': {
                        'name': 'OpenRPC Schema',
                        'schema': {'$ref': 'https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'},
                    },
                },
                {
                    'description': 'Function app.fn1',
                    'name': 'app.fn1',
                    'params': [{'name': 's', 'schema': {'type': 'object'}}],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
                {
                    'deprecated': False,
                    'description': 'Full description of app.fn2',
                    'errors': [{'code': -32600, 'data': {'s': 'Parameter is required'}, 'message': 'Invalid Request'}],
                    'examples': [
                        {
                            'description': 'Full description for default example',
                            'name': 'default',
                            'params': [{'name': 's', 'value': 'bar'}],
                            'result': {'name': 'result', 'value': 'Foo bar'},
                            'summary': 'Default example',
                        }
                    ],
                    'externalDocs': {
                        'description': 'Documentation',
                        'url': 'https://github.com/cenobites/flask-jsonrpc?tab=readme-ov-file',
                    },
                    'name': 'FN2',
                    'params': [{'description': 'The s parameter', 'name': 's', 'schema': {'type': 'string'}}],
                    'result': {
                        'description': 'The result of function app.fn2',
                        'name': 'result',
                        'schema': {'type': 'string'},
                    },
                    'summary': 'Function app.fn2',
                },
                {
                    'deprecated': False,
                    'description': 'Full description of app.fn3',
                    'errors': [{'code': -32600, 'data': {'s': 'Parameter is required'}, 'message': 'Invalid Request'}],
                    'examples': [
                        {
                            'description': 'Full description for default example',
                            'name': 'default',
                            'params': [{'name': 's', 'value': 'bar'}],
                            'result': {'name': 'result', 'value': 'Foo bar'},
                            'summary': 'Default example',
                        }
                    ],
                    'externalDocs': {
                        'description': 'Documentation',
                        'url': 'https://github.com/cenobites/flask-jsonrpc?tab=readme-ov-file',
                    },
                    'name': 'FN3',
                    'params': [{'description': 'The s parameter', 'name': 's', 'schema': {'type': 'string'}}],
                    'result': {
                        'description': 'The result of function app.fn3',
                        'name': 'result',
                        'schema': {'type': 'string'},
                    },
                    'summary': 'Function app.fn3',
                },
                {
                    'name': 'FN4',
                    'params': [{'name': 's', 'schema': {'type': 'string'}}],
                    'result': {'name': 'default', 'schema': {'type': 'string'}},
                },
                {
                    'name': 'app.fn5',
                    'params': [
                        {'name': 's', 'schema': {'type': 'object'}},
                        {'name': 't', 'schema': {'type': 'integer'}},
                        {'name': 'u', 'schema': {'type': 'object'}},
                        {'name': 'v', 'schema': {'type': 'string'}},
                        {'name': 'x', 'schema': {'type': 'object'}},
                        {'name': 'z', 'schema': {'type': 'object'}},
                    ],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
            ],
            'openrpc': '1.3.2',
            'servers': {'name': 'default', 'url': 'localhost'},
        }


def test_openrpc_create_by_autogenerate() -> None:
    app = Flask('test_openrpc', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api')
    openrpc = OpenRPC()
    openrpc.init_app(app, jsonrpc)

    @jsonrpc.method('app.fn1', validate=False)
    def fn1(s):  # noqa: ANN001,ANN202
        """Function app.fn1"""
        return f'Foo {s}'

    @jsonrpc.method('app.fn2', notification=True)
    def fn2(s: str) -> str:
        return f'Foo {s}'

    @jsonrpc.method('app.fn3', validate=False)
    def fn3(s: str) -> str:
        return f'Foo {s}'

    @openrpc.extend_schema(name='FN3')
    @jsonrpc.method('app.fn4', notification=False)
    def fn4(s: str) -> str:
        return f'Foo {s}'

    @jsonrpc.method('app.fn5', validate=False)
    def fn5(s, t: int, u, v: str, x, z):  # noqa: ANN001,ANN202
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

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn4', 'params': [':)']})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo :)'}
        assert rv.status_code == 200

        rv = client.post(
            '/api',
            json={
                'id': 1,
                'jsonrpc': '2.0',
                'method': 'app.fn5',
                'params': {'s': ':)', 't': 1, 'u': 3.2, 'v': ':D', 'x': [1, 2, 3], 'z': {1: 1}},
            },
        )
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': "Not validate: :) 1 3.2 :D [1, 2, 3] {'1': 1}"}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.discover'})
        assert rv.json['id'] == 1
        assert rv.json['jsonrpc'] == '2.0'
        assert rv.json['result'] == {
            'info': {'title': 'Flask-JSONRPC', 'version': '0.0.1'},
            'methods': [
                {
                    'name': 'rpc.describe',
                    'description': 'Service description for JSON-RPC 2.0',
                    'params': [],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
                {
                    'description': 'Returns an OpenRPC schema as a description of this service',
                    'name': 'rpc.discover',
                    'params': [],
                    'result': {
                        'name': 'OpenRPC Schema',
                        'schema': {'$ref': 'https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'},
                    },
                },
                {
                    'description': 'Function app.fn1',
                    'name': 'app.fn1',
                    'params': [{'name': 's', 'schema': {'type': 'object'}}],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
                {
                    'name': 'app.fn2',
                    'params': [{'name': 's', 'schema': {'type': 'string'}}],
                    'result': {'name': 'default', 'schema': {'type': 'string'}},
                },
                {
                    'name': 'app.fn3',
                    'params': [{'name': 's', 'schema': {'type': 'string'}}],
                    'result': {'name': 'default', 'schema': {'type': 'string'}},
                },
                {
                    'name': 'FN3',
                    'params': [{'name': 's', 'schema': {'type': 'string'}}],
                    'result': {'name': 'default', 'schema': {'type': 'string'}},
                },
                {
                    'name': 'app.fn5',
                    'params': [
                        {'name': 's', 'schema': {'type': 'object'}},
                        {'name': 't', 'schema': {'type': 'integer'}},
                        {'name': 'u', 'schema': {'type': 'object'}},
                        {'name': 'v', 'schema': {'type': 'string'}},
                        {'name': 'x', 'schema': {'type': 'object'}},
                        {'name': 'z', 'schema': {'type': 'object'}},
                    ],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
            ],
            'openrpc': '1.3.2',
            'servers': {'name': 'default', 'url': '/api'},
        }


def test_openrpc_create_with_blueprint() -> None:
    article = JSONRPCBlueprint('article', __name__)

    @article.method('Article.index')
    def article_index() -> str:
        return 'Welcome to Article API'

    user = JSONRPCBlueprint('user', __name__)

    @user.method('User.index')
    def user_index() -> str:
        return 'Welcome to User API'

    app = Flask('test_openrpc', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api')
    jsonrpc.register_blueprint(app, user, url_prefix='/user')
    jsonrpc.register_blueprint(app, article, url_prefix='/article')
    openrpc = OpenRPC(app=app, jsonrpc_app=jsonrpc)

    @openrpc.extend_schema(name='App.index')
    @jsonrpc.method('App.index')
    def index() -> str:
        return 'Welcome to Flask JSON-RPC'

    with app.test_client() as client:
        rv = client.post('/api/article', json={'id': 1, 'jsonrpc': '2.0', 'method': 'Article.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Article API'}
        assert rv.status_code == 200

        rv = client.post('/api/article', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.discover'})
        assert rv.json['id'] == 1
        assert rv.json['jsonrpc'] == '2.0'
        assert rv.json['result'] == {
            'info': {'title': 'Flask-JSONRPC', 'version': '0.0.1'},
            'methods': [
                {
                    'name': 'rpc.describe',
                    'description': 'Service description for JSON-RPC 2.0',
                    'params': [],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
                {'name': 'Article.index', 'params': [], 'result': {'name': 'default', 'schema': {'type': 'string'}}},
                {
                    'description': 'Returns an OpenRPC schema as a description of this service',
                    'name': 'rpc.discover',
                    'params': [],
                    'result': {
                        'name': 'OpenRPC Schema',
                        'schema': {'$ref': 'https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'},
                    },
                },
            ],
            'openrpc': '1.3.2',
            'servers': {'name': 'default', 'url': '/api/article'},
        }

        rv = client.post('/api/user', json={'id': 1, 'jsonrpc': '2.0', 'method': 'User.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to User API'}
        assert rv.status_code == 200

        rv = client.post('/api/user', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.discover'})
        assert rv.json['id'] == 1
        assert rv.json['jsonrpc'] == '2.0'
        assert rv.json['result'] == {
            'info': {'title': 'Flask-JSONRPC', 'version': '0.0.1'},
            'methods': [
                {
                    'name': 'rpc.describe',
                    'description': 'Service description for JSON-RPC 2.0',
                    'params': [],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
                {'name': 'User.index', 'params': [], 'result': {'name': 'default', 'schema': {'type': 'string'}}},
                {
                    'description': 'Returns an OpenRPC schema as a description of this service',
                    'name': 'rpc.discover',
                    'params': [],
                    'result': {
                        'name': 'OpenRPC Schema',
                        'schema': {'$ref': 'https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'},
                    },
                },
            ],
            'openrpc': '1.3.2',
            'servers': {'name': 'default', 'url': '/api/user'},
        }

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'App.index', 'params': []})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Welcome to Flask JSON-RPC'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.discover'})
        assert rv.json['id'] == 1
        assert rv.json['jsonrpc'] == '2.0'
        assert rv.json['result']['info'] == {'title': 'Flask-JSONRPC', 'version': '0.0.1'}
        assert rv.json['result']['openrpc'] == '1.3.2'
        assert rv.json['result']['servers'] == {'name': 'default', 'url': '/api'}
        assert len(rv.json['result']['methods']) == 5
        assert sorted(rv.json['result']['methods'], key=lambda d: d['name']) == sorted(
            [
                {
                    'name': 'rpc.describe',
                    'description': 'Service description for JSON-RPC 2.0',
                    'params': [],
                    'result': {'name': 'default', 'schema': {'type': 'object'}},
                },
                {
                    'description': 'Returns an OpenRPC schema as a description of this service',
                    'name': 'rpc.discover',
                    'params': [],
                    'result': {
                        'name': 'OpenRPC Schema',
                        'schema': {'$ref': 'https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'},
                    },
                },
                {'name': 'App.index', 'params': [], 'result': {'name': 'default', 'schema': {'type': 'string'}}},
                {'name': 'Article.index', 'params': [], 'result': {'name': 'default', 'schema': {'type': 'string'}}},
                {'name': 'User.index', 'params': [], 'result': {'name': 'default', 'schema': {'type': 'string'}}},
            ],
            key=lambda d: d['name'],
        )


def test_openrpc_disabled() -> None:
    app = Flask('test_openrpc', instance_relative_config=True)
    jsonrpc = JSONRPC(app, '/api')

    @jsonrpc.method('app.fn1', validate=False)
    def fn1(s):  # noqa: ANN001,ANN202
        """Function app.fn1"""
        return f'Foo {s}'

    with app.test_client() as client:
        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.fn1', 'params': [1]})
        assert rv.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Foo 1'}
        assert rv.status_code == 200

        rv = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'rpc.discover'})
        assert rv.status_code == 400
        assert rv.json == {
            'error': {
                'code': -32601,
                'data': {'message': 'Method not found: rpc.discover'},
                'message': 'Method not found',
                'name': 'MethodNotFoundError',
            },
            'id': 1,
            'jsonrpc': '2.0',
        }
