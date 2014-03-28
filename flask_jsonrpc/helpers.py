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
from functools import wraps

from flask import current_app, request, jsonify, json

from flask_jsonrpc._compat import b, u, text_type
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
    def _extract_raw_data_request(request):
        if request.method == 'GET':
            return request.query_string
        elif request.method == 'POST':
            if request.data:
                return request.data
            elif request.form.to_dict():
                return list(request.form.to_dict().keys())[0]
        return b('')
    raw_data = _extract_raw_data_request(request)

    tried_encodings = []

    # Try charset from content-type
    encoding = request.charset if request.charset else 'utf-8'

    if encoding:
        try:
            return text_type(raw_data, encoding)
        except UnicodeError:
            tried_encodings.append(encoding)

    # Fall back:
    try:
        return text_type(raw_data, encoding, errors='replace')
    except TypeError:
        return raw_data

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