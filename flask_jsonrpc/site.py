# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013, Cenobit Technologies, Inc. http://cenobit.es/
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
import re
import decimal
import datetime
from uuid import uuid1
from functools import wraps

from werkzeug.exceptions import HTTPException

from flask import json, jsonify, current_app, got_request_exception

from flask_jsonrpc.types import Object, Array, Any
from flask_jsonrpc.helpers import extract_raw_data_request, log_exception
from flask_jsonrpc._compat import (text_type, string_types, integer_types,
                                   iteritems, iterkeys)
from flask_jsonrpc.exceptions import (Error, ParseError, InvalidRequestError,
                                      MethodNotFoundError, InvalidParamsError,
                                      ServerError, RequestPostError,
                                      InvalidCredentialsError, OtherError)

empty_dec = lambda f: f
try:
    # TODO: Add CSRF check
    csrf_exempt = empty_dec
except (NameError, ImportError):
    csrf_exempt = empty_dec

NoneType = type(None)
encode_kw = lambda p: dict([(text_type(k), v) for k, v in iteritems(p)])

def encode_kw11(p):
    if not type(p) is dict:
        return {}
    ret = p.copy()
    removes = []
    for k, v in iteritems(ret):
        try:
            int(k)
        except ValueError:
            pass
        else:
            removes.append(k)
    for k in removes:
        ret.pop(k)
    return ret

def encode_arg11(p):
    if type(p) is list:
        return p
    elif not type(p) is dict:
        return []
    else:
        pos = []
        d = encode_kw(p)
        for k, v in iteritems(d):
            try:
                pos.append(int(k))
            except ValueError:
                pass
        pos = list(set(pos))
        pos.sort()
        return [d[text_type(i)] for i in pos]

def validate_params(method, D):
    if type(D['params']) == Object:
        keys = method.json_arg_types.keys()
        if len(keys) != len(D['params']):
            raise InvalidParamsError('Not eough params provided for {0}' \
                .format(method.json_sig))
        for k in keys:
            if not k in D['params']:
                raise InvalidParamsError('{0} is not a valid parameter for {1}' \
                    .format(k, method.json_sig))
            if not Any.kind(D['params'][k]) == method.json_arg_types[k]:
                raise InvalidParamsError('{0} is not the correct type {1} for {2}' \
                    .format(type(D['params'][k]), method.json_arg_types[k], method.json_sig))
    elif type(D['params']) == Array:
        arg_types = list(method.json_arg_types.values())
        try:
            for i, arg in enumerate(D['params']):
                if not Any.kind(arg) == arg_types[i]:
                    raise InvalidParamsError('{0} is not the correct type {1} for {2}' \
                        .format(type(arg), arg_types[i], method.json_sig))
        except IndexError:
            raise InvalidParamsError('Too many params provided for {0}'.format(method.json_sig))
        else:
            if len(D['params']) != len(arg_types):
                raise InvalidParamsError('Not enouh params provided for {0}'.format(method.json_sig))


