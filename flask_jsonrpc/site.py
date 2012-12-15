# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
import re
import decimal
import datetime 
from uuid import uuid1
from functools import wraps

from flask import json, jsonify, current_app, got_request_exception

from flask_jsonrpc.helpers import extract_raw_data_request, log_exception
from flask_jsonrpc.types import Object, Array, Any
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
encode_kw = lambda p: dict([(str(k), v) for k, v in p.iteritems()])

def encode_kw11(p):
    if not type(p) is dict:
        return {}
    ret = p.copy()
    removes = []
    for k, v in ret.iteritems():
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
        for k, v in d.iteritems():
            try:
                pos.append(int(k))
            except ValueError:
                pass
        pos = list(set(pos))
        pos.sort()
        return [d[str(i)] for i in pos]

def validate_params(method, D):
    if type(D['params']) == Object:
        keys = method.json_arg_types.keys()
        if len(keys) != len(D['params']):
            raise InvalidParamsError('Not eough params provided for %s' % method.json_sig)
        for k in keys:
            if not k in D['params']:
                raise InvalidParamsError('%s is not a valid parameter for %s' 
                                         % (k, method.json_sig))
            if not Any.kind(D['params'][k]) == method.json_arg_types[k]:
                raise InvalidParamsError('%s is not the correct type %s for %s'
                    % (type(D['params'][k]), method.json_arg_types[k], method.json_sig))
    elif type(D['params']) == Array:
        arg_types = method.json_arg_types.values()
        try:
            for i, arg in enumerate(D['params']):
                if not Any.kind(arg) == arg_types[i]:
                    raise InvalidParamsError('%s is not the correct type %s for %s'
                                             % (type(arg), arg_types[i], method.json_sig))
        except IndexError:
            raise InvalidParamsError('Too many params provided for %s' % method.json_sig)
        else:
            if len(D['params']) != len(arg_types):
                raise InvalidParamsError('Not enouh params provided for %s' % method.json_sig)


class JSONRPCSite(object):
    """A JSON-RPC Site
    """
    
    def __init__(self):
        self.urls = {}
        self.uuid = str(uuid1())
        self.version = '1.0'
        self.name = 'Flask-JSONRPC'
        self.register('system.describe', self.describe)
        
    def register(self, name, method):
        self.urls[unicode(name)] = method

    def extract_id_request(self, raw_data):
        if not raw_data is None and raw_data.find('id') != -1:
            find_id = re.findall(r'["|\']id["|\']:([0-9])|["|\']id["|\']:["|\'](.+?)["|\']', 
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
            method = unicode(method)
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
            '2.0': lambda f, r, p: f(**encode_kw(p)) if type(p) is dict else f(*p),
            '1.1': lambda f, r, p: f(*encode_arg11(p), **encode_kw(encode_kw11(p))),
            '1.0': lambda f, r, p: f(*p)
        }
        
        try:
            # params: An Array or Object, that holds the actual parameter values 
            # for the invocation of the procedure. Can be omitted if empty.
            if 'params' not in D or not D['params']:
                 D['params'] = []
            if 'method' not in D or 'params' not in D:
                raise InvalidParamsError('Request requires str:"method" and list:"params"')
            if D['method'] not in self.urls:
                raise MethodNotFoundError('Method not found. Available methods: %s' % ('\n'.join(self.urls.keys())))
            
            if 'jsonrpc' in D:
                if str(D['jsonrpc']) not in apply_version:
                    raise InvalidRequestError('JSON-RPC version %s not supported.' % D['jsonrpc'])
                version = request.jsonrpc_version = response['jsonrpc'] = str(D['jsonrpc'])
            elif 'version' in D:
                if str(D['version']) not in apply_version:
                    raise InvalidRequestError('JSON-RPC version %s not supported.' % D['version'])
                version = request.jsonrpc_version = response['version'] = str(D['version'])
            else:
                request.jsonrpc_version = '1.0'
                
            method = self.urls[str(D['method'])]
            if getattr(method, 'json_validate', False):
                validate_params(method, D)
            R = apply_version[version](method, request, D['params'])
            
            encoder = json.JSONEncoder()
            if not sum(map(lambda e: isinstance(R, e), # type of `R` should be one of these or...
                 (dict, str, unicode, int, long, list, set, NoneType, bool))):
                try:
                    rs = encoder.default(R) # ...or something this thing supports
                except TypeError, exc:
                    raise TypeError("Return type not supported, for %r" % R)

            if 'id' in D and D['id'] is not None: # regular request
                response['result'] = R
                response['id'] = D['id']
                if version in ('1.1', '2.0') and 'error' in response:
                    response.pop('error')
            elif is_batch: # notification, not ok in a batch format, but happened anyway
                raise InvalidRequestError
            else: # notification
                return None, 204
            
            status = 200
        
        except Error, e:
            #got_request_exception.connect(log_exception, current_app._get_current_object())
            
            response['error'] = e.json_rpc_format
            if version in ('1.1', '2.0') and 'result' in response:
                response.pop('result')
            status = e.status
        except Exception, e:
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
                except:
                    raise InvalidRequestError
            
            if type(D) is list:
                response = [self.response_dict(request, d, is_batch=True)[0] for d in D]
                status = 200
            else:
                response, status = self.response_dict(request, D)
                if response is None and (not u'id' in D or D[u'id'] is None): # a notification
                    response = ''
                    return response, status
        except Error, e:
            #got_request_exception.connect(log_exception, current_app._get_current_object())

            response['error'] = e.json_rpc_format
            status = e.status
        except Exception, e:
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
            'params': [{'type': str(Any.kind(t)), 'name': k} 
                for k, t in M.json_arg_types.iteritems()],
            'return': {'type': M.json_return_type}}
    
    def service_desc(self):
        return {
            'sdversion': '1.0',
            'name': self.name,
            'id': 'urn:uuid:%s' % str(self.uuid),
            'summary': self.__doc__,
            'version': self.version,
            'procs': [self.procedure_desc(k) 
                for k in self.urls.iterkeys()
                    if self.urls[k] != self.describe]}
    
    def describe(self, request):
        return self.service_desc()


jsonrpc_site = JSONRPCSite()
