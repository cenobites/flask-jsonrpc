# Copyright (c) 2020-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

import sys
import typing as t
import traceback

# Added in version 3.11.
from typing_extensions import Self

from flask import current_app

try:
    from flaskext.babel import gettext as _  # type: ignore

    _("You're lazy...")  # this function lazy-loads settings (pragma: no cover)
except (ImportError, NameError):
    _ = lambda t, *a, **k: t  # noqa: E731


class JSONRPCError(Exception):
    """Error class based on the `JSON-RPC 2.0 specs`_.

    Args:
        message (str | None, optional): Error message. Defaults to `None`.
        code (int | None, optional): Error code. Defaults to `0`.
        data (typing.Any | None, optional): Additional error data. Defaults to `None`.
        status_code (int | None, optional): HTTP status code. Defaults to `400`.

    Examples:
        >>> error = JSONRPCError(
        ...     message='An error occurred', code=1234, data={'info': 'details'}
        ... )
        >>> assert error.jsonrpc_format == {
        ...     'name': 'JSONRPCError',
        ...     'code': 1234,
        ...     'message': 'An error occurred',
        ...     'data': {'info': 'details'},
        ... }

    .. _JSON-RPC 2.0 specs:
        https://www.jsonrpc.org/specification
    .. _JSON-RPC Errors:
        https://www.jsonrpc.org/specification_v1#a2.2JSON-RPCoverHTTP
    """

    message: str | None = None
    code: int = 0
    data: t.Any | None = None  # noqa: ANN401
    status_code: int = 400

    def __init__(
        self: Self,
        message: str | None = None,
        code: int | None = None,
        data: t.Any | None = None,  # noqa: ANN401
        status_code: int | None = None,
    ) -> None:
        """Setup the Exception and overwrite the default message"""
        super().__init__(message)
        self.message = message or self.message
        self.code = code or self.code
        self.data = data or self.data
        self.status_code = status_code or self.status_code

    @property
    def jsonrpc_format(self: Self) -> dict[str, t.Any]:
        """Return the Exception data in a format for JSON-RPC

        Returns:
            dict[str, typing.Any]: The error data formatted for JSON-RPC

        Examples:
            >>> error = JSONRPCError(
            ...     message='An error occurred', code=1234, data={'info': 'details'}
            ... )
            >>> assert error.jsonrpc_format == {
            ...     'name': 'JSONRPCError',
            ...     'code': 1234,
            ...     'message': 'An error occurred',
            ...     'data': {'info': 'details'},
            ... }
        """
        error = {'name': self.__class__.__name__, 'code': self.code, 'message': self.message, 'data': self.data}

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

    def __init__(
        self: Self,
        message: str | None = _('Parse error'),
        code: int | None = -32700,
        data: t.Any | None = None,  # noqa: ANN401
        status_code: int | None = 400,
    ) -> None:
        super().__init__(message, code, data, status_code)


class InvalidRequestError(JSONRPCError):
    """The JSON sent is not a valid Request object."""

    def __init__(
        self: Self,
        message: str | None = _('Invalid Request'),
        code: int | None = -32600,
        data: t.Any | None = None,  # noqa: ANN401
        status_code: int | None = 400,
    ) -> None:
        super().__init__(message, code, data, status_code)


class MethodNotFoundError(JSONRPCError):
    """The method does not exist / is not available."""

    def __init__(
        self: Self,
        message: str | None = _('Method not found'),
        code: int | None = -32601,
        data: t.Any | None = None,  # noqa: ANN401
        status_code: int | None = 400,
    ) -> None:
        super().__init__(message, code, data, status_code)


class InvalidParamsError(JSONRPCError):
    """Invalid method parameter(s)."""

    def __init__(
        self: Self,
        message: str | None = _('Invalid params'),
        code: int | None = -32602,
        data: t.Any | None = None,  # noqa: ANN401
        status_code: int | None = 400,
    ) -> None:
        super().__init__(message, code, data, status_code)


class InternalError(JSONRPCError):
    """Internal JSON-RPC error."""

    def __init__(
        self: Self,
        message: str | None = _('Internal error'),
        code: int | None = -32603,
        data: t.Any | None = None,  # noqa: ANN401
        status_code: int | None = 400,
    ) -> None:
        super().__init__(message, code, data, status_code)


class ServerError(JSONRPCError):
    """Reserved for implementation-defined server-errors.

    Args:
        message (str | None, optional): Error message. Defaults to 'Server error'.
        code (int | None, optional): Error code. Defaults to -32000.
        data (typing.Any | None, optional): Additional error data. Defaults to `None`.
        status_code (int | None, optional): HTTP status code. Defaults to `500`.
        original_exception (BaseException | None, optional): The original exception that caused this error.
            Defaults to `None`.

    Notes:
        code: -32000 to -32099 Server error.

    Examples:
        >>> try:
        ...     1 / 0
        ... except ZeroDivisionError as e:
        ...     error = ServerError(original_exception=e)
        >>> assert error.jsonrpc_format == {
        ...     'name': 'ServerError',
        ...     'code': -32000,
        ...     'message': 'Server error',
        ...     'data': None,
        ... }
        >>> assert isinstance(error.original_exception, ZeroDivisionError)
    """

    def __init__(
        self: Self,
        message: str | None = _('Server error'),
        code: int | None = -32000,
        data: t.Any | None = None,  # noqa: ANN401
        status_code: int | None = 500,
        original_exception: BaseException | None = None,
    ) -> None:
        # The original exception that caused this 500 error. Can be
        # used by frameworks to provide context when handling
        # unexpected errors.
        self.original_exception = original_exception
        super().__init__(message, code, data, status_code)
