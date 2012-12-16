#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
import os
import sys

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
jsonrpc = JSONRPC(app, '/api')

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