# Copyright (c) 2020-2022, Cenobit Technologies, Inc. http://cenobit.es/
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

from flask import typing as ft
from flask import jsonify, current_app, make_response
from flask.views import MethodView

from .site import JSONRPC_VERSION_DEFAULT, JSONRPC_DEFAULT_HTTP_HEADERS
from .exceptions import JSONRPCError

if t.TYPE_CHECKING:
    from .site import JSONRPCSite


class JSONRPCView(MethodView):
    def __init__(self, jsonrpc_site: 'JSONRPCSite') -> None:
        self.jsonrpc_site = jsonrpc_site

    def post(self) -> ft.ResponseReturnValue:
        try:
            response, status_code, headers = self.jsonrpc_site.dispatch_request()
            if status_code == 204:
                return make_response('', status_code, headers)
            return make_response(jsonify(response), status_code, headers)
        except JSONRPCError as e:
            current_app.logger.exception('jsonrpc error')
            response = {
                'id': None,
                'jsonrpc': JSONRPC_VERSION_DEFAULT,
                'error': e.jsonrpc_format,
            }
            return make_response(jsonify(response), e.status_code, JSONRPC_DEFAULT_HTTP_HEADERS)
