# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
from functools import wraps

from flask import current_app, request, jsonify, json

from flask_jsonrpc.exceptions import InvalidCredentialsError, InvalidParamsError

def jsonify_status_code(status_code, *args, **kw):
    """Returns a jsonified response with the specified HTTP status code.

    The positional and keyword arguments are passed directly to the
    :func:`flask.jsonify` function which creates the response.

    """
    response = jsonify(*args, **kw)
    response.status_code = status_code
    return response

def extract_raw_data_request(request):
    if request.method == 'GET':
        return request.query_string
    elif request.method == 'POST':
        # True if the request was triggered via a JavaScript 
        # XMLHttpRequest
        if request.is_xhr:
            return json.dumps(request.form.to_dict())
        elif request.data:
            return request.data
        elif request.form.to_dict():
            return request.form.to_dict().keys()[0]
    return ''

def authenticate(f, f_check_auth):
    @wraps(f)
    def _f(*args, **kwargs):
        is_auth = False
        try:
            creds = args[:2]
            is_auth = f_check_auth(creds[0], creds[1])
            if is_auth:
                args = args[2:]
        except IndexError:
            if 'username' in kwargs and 'password' in kwargs:
                is_auth = f_check_auth(kwargs['username'], kwargs['password'])
                if is_auth:
                    kwargs.pop('username')
                    kwargs.pop('password')
            else:
                raise InvalidParamsError('Authenticated methods require at least '
                                         '[username, password] or {username: password:} arguments')
        if not is_auth:
            raise InvalidCredentialsError()
        return f(*args, **kwargs)
    return _f

def log_exception(sender, exception, **extra):
    sender.logger.debug('Got exception during processing: %s', exception)