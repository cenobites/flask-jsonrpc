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
from uuid import UUID, uuid4

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

# Python 3.8+
try:
    from typing_extensions import TypedDict
except ImportError:  # pragma: no cover
    from typing import TypedDict  # pylint: disable=C0412

ServiceProcedureDescribe = TypedDict(
    'ServiceProcedureDescribe',
    {
        'name': str,
        'summary': t.Optional[str],
        'params': t.List[t.Dict[str, str]],
        'return': t.Dict[str, str],
    },
)


class ServiceDescribe(TypedDict):
    id: str
    sdversion: str
    version: str
    name: str
    summary: t.Optional[str]
    procs: t.List[ServiceProcedureDescribe]  # pytype: disable=invalid-annotation


JSONRPC_VERSION_DEFAULT: str = '2.0'
JSONRCP_DESCRIBE_METHOD_NAME: str = 'system.describe'
JSONRPC_DEFAULT_HTTP_HEADERS: t.Dict[str, str] = {}
JSONRPC_DEFAULT_HTTP_STATUS_CODE: int = 200


class JSONRPCSite:
    def __init__(self) -> None:
        self.view_funcs: t.Dict[str, t.Callable[..., t.Any]] = {}
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
        return mt in ('application/json', 'application/json-rpc', 'application/jsonrequest') or (
            mt.startswith('application/') and mt.endswith('+json')
        )

    def register(self, name: str, view_func: t.Callable[..., t.Any]) -> None:
        self.view_funcs[name] = view_func

    def dispatch_request(
        self,
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        if not self.validate_request():
            raise ParseError(
                data={
                    'message': f'Invalid mime type for JSON: {request.mimetype}, '
                    'use header Content-Type: application/json'
                }
            )

        json_data = self.to_json(request.data)
        if self.is_batch_request(json_data):
            return self.batch_dispatch(json_data)
        return self.handle_dispatch_except(json_data)

    def validate_request(self) -> bool:
        if not self.is_json:
            current_app.logger.error('invalid mimetype')
            return False
        return True

    def to_json(self, request_data: bytes) -> t.Any:
        try:
            return json.loads(request_data)
        except ValueError as e:
            current_app.logger.exception('invalid json: %s', request_data)
            raise ParseError(data={'message': f'Invalid JSON: {request_data!r}'}) from e

    def handle_dispatch_except(
        self, req_json: t.Dict[str, t.Any]
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        try:
            if not self.validate(req_json):
                raise InvalidRequestError(data={'message': f'Invalid JSON: {req_json!r}'})
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
            jsonrpc_error = ServerError(data={'message': str(e)})
            response = {
                'id': get(req_json, 'id'),
                'jsonrpc': get(req_json, 'jsonrpc', JSONRPC_VERSION_DEFAULT),
                'error': jsonrpc_error.jsonrpc_format,
            }
            return response, jsonrpc_error.status_code, JSONRPC_DEFAULT_HTTP_HEADERS

    def batch_dispatch(
        self, reqs_json: t.List[t.Dict[str, t.Any]]
    ) -> t.Tuple[t.List[t.Any], int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        if not reqs_json:
            raise InvalidRequestError(data={'message': 'Empty array'})

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

    def dispatch(
        self, req_json: t.Dict[str, t.Any]
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        params = req_json.get('params', {})
        view_func = self.view_funcs.get(req_json['method'])
        if not view_func:
            raise MethodNotFoundError(data={'message': f"Method not found: {req_json['method']}"})

        try:
            if isinstance(params, (tuple, set, list)):
                resp_view = current_app.ensure_sync(view_func)(*params)
            elif isinstance(params, dict):
                resp_view = current_app.ensure_sync(view_func)(**params)
            else:
                raise InvalidParamsError(
                    data={
                        'message': 'Parameter structures are by-position '
                        f'(tuple, set, list) or by-name (dict): {params}'
                    }
                )

            # TODO: Improve the checker to return type
            view_fun_annotations = t.get_type_hints(view_func)
            view_fun_return: t.Optional[t.Any] = view_fun_annotations.pop('return', None)
            if resp_view is not None and view_fun_return is None:
                resp_view_qn = qualified_name(resp_view)
                view_fun_return_qn = qualified_name(view_fun_return)
                raise TypeError(f'return type of {resp_view_qn} must be a type; got {view_fun_return_qn} instead')
        except TypeError as e:
            current_app.logger.exception('invalid type checked for: %s', view_func.__name__)
            raise InvalidParamsError(data={'message': str(e)}) from e

        return self.make_response(req_json, resp_view)

    def validate(self, req_json: t.Dict[str, t.Any]) -> bool:
        if not isinstance(req_json, dict) or 'method' not in req_json:
            return False
        return True

    def unpack_tuple_returns(
        self, resp_view: t.Any
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
                )
            return rv, status_code, headers

        return resp_view, JSONRPC_DEFAULT_HTTP_STATUS_CODE, JSONRPC_DEFAULT_HTTP_HEADERS

    def make_response(
        self, req_json: t.Dict[str, t.Any], resp_view: t.Any
    ) -> t.Tuple[t.Any, int, t.Union[Headers, t.Dict[str, str], t.Tuple[str], t.List[t.Tuple[str]]]]:
        rv, status_code, headers = self.unpack_tuple_returns(resp_view)
        if self.is_notification_request(req_json):
            return None, 204, headers
        resp = {'id': req_json.get('id'), 'jsonrpc': req_json.get('jsonrpc', JSONRPC_VERSION_DEFAULT), 'result': rv}
        return resp, status_code, headers

    def is_notification_request(self, req_json: t.Dict[str, t.Any]) -> bool:
        return 'id' not in req_json

    def is_batch_request(self, req_json: t.Any) -> bool:
        return isinstance(req_json, list)

    def python_type_name(self, pytype: t.Any) -> str:
        return str(from_python_type(pytype))

    def procedure_desc(self, key: str) -> ServiceProcedureDescribe:  # pytype: disable=invalid-annotation
        view_func = self.view_funcs[key]
        return {
            'name': getattr(view_func, 'jsonrpc_method_name', key),
            'summary': getattr(view_func, '__doc__', None),
            'params': [
                {'name': k, 'type': self.python_type_name(t)}
                for k, t in getattr(view_func, 'jsonrpc_method_params', {}).items()
            ],
            'return': {'type': self.python_type_name(getattr(view_func, 'jsonrpc_method_return', type(None)))},
        }

    def service_desc(self) -> ServiceDescribe:
        return ServiceDescribe(
            sdversion='1.0',
            id=f'urn:uuid:{self.uuid}',
            version=self.version,
            name=self.name,
            summary=self.__doc__,
            procs=[self.procedure_desc(k) for k in self.view_funcs if k != JSONRCP_DESCRIBE_METHOD_NAME],
        )

    def describe(self) -> ServiceDescribe:
        return self.service_desc()
