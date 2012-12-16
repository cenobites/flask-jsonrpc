#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
import os
import sys
from functools import wraps

from flask import Flask

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.realpath(__file__))
)

FLASK_JSONRPC_PROJECT_DIR = os.path.join(PROJECT_DIR, os.pardir)
if os.path.exists(FLASK_JSONRPC_PROJECT_DIR) \
        and not FLASK_JSONRPC_PROJECT_DIR in sys.path:
    sys.path.append(FLASK_JSONRPC_PROJECT_DIR)

from flask_jsonrpc import JSONRPC

app = Flask(__name__)

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

jsonrpc = JSONRPC(app, '/api', auth_backend=authenticate)

def check_auth(username, password):
    return True

@jsonrpc.method('app.index', authenticated=check_auth)
def index():
    return 'Welcome to Flask JSON-RPC'

@jsonrpc.method('app.echo(name=str)', authenticated=check_auth)
def echo(name=''):
    return 'Hello {}'.format(name)


if __name__ == '__main__':
    app.run()