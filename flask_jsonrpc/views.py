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
from typing import TYPE_CHECKING, List

from flask import Response, jsonify, current_app, make_response
from flask.views import View

from .site import JSONRPC_VERSION_DEFAULT, JSONRPC_DEFAULT_HTTP_HEADERS
from .exceptions import JSONRPCError

if TYPE_CHECKING:
    from .site import JSONRPCSite


class JSONRPCView(View):
    methods: List[str] = ['POST']

    def __init__(self, jsonrpc_site: 'JSONRPCSite') -> None:
        self.jsonrpc_site = jsonrpc_site

    def dispatch_request(self) -> Response:  # type: ignore
        try:
            response, status_code, headers = self.jsonrpc_site.dispatch_request()
            if status_code == 204:
                return make_response('', status_code, headers)
            return make_response(jsonify(response), status_code, headers)
        except JSONRPCError as e:
            if current_app:
                current_app.logger.error('jsonrpc error')
                current_app.logger.exception(e)
            response = {
                'id': None,
                'jsonrpc': JSONRPC_VERSION_DEFAULT,
                'error': e.jsonrpc_format,
            }
            return make_response(jsonify(response), e.status_code, JSONRPC_DEFAULT_HTTP_HEADERS)