class JSONRPCSite(object):
    """A JSON-RPC Site
    """

    def __init__(self):
        self.urls = {}
        self.uuid = text_type(uuid1())
        self.version = '1.0'
        self.name = 'Flask-JSONRPC'
        self.register('system.describe', self.describe)

    def register(self, name, method):
        self.urls[text_type(name)] = method

    def extract_id_request(self, raw_data):
        if not raw_data is None and raw_data.find('id') != -1:
            find_id = re.findall(r'["|\']id["|\']:([0-9]+)|["|\']id["|\']:["|\'](.+?)["|\']',
                                 raw_data.replace(' ', ''), re.U)
            if find_id:
                g1, g2 = find_id[0]
                return g1 if g1 else g2
        return None

    def empty_response(self, version='1.0'):
        resp = {'id': None}
        if version == '1.1':
            resp['version'] = version
            return resp
        if version == '2.0':
            resp['jsonrpc'] = version
        resp.update({'error': None, 'result': None})
        return resp

    def validate_get(self, request, method):
        encode_get_params = lambda r: dict([(k, v[0] if len(v) == 1 else v) for k, v in r])
        if request.method == 'GET':
            method = text_type(method)
            if method in self.urls and getattr(self.urls[method], 'json_safe', False):
                D = {
                    'params': request.args.to_dict(),
                    'method': method,
                    'id': 'jsonrpc',
                    'version': '1.1'
                }
                return True, D
        return False, {}

    def response_dict(self, request, D, is_batch=False, version_hint='1.0'):
        version = version_hint
        response = self.empty_response(version=version)
        apply_version = {
            '2.0': lambda f, p: f(**encode_kw(p)) if type(p) is dict else f(*p),
            '1.1': lambda f, p: f(*encode_arg11(p), **encode_kw(encode_kw11(p))),
            '1.0': lambda f, p: f(*p)
        }

        try:
            # params: An Array or Object, that holds the actual parameter values
            # for the invocation of the procedure. Can be omitted if empty.
            if 'params' not in D or not D['params']:
                 D['params'] = []
            if 'method' not in D or 'params' not in D:
                raise InvalidParamsError('Request requires str:"method" and list:"params"')
            if D['method'] not in self.urls:
                raise MethodNotFoundError('Method not found. Available methods: {0}' \
                    .format('\n'.join(list(self.urls.keys()))))

            if 'jsonrpc' in D:
                if text_type(D['jsonrpc']) not in apply_version:
                    raise InvalidRequestError('JSON-RPC version {0} not supported.'.format(D['jsonrpc']))
                version = request.jsonrpc_version = response['jsonrpc'] = text_type(D['jsonrpc'])
            elif 'version' in D:
                if text_type(D['version']) not in apply_version:
                    raise InvalidRequestError('JSON-RPC version {0} not supported.'.format(D['version']))
                version = request.jsonrpc_version = response['version'] = text_type(D['version'])
            else:
                request.jsonrpc_version = '1.0'

            method = self.urls[text_type(D['method'])]
            if getattr(method, 'json_validate', False):
                validate_params(method, D)

            if 'id' in D and D['id'] is not None: # regular request
                response['id'] = D['id']
                if version in ('1.1', '2.0') and 'error' in response:
                    response.pop('error')
            elif is_batch: # notification, not ok in a batch format, but happened anyway
                raise InvalidRequestError
            else: # notification
                return None, 204

            R = apply_version[version](method, D['params'])

            if 'id' not in D or ('id' in D and D['id'] is None): # notification
                return None, 204

            encoder = current_app.json_encoder()

            # type of `R` should be one of these or...
            if not sum([isinstance(R, e) for e in \
                    string_types + integer_types + (dict, list, set, NoneType, bool)]):
                try:
                    rs = encoder.default(R) # ...or something this thing supports
                except TypeError as exc:
                    raise TypeError("Return type not supported, for {0!r}".format(R))

            response['result'] = R

            status = 200

        except Error as e:
            # exception missed by others
            #got_request_exception.connect(log_exception, current_app._get_current_object())

            response['error'] = e.json_rpc_format
            if version in ('1.1', '2.0') and 'result' in response:
                response.pop('result')
            status = e.status
        except HTTPException as e:
            # exception missed by others
            #got_request_exception.connect(log_exception, current_app._get_current_object())

            other_error = OtherError(e)
            response['error'] = other_error.json_rpc_format
            response['error']['code'] = e.code
            if version in ('1.1', '2.0') and 'result' in response:
                response.pop('result')
            status = e.code
        except Exception as e:
            # exception missed by others
            #got_request_exception.connect(log_exception, current_app._get_current_object())

            other_error = OtherError(e)
            response['error'] = other_error.json_rpc_format
            status = other_error.status
            if version in ('1.1', '2.0') and 'result' in response:
                response.pop('result')

        # Exactly one of result or error MUST be specified. It's not
        # allowed to specify both or none.
        if version in ('1.1', '2.0') and 'error' in response and not response['error']:
            response.pop('error')

        return response, status

    @csrf_exempt
    def dispatch(self, request, method=''):
        # in case we do something json doesn't like, we always get back valid
        # json-rpc response
        response = self.empty_response()
        raw_data = extract_raw_data_request(request)

        try:
            if request.method == 'GET':
                valid, D = self.validate_get(request, method)
                if not valid:
                    raise InvalidRequestError('The method you are trying to access is '
                                              'not availble by GET requests')
            elif not request.method == 'POST':
                raise RequestPostError
            else:
                try:
                    D = json.loads(raw_data)
                except Exception as e:
                    raise InvalidRequestError(e.message)

            if type(D) is list:
                response = [self.response_dict(request, d, is_batch=True)[0] for d in D]
                status = 200
            else:
                response, status = self.response_dict(request, D)
                if response is None and (not 'id' in D or D['id'] is None): # a notification
                    response = ''
                    return response, status
        except Error as e:
            #got_request_exception.connect(log_exception, current_app._get_current_object())

            response['error'] = e.json_rpc_format
            status = e.status
        except Exception as e:
            # exception missed by others
            #got_request_exception.connect(log_exception, current_app._get_current_object())

            other_error = OtherError(e)
            response['result'] = None
            response['error'] = other_error.json_rpc_format
            status = other_error.status

        # extract id the request
        json_request_id = self.extract_id_request(raw_data)
        response['id'] = json_request_id

        return response, status

    def procedure_desc(self, key):
        M = self.urls[key]
        return {
            'name': M.json_method,
            'summary': M.__doc__,
            'idempotent': M.json_safe,
            'params': [{'type': text_type(Any.kind(t)), 'name': k}
                for k, t in iteritems(M.json_arg_types)],
            'return': {'type': text_type(Any.kind(M.json_return_type))}}

    def service_desc(self):
        return {
            'sdversion': '1.0',
            'name': self.name,
            'id': 'urn:uuid:{0}'.format(text_type(self.uuid)),
            'summary': self.__doc__,
            'version': self.version,
            'procs': [self.procedure_desc(k)
                for k in iterkeys(self.urls)
                    if self.urls[k] != self.describe]}

    def describe(self):
        return self.service_desc()


jsonrpc_site = JSONRPCSite()
