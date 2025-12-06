# Copyright (c) 2012-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

# Added in version 3.11.
from typing_extensions import Self

from flask import Flask, request

from flask_jsonrpc import JSONRPC, JSONRPCView
from flask_jsonrpc.contrib.browse import JSONRPCBrowse

if t.TYPE_CHECKING:
    from flask.typing import ResponseReturnValue


class UnauthorizedError(Exception):
    pass


class AuthorizationView(JSONRPCView):
    def check_auth(self: Self) -> bool:
        username = request.headers.get('X-Username')
        password = request.headers.get('X-Password')
        return username == 'username' and password == 'secret'

    def dispatch_request(self: Self) -> 'ResponseReturnValue':
        if not self.check_auth():
            raise UnauthorizedError()
        return super().dispatch_request()


app = Flask('multiplesite')
jsonrpc_v1 = JSONRPC(app, '/api/v1', enable_web_browsable_api=True)
jsonrpc_v2 = JSONRPC(app, '/api/v2', enable_web_browsable_api=True, jsonrpc_site_api=AuthorizationView)

browse = JSONRPCBrowse(app, url_prefix='/api/browse')
browse.register_jsonrpc_site(jsonrpc_v1.get_jsonrpc_site())
browse.register_jsonrpc_site(jsonrpc_v2.get_jsonrpc_site())


@jsonrpc_v1.method('App1.index')
def index_v1() -> str:
    return 'Welcome to Flask JSON-RPC Version API 1'


@jsonrpc_v2.method('App2.index')
def index_v2() -> str:
    return 'Welcome to Flask JSON-RPC Version API 2'
