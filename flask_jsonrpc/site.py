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
from uuid import UUID, uuid4
from typing import Any, Dict, List, Type, Tuple, Union, TypeVar, Callable, get_type_hints
from concurrent.futures import ThreadPoolExecutor

from flask import json, request, current_app

from typeguard import qualified_name
from werkzeug.datastructures import Headers

from .helpers import get, from_python_type
from .exceptions import (
    ParseError,
    ServerError,
    JSONRPCError,
    InvalidParamsError,
    InvalidRequestError,
    MethodNotFoundError,
)

T = TypeVar('T')

JSONRPC_VERSION_DEFAULT: str = '2.0'
JSONRCP_DESCRIBE_METHOD_NAME: str = 'system.describe'
JSONRPC_DEFAULT_HTTP_HEADERS: Dict[str, str] = {}
JSONRPC_DEFAULT_HTTP_STATUS_CODE: int = 200


class JSONRPCSite:
    def __init__(self) -> None:
        self.view_funcs: Dict[str, Callable[..., Any]] = {}
        self.uuid: UUID = uuid4()
        self.name: str = 'Flask-JSONRPC'
        self.version: str = JSONRPC_VERSION_DEFAULT
        self.register(JSONRCP_DESCRIBE_METHOD_NAME, self.describe)

    @property
    def is_json(self) -> bool:
        """Check if the mimetype indicates JSON data, either
        :mimetype:`application/json` or :mimetype:`application/*+json`.

        https://github.com/pallets/werkzeug/blob/master/src/werkzeug/wrappers/json.py#L54
        """
        mt = request.mimetype
        return mt == 'application/json' or mt.startswith('application/') and mt.endswith('+json')

    def register(self, name: str, view_func: Callable[..., Any]) -> None:
        self.view_funcs[name] = view_func

    def dispatch_request(self) -> Tuple[Any, int, Union[Headers, Dict[str, str], Tuple[str], List[Tuple[str]]]]:
        if not self.validate_request():
            raise ParseError(
                data={
                    'message': 'Invalid mime type for JSON: {0}, use header Content-Type: application/json'.format(
                        request.mimetype
                    )
                }
            )

        json_data = self.to_json(request.data)
        if self.is_batch_request(json_data):
            return self.batch_dispatch(json_data)
        return self.handle_dispatch_except(json_data)

    def validate_request(self) -> bool:
        if not self.is_json:
            if current_app:
                current_app.logger.error('invalid mimetype')
            return False
        return True

    def to_json(self, request_data: bytes) -> Any:
        try:
            return json.loads(request_data)
        except ValueError as e:
            if current_app:
                current_app.logger.error('invalid json: %s', request_data)
                current_app.logger.exception(e)
            raise ParseError(data={'message': 'Invalid JSON: {0!r}'.format(request_data)})

    def handle_dispatch_except(
        self, req_json: Dict[str, Any]
    ) -> Tuple[Any, int, Union[Headers, Dict[str, str], Tuple[str], List[Tuple[str]]]]:
        try:
            if not self.validate(req_json):
                raise InvalidRequestError(data={'message': 'Invalid JSON: {0!r}'.format(req_json)})
            return self.dispatch(req_json)
        except JSONRPCError as e:
            if current_app:
                current_app.logger.error('jsonrpc error')
                current_app.logger.exception(e)
            response = {
                'id': get(req_json, 'id'),
                'jsonrpc': get(req_json, 'jsonrpc', JSONRPC_VERSION_DEFAULT),
                'error': e.jsonrpc_format,
            }
            return response, e.status_code, JSONRPC_DEFAULT_HTTP_HEADERS
        except Exception as e:  # pylint: disable=W0703
            if current_app:
                current_app.logger.error('unexpected error')
                current_app.logger.exception(e)
            jsonrpc_error = ServerError(data={'message': str(e)})
            response = {
                'id': get(req_json, 'id'),
                'jsonrpc': get(req_json, 'jsonrpc', JSONRPC_VERSION_DEFAULT),
                'error': jsonrpc_error.jsonrpc_format,
            }
            return response, jsonrpc_error.status_code, JSONRPC_DEFAULT_HTTP_HEADERS

    def batch_dispatch(
        self, reqs_json: List[Dict[str, Any]]
    ) -> Tuple[List[Any], int, Union[Headers, Dict[str, str], Tuple[str], List[Tuple[str]]]]:
        if not reqs_json:
            raise InvalidRequestError(data={'message': 'Empty array'})

        resp_views = []
        headers = Headers()
        status_code = JSONRPC_DEFAULT_HTTP_STATUS_CODE
        with ThreadPoolExecutor(max_workers=len(reqs_json) or 1) as executor:
            for rv, _, hdrs in executor.map(self.handle_dispatch_except, reqs_json):
                headers.update([hdrs] if isinstance(hdrs, tuple) else hdrs)  # type: ignore
                if rv is None:
                    continue
                resp_views.append(rv)
        if not resp_views:
            status_code = 204
        return resp_views, status_code, headers

    def dispatch(
        self, req_json: Dict[str, Any]
    ) -> Tuple[Any, int, Union[Headers, Dict[str, str], Tuple[str], List[Tuple[str]]]]:
        params = req_json.get('params', {})
        view_func = self.view_funcs.get(req_json['method'])
        if not view_func:
            raise MethodNotFoundError(data={'message': 'Method not found: {0}'.format(req_json['method'])})

        try:
            if isinstance(params, (tuple, set, list)):
                resp_view = view_func(*params)
            elif isinstance(params, dict):
                resp_view = view_func(**params)
            else:
                raise InvalidParamsError(
                    data={
                        'message': 'Parameter structures are by-position '
                        '(tuple, set, list) or by-name (dict): {0}'.format(params)
                    }
                )

            # TODO: Improve the checker to return type
            view_fun_annotations = get_type_hints(view_func)
            view_fun_return = view_fun_annotations.pop('return', None)
            if resp_view is not None and view_fun_return is None:
                raise TypeError(
                    'return type of {} must be a type; got {} instead'.format(
                        qualified_name(resp_view), qualified_name(view_fun_return)
                    )
                )
        except TypeError as e:
            if current_app:
                current_app.logger.error('invalid type checked for: %s', view_func.__name__)
                current_app.logger.exception(e)
            raise InvalidParamsError(data={'message': str(e)})

        return self.make_response(req_json, resp_view)

    def validate(self, req_json: Dict[str, Any]) -> bool:
        if not isinstance(req_json, dict) or 'method' not in req_json:
            return False
        return True

    def unpack_tuple_returns(
        self, resp_view: Any
    ) -> Tuple[Any, int, Union[Headers, Dict[str, str], Tuple[str], List[Tuple[str]]]]:
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
                )
            return rv, status_code, headers

        return resp_view, JSONRPC_DEFAULT_HTTP_STATUS_CODE, JSONRPC_DEFAULT_HTTP_HEADERS

    def make_response(
        self, req_json: Dict[str, Any], resp_view: Any
    ) -> Tuple[Any, int, Union[Headers, Dict[str, str], Tuple[str], List[Tuple[str]]]]:
        rv, status_code, headers = self.unpack_tuple_returns(resp_view)
        if self.is_notification_request(req_json):
            return None, 204, headers
        resp = {'id': req_json.get('id'), 'jsonrpc': req_json.get('jsonrpc', JSONRPC_VERSION_DEFAULT), 'result': rv}
        return resp, status_code, headers

    def is_notification_request(self, req_json: Dict[str, Any]) -> bool:
        return 'id' not in req_json

    def is_batch_request(self, req_json: Any) -> bool:
        return isinstance(req_json, list)

    def python_type_name(self, pytype: Type[T]) -> str:
        return str(from_python_type(pytype))

    def procedure_desc(self, key: str) -> Dict[str, Any]:
        view_func = self.view_funcs[key]
        return {
            'name': getattr(view_func, 'jsonrpc_method_name', None),
            'summary': getattr(view_func, '__doc__', None),
            'params': [
                {'name': k, 'type': self.python_type_name(t)}
                for k, t in getattr(view_func, 'jsonrpc_method_params', {}).items()
            ],
            'return': {'type': self.python_type_name(getattr(view_func, 'jsonrpc_method_return', None))},
        }

    def service_desc(self) -> Dict[str, Any]:
        return {
            'sdversion': '1.0',
            'id': 'urn:uuid:{0}'.format(self.uuid),
            'version': self.version,
            'name': self.name,
            'summary': self.__doc__,
            'procs': [self.procedure_desc(k) for k in self.view_funcs if k != JSONRCP_DESCRIBE_METHOD_NAME],
        }

    def describe(self) -> Dict[str, Any]:
        return self.service_desc()
