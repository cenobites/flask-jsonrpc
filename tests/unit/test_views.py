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
import typing as t
import logging

from flask import Flask

import pytest

from flask_jsonrpc.views import JSONRPCView
from flask_jsonrpc.exceptions import JSONRPCError

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

pytestmark = pytest.mark.parallel_threads(1)


def test_jsonrpc_view_simple() -> None:
    class MockJSONRPCSite:
        def __init__(self: Self) -> None:
            self.logger = logging.getLogger('mock_jsonrpc_site')

        def dispatch_request(self: Self) -> tuple[t.Any, int, dict[str, t.Any]]:
            return {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}, 200, {}

    app = Flask('mehod_view')
    app.add_url_rule('/api', view_func=JSONRPCView.as_view('jsonrpc_view', jsonrpc_site=MockJSONRPCSite()))

    with app.test_client() as client:
        r = client.post('/api', json={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': ['Tequila']})
        assert r.status_code == 200
        assert r.json == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello world!'}


def test_jsonrpc_view_with_response_status_code_204() -> None:
    class MockJSONRPCSite:
        def __init__(self: Self) -> None:
            self.logger = logging.getLogger('mock_jsonrpc_site')

        def dispatch_request(self: Self) -> tuple[t.Any, int, dict[str, t.Any]]:
            return '', 204, {}

    app = Flask('mehod_view')
    app.add_url_rule('/api', view_func=JSONRPCView.as_view('jsonrpc_view', jsonrpc_site=MockJSONRPCSite()))

    with app.test_client() as client:
        r = client.post('/api', json={'jsonrpc': '2.0', 'method': 'app.index', 'params': ['Lou']})
        assert r.status_code == 204
        assert r.text == ''


def test_jsonrpc_view_with_invalid_request() -> None:
    class MockJSONRPCSite:
        def __init__(self: Self) -> None:
            self.logger = logging.getLogger('mock_jsonrpc_site')

        def dispatch_request(self: Self) -> tuple[t.Any, int, dict[str, t.Any]]:
            raise JSONRPCError(
                message='Invalid request', code=1001, data={'message': 'Invalid request'}, status_code=500
            )

    app = Flask('mehod_view')
    app.add_url_rule('/api', view_func=JSONRPCView.as_view('jsonrpc_view', jsonrpc_site=MockJSONRPCSite()))

    with app.test_client() as client:
        r = client.post('/api', data={'id': 1, 'jsonrpc': '2.0', 'method': 'app.index', 'params': ['Eve']})
        assert r.status_code == 500
        assert r.json == {
            'error': {
                'code': 1001,
                'data': {'message': ('Invalid request')},
                'message': 'Invalid request',
                'name': 'JSONRPCError',
            },
            'id': None,
            'jsonrpc': '2.0',
        }
