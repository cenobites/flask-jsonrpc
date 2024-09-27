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
# pylint: disable=R0904
from uuid import UUID, uuid4
import typing as t
from collections import OrderedDict

from flask import json, request, current_app

from typeguard import qualified_name
from werkzeug.datastructures import Headers

from .helpers import get
from .settings import settings
from .funcutils import bindfy
from .descriptor import JSONRPCServiceDescriptor
from .exceptions import (
    ParseError,
    ServerError,
    JSONRPCError,
    InvalidParamsError,
    InvalidRequestError,
    MethodNotFoundError,
)

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

JSONRPC_VERSION_DEFAULT: str = '2.0'
JSONRPC_DEFAULT_HTTP_HEADERS: t.Dict[str, str] = {}
JSONRPC_DEFAULT_HTTP_STATUS_CODE: int = 200


class JSONRPCSite:
    def __init__(self: Self, path: t.Optional[str] = None, base_url: t.Optional[str] = None) -> None:
        self.path = path
        self.base_url = base_url
        self.error_handlers: t.Dict[t.Type[Exception], t.Callable[[t.Any], t.Any]] = {}
        self.view_funcs: t.OrderedDict[str, t.Callable[..., t.Any]] = OrderedDict()
        self.uuid: UUID = uuid4()
        self.name: str = 'Flask-JSONRPC'
        self.version: str = JSONRPC_VERSION_DEFAULT
        self.describe = JSONRPCServiceDescriptor(self).describe

    @property
    def is_json(self: Self) -> bool:
        """Check if the mimetype indicates JSON data, either
        :mimetype:`application/json` or :mimetype:`application/*+json`.

        https://github.com/pallets/werkzeug/blob/master/src/werkzeug/wrappers/json.py#L54
        """
        mt = request.mimetype
        return mt in ('application/json', 'application/json-rpc', 'application/jsonrequest') or (
            mt.startswith('application/') and mt.endswith('+json')
        )

    def set_path(self: Self, path: str) -> None:
        self.path = path

    def set_base_url(self: Self, base_url: t.Optional[str]) -> None:
        self.base_url = base_url

    def register_error_handler(self: Self, exception: t.Type[Exception], fn: t.Callable[[t.Any], t.Any]) -> None:
        self.error_handlers[exception] = fn

    def register(self: Self, name: str, view_func: t.Callable[..., t.Any]) -> None:
        self.view_funcs[name] = view_func

    def dispatch_request(
        self: Self,
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        if not self.validate_request():
            raise ParseError(
                data={
                    'message': f'Invalid mime type for JSON: {request.mimetype}, '
                    'use header Content-Type: application/json'
                }
            ) from None

        json_data = self.to_json(request.data)
        if self.is_batch_request(json_data):
            return self.batch_dispatch(json_data)
        return self.handle_dispatch_except(json_data)

    def validate_request(self: Self) -> bool:
        if not self.is_json:
            current_app.logger.error('invalid mimetype')
            return False
        return True

    def to_json(self: Self, request_data: bytes) -> t.Any:  # noqa: ANN401
        try:
            return json.loads(request_data)
        except ValueError as e:
            current_app.logger.exception('invalid json: %s', request_data)
            raise ParseError(data={'message': f'Invalid JSON: {request_data!r}'}) from e

    def handle_view_func(self: Self, view_func: t.Callable[..., t.Any], params: t.Any) -> t.Any:  # noqa: ANN401
        view_func_params = getattr(view_func, 'jsonrpc_method_params', {})
        validate = getattr(view_func, 'jsonrpc_validate', settings.DEFAULT_JSONRPC_METHOD['VALIDATE'])
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

            sanitazed_params = {k: v for k, v in binded_params.items() if v is not None}
            resp_view = current_app.ensure_sync(view_func)(**sanitazed_params)

            # TODO: Enhance the checker to return the type
            view_fun_annotations = t.get_type_hints(view_func)
            view_fun_return: t.Optional[t.Any] = view_fun_annotations.pop('return', None)
            if validate and resp_view is not None and view_fun_return is None:
                resp_view_qn = qualified_name(resp_view)
                view_fun_return_qn = qualified_name(view_fun_return)
                raise TypeError(
                    f'return type of {resp_view_qn} must be a type; got {view_fun_return_qn} instead'
                ) from None

            return resp_view
        except TypeError as e:
            current_app.logger.exception('invalid type checked for: %s', view_func.__name__)
            raise InvalidParamsError(data={'message': str(e)}) from e

    def dispatch(
        self: Self, req_json: t.Dict[str, t.Any]
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        method_name = req_json['method']
        params = req_json.get('params', {})
        view_func = self.view_funcs.get(method_name)
        notification = getattr(view_func, 'jsonrpc_notification', settings.DEFAULT_JSONRPC_METHOD['NOTIFICATION'])
        if not view_func:
            raise MethodNotFoundError(data={'message': f'Method not found: {method_name}'}) from None

        if self.is_notification_request(req_json) and not notification:
            raise InvalidRequestError(
                data={
                    'message': f"The method {method_name!r} doesn't allow Notification "
                    "Request object (without an 'id' member)"
                }
            ) from None

        resp_view = self.handle_view_func(view_func, params)
        return self.make_response(req_json, resp_view)

    def _find_error_handler(self: Self, exc: Exception) -> t.Optional[t.Callable[[t.Any], t.Any]]:
        exc_class = type(exc)
        if not self.error_handlers:
            return None

        for cls in exc_class.__mro__:
            handler = self.error_handlers.get(cls)
            if handler is not None:
                return handler
        return None

    def handle_dispatch_except(
        self: Self, req_json: t.Dict[str, t.Any]
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        try:
            if not self.validate(req_json):
                raise InvalidRequestError(data={'message': f'Invalid JSON: {req_json!r}'}) from None
            return self.dispatch(req_json)
        except JSONRPCError as e:
            current_app.logger.exception('jsonrpc error')
            response = {
                'id': get(req_json, 'id'),
                'jsonrpc': get(req_json, 'jsonrpc', JSONRPC_VERSION_DEFAULT),
                'error': e.jsonrpc_format,
            }
            return response, e.status_code, JSONRPC_DEFAULT_HTTP_HEADERS
        except Exception as e:  # pylint: disable=W0703
            current_app.logger.exception('unexpected error')
            error_handler = self._find_error_handler(e)
            jsonrpc_error_data = (
                current_app.ensure_sync(error_handler)(e) if error_handler is not None else {'message': str(e)}
            )
            jsonrpc_error = ServerError(data=jsonrpc_error_data)
            response = {
                'id': get(req_json, 'id'),
                'jsonrpc': get(req_json, 'jsonrpc', JSONRPC_VERSION_DEFAULT),
                'error': jsonrpc_error.jsonrpc_format,
            }
            return response, jsonrpc_error.status_code, JSONRPC_DEFAULT_HTTP_HEADERS

    def batch_dispatch(
        self: Self, reqs_json: t.List[t.Dict[str, t.Any]]
    ) -> t.Tuple[t.List[t.Any], int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        if not reqs_json:
            raise InvalidRequestError(data={'message': 'Empty array'}) from None

        resp_views = []
        headers = Headers()
        status_code = JSONRPC_DEFAULT_HTTP_STATUS_CODE
        for rv, _, hdrs in (self.handle_dispatch_except(rq) for rq in reqs_json):
            headers.update([hdrs] if isinstance(hdrs, tuple) else hdrs)  # type: ignore
            if rv is None:
                continue
            resp_views.append(rv)
        if not resp_views:
            status_code = 204
        return resp_views, status_code, headers

    def validate(self: Self, req_json: t.Dict[str, t.Any]) -> bool:
        return isinstance(req_json, dict) and 'method' in req_json

    def unpack_tuple_returns(
        self: Self,
        resp_view: t.Any,  # noqa: ANN401
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        # https://github.com/pallets/flask/blob/d091bb00c0358e9f30006a064f3dbb671b99aeae/src/flask/app.py#L1981
        if isinstance(resp_view, tuple):
            len_resp_view = len(resp_view)

            # a 3-tuple is unpacked directly
            if len_resp_view == 3:
                rv, status_code, headers = resp_view
            # decide if a 2-tuple has status or headers
            elif len_resp_view == 2:
                if isinstance(resp_view[1], (Headers, dict, tuple, list)):
                    rv, headers, status_code = resp_view + (JSONRPC_DEFAULT_HTTP_STATUS_CODE,)
                else:
                    rv, status_code, headers = resp_view + (JSONRPC_DEFAULT_HTTP_HEADERS,)
            # other sized tuples are not allowed
            else:
                raise TypeError(
                    'the view function did not return a valid response tuple.'
                    ' The tuple must have the form (body, status, headers),'
                    ' (body, status), or (body, headers).'
                ) from None
            return rv, status_code, headers

        return resp_view, JSONRPC_DEFAULT_HTTP_STATUS_CODE, JSONRPC_DEFAULT_HTTP_HEADERS

    def make_response(
        self: Self,
        req_json: t.Dict[str, t.Any],
        resp_view: t.Any,  # noqa: ANN401
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        rv, status_code, headers = self.unpack_tuple_returns(resp_view)
        if self.is_notification_request(req_json):
            return None, 204, headers
        resp = {'id': req_json.get('id'), 'jsonrpc': req_json.get('jsonrpc', JSONRPC_VERSION_DEFAULT), 'result': rv}
        return resp, status_code, headers

    def is_notification_request(self: Self, req_json: t.Dict[str, t.Any]) -> bool:
        return 'id' not in req_json

    def is_batch_request(self: Self, req_json: t.Any) -> bool:  # noqa: ANN401
        return isinstance(req_json, list)
