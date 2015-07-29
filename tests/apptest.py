# -*- coding: utf-8 -*-
# Copyright (c) 2012-2015, Cenobit Technologies, Inc. http://cenobit.es/
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
from __future__ import unicode_literals, absolute_import
import os
import sys
import time
import argparse
import unittest
import subprocess

from flask import Flask

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(os.path.dirname(os.path.realpath(__file__)))
FLASK_JSONRPC_PROJECT_DIR = os.path.join(PROJECT_DIR)
if os.path.exists(FLASK_JSONRPC_PROJECT_DIR) and not FLASK_JSONRPC_PROJECT_DIR in sys.path:
    sys.path.append(FLASK_JSONRPC_PROJECT_DIR)

from flask_jsonrpc import JSONRPC

from appserver import flask_server

SERVER_HOSTNAME = 'localhost'
SERVER_PORT = 5001

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = True
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

def check_auth(username, password):
    return True

@jsonrpc.method('jsonrpc.echo')
def echo(name='Flask JSON-RPC'):
    return 'Hello {0}'.format(name)

@jsonrpc.method('jsonrpc.echoMyStr')
def echoMyStr(string):
    return string

@jsonrpc.method('jsonrpc.echoAuth', authenticated=check_auth)
def echoAuth(string):
    return string

@jsonrpc.method('jsonrpc.echoAuthChecked(string=str) -> str', authenticated=check_auth, validate=True)
def echoAuthChecked(string):
    return string

@jsonrpc.method('jsonrpc.notify')
def notify(string):
    pass

@jsonrpc.method('jsonrpc.fails')
def fails(string):
    raise IndexError

@jsonrpc.method('jsonrpc.strangeEcho')
def strangeEcho(string, omg, wtf, nowai, yeswai='Default'):
    return [string, omg, wtf, nowai, yeswai]

@jsonrpc.method('jsonrpc.safeEcho', safe=True)
def safeEcho(string):
    return string

@jsonrpc.method('jsonrpc.strangeSafeEcho', safe=True)
def strangeSafeEcho(*args, **kwargs):
    return strangeEcho(*args, **kwargs)

@jsonrpc.method('jsonrpc.checkedEcho(string=str, string2=str) -> str', safe=True, validate=True)
def protectedEcho(string, string2):
    return string + string2

@jsonrpc.method('jsonrpc.checkedArgsEcho(string=str, string2=str)', validate=True)
def protectedArgsEcho(string, string2):
    return string + string2

@jsonrpc.method('jsonrpc.checkedReturnEcho() -> String', validate=True)
def protectedReturnEcho():
    return 'this is a string'

@jsonrpc.method('jsonrpc.authCheckedEcho(Object, Array) -> Object', validate=True)
def authCheckedEcho(obj1, arr1):
    return {'obj1': obj1, 'arr1': arr1}

@jsonrpc.method('jsonrpc.varArgs(String, String, str3=String) -> Array', validate=True)
def checkedVarArgsEcho(*args, **kw):
    return list(args) + list(kw.values())


class ServerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.service_url = 'http://{0}:{1}/api'.format(SERVER_HOSTNAME, SERVER_PORT)
        cls.server_process = flask_server.run()

    @classmethod
    def tearDownClass(cls):
        try:
            flask_server.kill(process=cls.server_process)
        except OSError:
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run',
        action='store_true', dest='run', default=False,
        help='Running Flask in subprocess')
    options = parser.parse_args()
    if options.run:
        return app.run(host=SERVER_HOSTNAME, port=SERVER_PORT)

if __name__ == '__main__':
    main()
