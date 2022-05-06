#!/usr/bin/env python
# Copyright (c) 2012-2022, Cenobit Technologies, Inc. http://cenobit.es/
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
# isort:skip_file
import os
import sys
from typing import Any, Callable

from flask import Flask, request

try:
    from flask_jsonrpc import JSONRPC
except ModuleNotFoundError:
    project_dir, project_module_name = os.path.split(os.path.dirname(os.path.realpath(__file__)))
    flask_jsonrpc_project_dir = os.path.join(project_dir, os.pardir, 'src')
    if os.path.exists(flask_jsonrpc_project_dir) and flask_jsonrpc_project_dir not in sys.path:
        sys.path.append(flask_jsonrpc_project_dir)

    from flask_jsonrpc import JSONRPC

app = Flask('decorator')
jsonrpc = JSONRPC(app, '/api')


def check_terminal_id(fn: Callable[..., Any]):
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        terminal_id = int(request.get_json(silent=True).get('terminal_id', 0))
        if terminal_id <= 0:
            raise ValueError('Invalid terminal ID')
        rv = fn(*args, **kwargs)
        return rv

    return wrapped


def jsonrcp_headers(fn: Callable[..., Any]):
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        headers = {'X-JSONRPC-Tag': 'JSONRPC 2.0'}
        rv = fn(*args, **kwargs)
        return rv, 200, headers

    return wrapped


@jsonrpc.method('App.index')
@check_terminal_id
def index() -> str:
    terminal_id = request.get_json(silent=True).get('terminal_id', 0)
    return f'Terminal ID: {terminal_id}'


@jsonrpc.method('App.decorators')
@check_terminal_id
@jsonrcp_headers
def decorators() -> dict:
    return {'terminal_id': request.get_json(silent=True).get('terminal_id', 0), 'headers': str(request.headers)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
