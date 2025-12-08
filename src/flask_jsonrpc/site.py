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

from uuid import UUID, uuid4
import typing as t
import logging
from collections import OrderedDict

# Added in version 3.11.
from typing_extensions import Self

from flask import json, request, current_app
from flask.logging import has_level_handler

from typeguard import TypeCheckError
from werkzeug.utils import cached_property
from typeguard._utils import qualified_name
from werkzeug.datastructures import Headers

from flask_jsonrpc.conf import settings
from flask_jsonrpc.helpers import get
from flask_jsonrpc.funcutils import bindfy
from flask_jsonrpc.descriptor import JSONRPCServiceDescriptor
from flask_jsonrpc.exceptions import (
    ParseError,
    ServerError,
    JSONRPCError,
    InvalidParamsError,
    InvalidRequestError,
    MethodNotFoundError,
)
from flask_jsonrpc.types.types import AnnotatedMetadataTypeError, type_checker

JSONRPC_VERSION_DEFAULT: str = '2.0'
JSONRPC_DEFAULT_HTTP_HEADERS: dict[str, str] = {}
JSONRPC_DEFAULT_HTTP_STATUS_CODE: int = 200


class JSONRPCSite:
    """JSON-RPC site to handle JSON-RPC requests.

    Args:
        version (str): The version of the JSON-RPC API.
        path (str | None): The URL path for the JSON-RPC site. If None, it will be set later.
        base_url (str | None): The base URL for the JSON-RPC site. If None, it will be set later.

    Attributes:
        path (str | None): The URL path for the JSON-RPC site.
        base_url (str | None): The base URL for the JSON-RPC site.
        error_handlers (dict[type[Exception], typing.Callable[[typing.Any], typing.Any]]): A mapping of exception
            types to their handlers.
        view_funcs (collections.OrderedDict[str, typing.Callable[..., typing.Any]]): A mapping of method names to
            their view functions.
        uuid (uuid.UUID): A unique identifier for the JSON-RPC site.
        name (str): The name of the JSON-RPC site.
        version (str): The version of the JSON-RPC API.
        describe (typing.Callable[[], dict[str, typing.Any]]): A callable that returns the service description.

    Examples:
        >>> jsonrpc_site = JSONRPCSite(
        ...     version='2.0', path='/api', base_url='http://localhost/api'
        ... )
    """

    def __init__(self: Self, version: str, path: str | None = None, base_url: str | None = None) -> None:
        self.path = path
        self.base_url = base_url
        self.error_handlers: dict[type[Exception], t.Callable[[t.Any], t.Any]] = {}
        self.view_funcs: t.OrderedDict[str, t.Callable[..., t.Any]] = OrderedDict()
        self.uuid: UUID = uuid4()
        self.name: str = 'Flask-JSONRPC'
        self.version: str = version
        self.describe = JSONRPCServiceDescriptor(self).describe

    def _is_notification_request(self: Self, req_json: dict[str, t.Any]) -> bool:
        """Check if the request is a notification request (without an 'id' member).

        Args:
            req_json (dict[str, typing.Any]): The JSON-RPC request data.

        Returns:
            bool: True if the request is a notification request, False otherwise.
        """
        return 'id' not in req_json

    def _is_batch_request(self: Self, req_json: t.Any) -> bool:  # noqa: ANN401
        """Check if the request is a batch request.

        Args:
            req_json (typing.Any): The JSON-RPC request data.

        Returns:
            bool: True if the request is a batch request, False otherwise.
        """
        return isinstance(req_json, list)

    def _find_error_handler(self: Self, exc: Exception) -> t.Callable[[t.Any], t.Any] | None:
        """Find the appropriate error handler for the given exception.

        Find the most specific error handler registered for the exception's class
        or its base classes.

        Args:
            exc (Exception): The exception to find a handler for.

        Returns:
            typing.Callable[[typing.Any], typing.Any] | None: The error handler if found, None otherwise.
        """
        exc_class = type(exc)
        if not self.error_handlers:
            return None

        for cls in exc_class.__mro__:
            handler = self.error_handlers.get(cls)
            if handler is not None:
                return handler
        return None

    @property
    def is_json(self: Self) -> bool:
        """Check if the mimetype indicates JSON data, either
        :mimetype:`application/json` or :mimetype:`application/*+json`.

        Note:
            https://github.com/pallets/werkzeug/blob/master/src/werkzeug/wrappers/json.py#L54

        Returns:
            bool: True if the mimetype indicates JSON data, False otherwise.
        """
        mt = request.mimetype
        return mt in ('application/json', 'application/json-rpc', 'application/jsonrequest') or (
            mt.startswith('application/') and mt.endswith('+json')
        )

    @cached_property
    def logger(self: Self) -> logging.Logger:
        """Get the logger for the JSON-RPC site.

        If the logger does not have any level handlers, a NullHandler is added.

        Returns:
            logging.Logger: The logger instance.
        """
        logger = logging.getLogger('flask_jsonrpc')
        if not has_level_handler(logger):
            logger.addHandler(logging.NullHandler())
        return logger

    def set_path(self: Self, path: str) -> None:
        """Set the URL path for the JSON-RPC site.

        Args:
            path (str): The URL path to set.
        """
        self.path = path

    def set_base_url(self: Self, base_url: str | None) -> None:
        """Set the base URL for the JSON-RPC site.

        Args:
            base_url (str | None): The base URL to set.
        """
        self.base_url = base_url

    def register_error_handler(self: Self, exception: type[Exception], fn: t.Callable[[t.Any], t.Any]) -> None:
        """Register an error handler for a specific exception type.

        Args:
            exception (type[Exception]): The exception type to register the handler for.
            fn (typing.Callable[[typing.Any], typing.Any]): The error handler function.

        Examples:
            >>> class MyException(Exception):
            ...     pass
            >>>
            >>>
            >>> def my_error_handler(exc: MyException) -> dict[str, Any]:
            ...     return {'message': str(exc), 'code': 1234}
            >>>
            >>> jsonrpc_site = JSONRPCSite(version='2.0', path='/api')
            >>> jsonrpc_site.register_error_handler(MyException, my_error_handler)
        """
        self.error_handlers[exception] = fn

    def register(self: Self, name: str, view_func: t.Callable[..., t.Any]) -> None:
        """Register a view function with the JSON-RPC site.

        Args:
            name (str): The name of the method.
            view_func (typing.Callable[..., typing.Any]): The view function to register.

        Examples:
            >>> def my_method(param1: int) -> str:
            ...     return str(param1)
            >>> jsonrpc_site = JSONRPCSite(version='2.0', path='/api')
            >>> jsonrpc_site.register('my_method', my_method)
        """
        self.view_funcs[name] = view_func

    def dispatch_request(self: Self) -> tuple[t.Any, int, Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
        """Dispatch the JSON-RPC request.

        Returns:
            tuple[typing.Any, int, werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
                The response data, status code, and headers.

        Raises:
            flask_jsonrpc.exceptions.ParseError: If the request is not valid JSON.
        """
        if not self.validate_request():
            raise ParseError(
                data={
                    'message': f'Invalid mime type for JSON: {request.mimetype}, '
                    'use header Content-Type: application/json'
                }
            ) from None

        json_data = self.to_json(request.data)
        if self._is_batch_request(json_data):
            return self.batch_dispatch(json_data)
        return self.handle_dispatch_except(json_data)

    def validate_request(self: Self) -> bool:
        """Validate the JSON-RPC request.

        Returns:
            bool: True if the request is valid, False otherwise.
        """
        if not self.is_json:
            self.logger.info('invalid mimetype')
            return False
        return True

    def to_json(self: Self, request_data: bytes) -> t.Any:  # noqa: ANN401
        """Convert the request data to JSON.

        Args:
            request_data (bytes): The request data.

        Returns:
            typing.Any: The JSON-decoded data.

        Raises:
            flask_jsonrpc.exceptions.ParseError: If the request data is not valid JSON.
        """
        try:
            return json.loads(request_data)
        except ValueError as e:
            self.logger.info('invalid json: %s', request_data, exc_info=e)
            raise ParseError(data={'message': f'Invalid JSON: {request_data!r}'}) from e

    def handle_view_func(self: Self, view_func: t.Callable[..., t.Any], params: t.Any) -> t.Any:  # noqa: ANN401
        """Handle the view function with the given parameters.

        Args:
            view_func (typing.Callable[..., typing.Any]): The view function to handle.
            params (typing.Any): The parameters to pass to the view function.

        Returns:
            typing.Any: The result of the view function.

        Raises:
            flask_jsonrpc.exceptions.InvalidParamsError: If the parameters are invalid.
            flask_jsonrpc.exceptions.InvalidParamsError: If there is an annotated metadata type error.
            flask_jsonrpc.exceptions.InvalidParamsError: If there is a type checking error.
            TypeError: If there is a type mismatch.

        TODO:
            - Enhance the checker to return the type.
        """
        view_func_params = getattr(view_func, 'jsonrpc_method_params', {})
        validate = getattr(view_func, 'jsonrpc_validate', settings.DEFAULT_JSONRPC_METHOD_VALIDATE)
        try:
            if isinstance(params, list):
                kw_params = {}
                for i, (param_name, _param_type) in enumerate(view_func_params.items()):
                    kw_params[param_name] = (params[i : i + 1] or [None])[0]
                binded_params = bindfy(view_func, kw_params)
            elif isinstance(params, dict):
                binded_params = bindfy(view_func, params)
            else:
                raise InvalidParamsError(
                    data={'message': f'Parameter structures are by-position (list) or by-name (dict): {params}'}
                ) from None

            if validate:
                binded_params = type_checker(view_func, binded_params)

            resp_view = current_app.ensure_sync(view_func)(**binded_params)

            # TODO: Enhance the checker to return the type
            view_fun_annotations = t.get_type_hints(view_func) if validate else {}
            view_fun_return: t.Any | None = view_fun_annotations.pop('return', type(None))
            if validate and resp_view is not None and view_fun_return is type(None):
                resp_view_qn = qualified_name(resp_view)
                view_fun_return_qn = qualified_name(view_fun_return)
                raise TypeError(
                    f'return type of {resp_view_qn} must be a type; got {view_fun_return_qn} instead'
                ) from None

            return resp_view
        except AnnotatedMetadataTypeError as e:
            self.logger.info('invalid annotated type checked for: %s', view_func.__name__, exc_info=e)
            raise InvalidParamsError(
                data={
                    'constraint': e.annotated.__class__.__name__,
                    'param': e.name,
                    'value': e.value,
                    'message': e.message,
                }
            ) from e
        except (TypeError, TypeCheckError) as e:
            self.logger.info('invalid type checked for: %s', getattr(view_func, '__name__', view_func), exc_info=e)
            raise InvalidParamsError(data={'message': str(e)}) from e

    def dispatch(
        self: Self, req_json: dict[str, t.Any]
    ) -> tuple[t.Any, int, Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
        """Dispatch the JSON-RPC request.

        Args:
            req_json (dict[str, typing.Any]): The JSON-RPC request data.

        Returns:
            tuple[typing.Any, int, werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
                The response data, status code, and headers.

        Raises:
            flask_jsonrpc.exceptions.MethodNotFoundError: If the requested method is not found.
            flask_jsonrpc.exceptions.InvalidRequestError: If the request is invalid.
        """
        method_name = req_json['method']
        params = req_json.get('params', {})
        view_func = self.view_funcs.get(method_name)
        notification = getattr(view_func, 'jsonrpc_notification', settings.DEFAULT_JSONRPC_METHOD_NOTIFICATION)
        if not view_func:
            raise MethodNotFoundError(data={'message': f'Method not found: {method_name}'}) from None

        if self._is_notification_request(req_json) and not notification:
            raise InvalidRequestError(
                data={
                    'message': f"The method {method_name!r} doesn't allow Notification "
                    "Request object (without an 'id' member)"
                }
            ) from None

        resp_view = self.handle_view_func(view_func, params)
        return self.make_response(req_json, resp_view)

    def handle_exception(
        self: Self, req_json: dict[str, t.Any], exc: Exception
    ) -> tuple[t.Any, int, Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
        """Handle exceptions that occur during request dispatch.

        If no specific error handler is found for the exception, a generic ServerError is used.

        Args:
            req_json (dict[str, typing.Any]): The JSON-RPC request data.
            exc (Exception): The exception that occurred.

        Returns:
            tuple[typing.Any, int, werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
                The response data, status code, and headers.
        """
        self.logger.info('unexpected error', exc_info=exc)
        jsonrpc_error = ServerError(data={'message': str(exc)}, original_exception=exc)
        jsonrpc_error_headers: Headers | dict[str, str] | tuple[str] | list[tuple[str]] = JSONRPC_DEFAULT_HTTP_HEADERS
        error_handler = self._find_error_handler(exc)

        # If no specific error handler found, use the generic ServerError handler if available
        if error_handler is None:
            exc = jsonrpc_error
            error_handler = self.error_handlers.get(ServerError)

        if error_handler is not None:
            resp_view = current_app.ensure_sync(error_handler)(exc)
            rv, status_code, headers = self.unpack_tuple_returns(
                resp_view, default_status_code=jsonrpc_error.status_code
            )
            jsonrpc_error.data = rv
            jsonrpc_error.status_code = status_code
            jsonrpc_error_headers = headers
        response = {
            'id': get(req_json, 'id'),
            'jsonrpc': get(req_json, 'jsonrpc', JSONRPC_VERSION_DEFAULT),
            'error': jsonrpc_error.jsonrpc_format,
        }
        return response, jsonrpc_error.status_code, jsonrpc_error_headers

    def handle_dispatch_except(
        self: Self, req_json: dict[str, t.Any]
    ) -> tuple[t.Any, int, Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
        """Handle the dispatch of the request and catch exceptions.

        If an exception occurs during dispatch, it is handled appropriately.

        Args:
            req_json (dict[str, typing.Any]): The JSON-RPC request data.

        Returns:
            tuple[typing.Any, int, werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
                The response data, status code, and headers.
        """
        try:
            if not self.validate(req_json):
                raise InvalidRequestError(data={'message': f'Invalid JSON: {req_json!r}'}) from None
            return self.dispatch(req_json)
        except Exception as e:
            if isinstance(e, JSONRPCError):  # mypyc: https://docs.python.org/3/glossary.html#term-EAFP
                self.logger.info('jsonrpc error', exc_info=e)
                response = {
                    'id': get(req_json, 'id'),
                    'jsonrpc': get(req_json, 'jsonrpc', JSONRPC_VERSION_DEFAULT),
                    'error': e.jsonrpc_format,
                }
                return response, e.status_code, JSONRPC_DEFAULT_HTTP_HEADERS
            return self.handle_exception(req_json, e)

    def batch_dispatch(
        self: Self, reqs_json: list[dict[str, t.Any]]
    ) -> tuple[list[t.Any], int, Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
        """Dispatch a batch of JSON-RPC requests.

        Args:
            reqs_json (list[dict[str, typing.Any]]): The list of JSON-RPC request data.

        Returns:
            tuple[
                list[typing.Any], int, werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]
            ]:
                The list of response data, status code, and headers.

        Raises:
            flask_jsonrpc.exceptions.InvalidRequestError: If the batch request is empty.
        """
        if not reqs_json:
            raise InvalidRequestError(data={'message': 'Empty array'}) from None

        resp_views = []
        headers = Headers()
        status_code = JSONRPC_DEFAULT_HTTP_STATUS_CODE
        for rv, _, hdrs in [self.handle_dispatch_except(rq) for rq in reqs_json]:
            headers.update([hdrs] if isinstance(hdrs, tuple) else hdrs)  # type: ignore
            if rv is None:
                continue
            resp_views.append(rv)
        if not resp_views:
            status_code = 204
        return resp_views, status_code, headers

    def validate(self: Self, req_json: dict[str, t.Any]) -> bool:
        """Validate the JSON-RPC request structure.

        Args:
            req_json (dict[str, typing.Any]): The JSON-RPC request data.

        Returns:
            bool: True if the request is valid, False otherwise.
        """
        return isinstance(req_json, dict) and 'method' in req_json

    def unpack_tuple_returns(
        self: Self,
        resp_view: t.Any,  # noqa: ANN401
        default_status_code: int = JSONRPC_DEFAULT_HTTP_STATUS_CODE,
        default_headers: Headers | dict[str, str] | tuple[str] | list[tuple[str]] = JSONRPC_DEFAULT_HTTP_HEADERS,
    ) -> tuple[t.Any, int, Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
        """Unpack the response tuple returned by a view function.

        Note:
            https://github.com/pallets/flask/blob/d091bb00c0358e9f30006a064f3dbb671b99aeae/src/flask/app.py#L1981

        Args:
            resp_view (typing.Any): The response returned by the view function.
            default_status_code (int): The default HTTP status code to use if not specified.
            default_headers (werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]):
                The default HTTP headers to use if not specified.

        Returns:
            tuple[typing.Any, int, werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
                The unpacked response body, status code, and headers.
        """
        # https://github.com/pallets/flask/blob/d091bb00c0358e9f30006a064f3dbb671b99aeae/src/flask/app.py#L1981
        if isinstance(resp_view, tuple):
            len_resp_view = len(resp_view)

            # a 3-tuple is unpacked directly
            if len_resp_view == 3:
                rv, status_code, headers = resp_view
            # decide if a 2-tuple has status or headers
            elif len_resp_view == 2:
                if isinstance(resp_view[1], Headers | dict | tuple | list):
                    rv, headers, status_code = resp_view + (default_status_code,)
                else:
                    rv, status_code, headers = resp_view + (default_headers,)
            # other sized tuples are not allowed
            else:
                raise TypeError(
                    'the view function did not return a valid response tuple.'
                    ' The tuple must have the form (body, status, headers),'
                    ' (body, status), or (body, headers).'
                ) from None
            return rv, status_code, headers

        return resp_view, default_status_code, default_headers

    def make_response(
        self: Self,
        req_json: dict[str, t.Any],
        resp_view: t.Any,  # noqa: ANN401
    ) -> tuple[t.Any, int, Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
        """Make a JSON-RPC response.

        Args:
            req_json (dict[str, typing.Any]): The JSON-RPC request data.
            resp_view (typing.Any): The response returned by the view function.

        Returns:
            tuple[typing.Any, int, werkzeug.datastructures.Headers | dict[str, str] | tuple[str] | list[tuple[str]]]:
                The response data, status code, and headers.
        """
        rv, status_code, headers = self.unpack_tuple_returns(resp_view)
        if self._is_notification_request(req_json):
            return None, 204, headers
        resp = {'id': req_json.get('id'), 'jsonrpc': req_json.get('jsonrpc', JSONRPC_VERSION_DEFAULT), 'result': rv}
        return resp, status_code, headers
