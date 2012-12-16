# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
from flask import Blueprint

from modular import jsonrpc

mod = Blueprint('article', __name__)
jsonrpc.register_blueprint(mod)

@jsonrpc.method('article.index')
def index():
    return 'Welcome to Article API'