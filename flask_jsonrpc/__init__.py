# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
import re
import StringIO
from functools import wraps
from inspect import getargspec

from collections import OrderedDict

from flask import current_app, request, jsonify

from flask_jsonrpc.site import jsonrpc_site
from flask_jsonrpc.types import Object, Number, Boolean, String, Array, Nil, Any, Type
from flask_jsonrpc.helpers import jsonify_status_code, extract_raw_data_request, authenticate
from flask_jsonrpc.exceptions import (Error, ParseError, InvalidRequestError, 
                                      MethodNotFoundError, InvalidParamsError, 
                                      ServerError, RequestPostError,
                                      InvalidCredentialsError, OtherError)

default_site = jsonrpc_site
KWARG_RE = re.compile(
    r'\s*(?P<arg_name>[a-zA-Z0-9_]+)\s*=\s*(?P<arg_type>[a-zA-Z]+)\s*$')
SIG_RE = re.compile(
    r'\s*(?P<method_name>[a-zA-Z0-9._]+)\s*(\((?P<args_sig>[^)].*)?\)'
    r'\s*(\->\s*(?P<return_sig>.*))?)?\s*$')


class JSONRPCTypeCheckingUnavailable(Exception):
    pass

def _type_checking_available(sig='', validate=False):
    if not hasattr(type, '__eq__') and validate: # and False:
        raise JSONRPCTypeCheckingUnavailable(
            'Type checking is not available in your version of Python '
            'which is only available in Python 2.6 or later. Use Python 2.6 '
            'or later or disable type checking in %s' % sig)

def _validate_arg(value, expected):
    """Returns whether or not ``value`` is the ``expected`` type.
    """
    if type(value) == expected:
        return True
    return False

def _eval_arg_type(arg_type, T=Any, arg=None, sig=None):
    """Returns a type from a snippit of python source. Should normally be
    something just like 'str' or 'Object'.
    
        arg_type            the source to be evaluated
        T                         the default type
        arg                     context of where this type was extracted
        sig                     context from where the arg was extracted
    
    Returns a type or a Type
    """
    try:
        T = eval(arg_type)
    except Exception, e:
        raise ValueError('The type of %s could not be evaluated in %s for %s: %s' %
                                        (arg_type, arg, sig, str(e)))
    else:
        if type(T) not in (type, Type):
            raise TypeError('%s is not a valid type in %s for %s' %
                                            (repr(T), arg, sig))
        return T

def _parse_sig(sig, arg_names, validate=False):
    """Parses signatures into a ``OrderedDict`` of paramName => type.
    Numerically-indexed arguments that do not correspond to an argument
    name in python (ie: it takes a variable number of arguments) will be
    keyed as the stringified version of it's index.
    
        sig                 the signature to be parsed
        arg_names     a list of argument names extracted from python source
    
    Returns a tuple of (method name, types dict, return type)
    """
    d = SIG_RE.match(sig)
    if not d:
        raise ValueError('Invalid method signature %s' % sig)
    d = d.groupdict()
    ret = [(n, Any) for n in arg_names]
    if 'args_sig' in d and type(d['args_sig']) is str and d['args_sig'].strip():
        for i, arg in enumerate(d['args_sig'].strip().split(',')):
            _type_checking_available(sig, validate)
            if '=' in arg:
                if not type(ret) is OrderedDict:
                    ret = OrderedDict(ret)
                dk = KWARG_RE.match(arg)
                if not dk:
                    raise ValueError('Could not parse arg type %s in %s' % (arg, sig))
                dk = dk.groupdict()
                if not sum([(k in dk and type(dk[k]) is str and bool(dk[k].strip()))
                        for k in ('arg_name', 'arg_type')]):
                    raise ValueError('Invalid kwarg value %s in %s' % (arg, sig))
                ret[dk['arg_name']] = _eval_arg_type(dk['arg_type'], None, arg, sig)
            else:
                if type(ret) is OrderedDict:
                    raise ValueError('Positional arguments must occur '
                                     'before keyword arguments in %s' % sig)
                if len(ret) < i + 1:
                    ret.append((str(i), _eval_arg_type(arg, None, arg, sig)))
                else:
                    ret[i] = (ret[i][0], _eval_arg_type(arg, None, arg, sig))
    if not type(ret) is OrderedDict:
        ret = OrderedDict(ret)
    return (d['method_name'], 
                    ret, 
                    (_eval_arg_type(d['return_sig'], Any, 'return', sig)
                        if d['return_sig'] else Any))

def _inject_args(sig, types):
    """A function to inject arguments manually into a method signature before
    it's been parsed. If using keyword arguments use 'kw=type' instead in
    the types array.
        
        sig         the string signature
        types     a list of types to be inserted
        
    Returns the altered signature.
    """
    if '(' in sig:
        parts = sig.split('(')
        sig = '%s(%s%s%s' % (
            parts[0], ', '.join(types), 
            (', ' if parts[1].index(')') > 0 else ''), parts[1]
        )
    else:
        sig = '%s(%s)' % (sig, ', '.join(types))
    return sig

def _site_api(method=''):
    response_dict, status_code = default_site.dispatch(request, method)
    if current_app.config['DEBUG']:
        print('\n ++ data request')
        print('>> request: {}'.format(extract_raw_data_request(request)))
        print('<< response: {}, {}'.format(status_code, response_dict))
    return jsonify_status_code(status_code, response_dict), status_code


class JSONRPC(object):
    
    def __init__(self, app=None, service_url='/api', auth_backend=authenticate, site=default_site):
        self.service_url = service_url
        self.auth_backend = auth_backend
        self.site = site
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None
            
    def init_app(self, app):
        app.add_url_rule(self.service_url, '', _site_api, methods=['POST'])
        app.add_url_rule(self.service_url + '/<method>', '', _site_api, methods=['GET'])
        
    def register_blueprint(self, blueprint):
        blueprint.add_url_rule(self.service_url, '', _site_api, methods=['POST'])
        blueprint.add_url_rule(self.service_url + '/<method>', '', _site_api, methods=['GET'])
        
    def method(self, name, authenticated=False, safe=False, validate=False, **options):
        def decorator(f):
            arg_names = getargspec(f)[0][1:]
            X = {'name': name, 'arg_names': arg_names}
            if authenticated:
                # TODO: this is an assumption
                X['arg_names'] = ['username', 'password'] + X['arg_names']
                X['name'] = _inject_args(X['name'], ('String', 'String'))
                _f = self.auth_backend(f, authenticated)
            else:
                _f = f
            method, arg_types, return_type = _parse_sig(X['name'], X['arg_names'], validate)
            _f.json_args = X['arg_names']
            _f.json_arg_types = arg_types
            _f.json_return_type = return_type
            _f.json_method = method
            _f.json_safe = safe
            _f.json_sig = X['name']
            _f.json_validate = validate
            self.site.register(method, _f)
            return _f
        return decorator
