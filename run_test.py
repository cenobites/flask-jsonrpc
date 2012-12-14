#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
from flask import Flask, g, request, session
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api')

@jsonrpc.method('App.index')
def index():
    return 'Welcome to Flask JSON-RPC'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=0)