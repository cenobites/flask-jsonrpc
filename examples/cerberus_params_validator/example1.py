#!/usr/bin/env python
# Copyright (c) 2022, Cenobit Technologies, Inc. http://cenobit.es/
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
from typing import Any, Dict

from flask import Flask
from cerberus import Validator

try:
    from flask_jsonrpc import JSONRPC
except ModuleNotFoundError:
    project_dir, project_module_name = os.path.split(os.path.dirname(os.path.realpath(__file__)))
    flask_jsonrpc_project_dir = os.path.join(project_dir, os.pardir, 'src')
    if os.path.exists(flask_jsonrpc_project_dir) and flask_jsonrpc_project_dir not in sys.path:
        sys.path.append(flask_jsonrpc_project_dir)

    from flask_jsonrpc import JSONRPC
from flask_jsonrpc.exceptions import InvalidParamsError

app = Flask('cerberus')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

v = Validator()
v.schema = {
    'user': {
        'type': 'dict',
        'schema': {
            'name': {'type': 'string', 'maxlength': 10},
            'age': {'type': 'integer', 'min': 10},
        },
    },
    'vehicle': {
        'type': 'dict',
        'schema': {
            'make': {'type': 'string'},
            'model': {'type': 'string'},
            'year': {'type': 'integer', 'min': 1900},
        },
    },
}


@jsonrpc.method('App.createUsers')
def create_users(user: Dict[str, Any]) -> Dict[str, Any]:
    if not v.validate({'user': {**user}}):
        raise InvalidParamsError(data={'message': v.errors})
    return {'created': True}


@jsonrpc.method('App.createVehicles')
def create_vehicles(vehicle: Dict[str, Any]) -> Dict[str, Any]:
    if not v.validate({'vehicle': {**vehicle}}):
        raise InvalidParamsError(data={'message': v.errors})
    return {'created': True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
