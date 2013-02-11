# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
from flask import Blueprint

from hrx import jsonrpc

mod = Blueprint('hello', __name__)
jsonrpc.register_blueprint(mod)

@jsonrpc.method('hello.index')
def index():
    return 'Welcome to Hello API!'

@jsonrpc.method('hello.say(name=String)')
def say(name=''):
    return 'Hello {0}!'.format(name)