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
import sys
import traceback
from typing import Any, Dict, Optional

from flask import current_app

try:
    from flaskext.babel import gettext as _  # type: ignore

    _("You're lazy...")  # this function lazy-loads settings (pragma: no cover)
except (ImportError, NameError):
    _ = lambda t, *a, **k: t  # noqa: E731


class JSONRPCError(Exception):
    """Error class based on the JSON-RPC 2.0 specs
    https://www.jsonrpc.org/specification

      message - string
      code    - number
      data    - object

      status_code - number    from https://www.jsonrpc.org/specification_v1#a2.2JSON-RPCoverHTTP
                              JSON-RPC over HTTP Errors section
    """

    code: int = 0
    message: Optional[str] = None
    data: Optional[Any] = None
    status_code: int = 400

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[int] = None,
        data: Optional[Any] = None,
        status_code: Optional[int] = None,
    ) -> None:
        """Setup the Exception and overwrite the default message
        """
        super(JSONRPCError, self).__init__()
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if data is not None:
            self.data = data
        if status_code is not None:
            self.status_code = status_code

    @property
    def jsonrpc_format(self) -> Dict[str, Any]:
        """Return the Exception data in a format for JSON-RPC
        """

        error = {
            'name': self.__class__.__name__,
            'code': self.code,
            'message': self.message,
            'data': self.data,
        }

        # RuntimeError: Working outside of application context.
        # This typically means that you attempted to use functionality that needed
        # to interface with the current application object in some way. To solve
        # this, set up an application context with app.app_context().  See the
        #  documentation for more information.
        if current_app and current_app.config['DEBUG']:  # pragma: no cover
            error['stack'] = traceback.format_exc()
            error['executable'] = sys.executable

        return error


# The error codes from and including -32768 to -32000 are reserved for
# pre-defined errors. Any code within this range, but not defined explicitly
# below is reserved for future use. The error codes are nearly the same as
# those suggested for XML-RPC at the following url:
# http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php


class ParseError(JSONRPCError):
    """Invalid JSON was received by the server.
    An error occurred on the server while parsing the JSON text.
    """

    code = -32700
    message = _('Parse error')


class InvalidRequestError(JSONRPCError):
    """The JSON sent is not a valid Request object.
    """

    code = -32600
    message = _('Invalid Request')


class MethodNotFoundError(JSONRPCError):
    """The method does not exist / is not available.
    """

    code = -32601
    message = _('Method not found')


class InvalidParamsError(JSONRPCError):
    """Invalid method parameter(s).
    """

    code = -32602
    message = _('Invalid params')


class InternalError(JSONRPCError):
    """Internal JSON-RPC error.
    """

    code = -32603
    message = _('Internal error')


class ServerError(JSONRPCError):
    """Reserved for implementation-defined server-errors.

    code: -32000 to -32099 Server error.
    """

    code = -32000
    message = _('Server error')
    status_code = 500
