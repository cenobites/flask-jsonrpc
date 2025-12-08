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
from __future__ import annotations

import typing as t

# Added in version 3.11.
from typing_extensions import Self

from flask import typing as ft, make_response
from flask.views import MethodView

from flask_jsonrpc.site import JSONRPC_VERSION_DEFAULT, JSONRPC_DEFAULT_HTTP_HEADERS
from flask_jsonrpc.encoders import jsonify
from flask_jsonrpc.exceptions import JSONRPCError

if t.TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite


class JSONRPCView(MethodView):
    """JSON-RPC view to handle JSON-RPC requests.

    Args:
        jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): The JSON-RPC site instance.

    Attributes:
        jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): The JSON-RPC site instance.
    """

    def __init__(self: Self, jsonrpc_site: JSONRPCSite) -> None:
        self.jsonrpc_site = jsonrpc_site

    def post(self: Self) -> ft.ResponseReturnValue:
        """Handle POST requests for JSON-RPC.

        If the request is successful, returns a JSON response with the result.
        If there is a JSON-RPC error, returns a JSON response with the error details.

        Returns:
            flask.typing.ResponseReturnValue: The Flask response object.
        """
        try:
            response, status_code, headers = self.jsonrpc_site.dispatch_request()
            if status_code == 204:
                return make_response('', status_code, headers)
            return make_response(jsonify(response), status_code, headers)
        except JSONRPCError as e:
            self.jsonrpc_site.logger.info('jsonrpc error', exc_info=e)
            response = {'id': None, 'jsonrpc': JSONRPC_VERSION_DEFAULT, 'error': e.jsonrpc_format}
            return make_response(jsonify(response), e.status_code, JSONRPC_DEFAULT_HTTP_HEADERS)
