#!/usr/bin/env python
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
import os
import uuid
import unittest
import tempfile

from flask import json

from flask_jsonrpc.proxy import ServiceProxy 
from run import app, jsonrpc

@jsonrpc.method('jsonrpc.echo')
def echo(name='Flask JSON-RPC'):
    return 'Hello {0}'.format(name)

@jsonrpc.method('jsonrpc.notify')
def notify(string):
    pass

@jsonrpc.method('jsonrpc.fails')
def fails(string):
    raise IndexError

@jsonrpc.method('jsonrpc.strangeEcho')
def strangeEcho(string, omg, wtf, nowai, yeswai='Default'):
    #  ['1', '2', 'wtf', 'nowai', 'Default'] != ['nowai', 'wtf', '2', '1', 'Default']
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


class FlaskJSONRPCTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.service_url = jsonrpc.service_url
        
    def tearDown(self):
        pass
    
    def _make_payload(self, method, params=None, version='1.0', is_notify=False):
        return json.dumps({
            'jsonrpc': version,
            'method': method,
            'params': params if params else [],
            'id': None if is_notify else str(uuid.uuid1())
        })
        
    def _call(self, req):
        return json.loads((self.app.post(self.service_url, data=req)).data)
    
    def _assert_equals(self, resp, st):
        assert st == resp, '{0} != {1}'.format(st, resp)
    
    def test_echo(self):
        T = [[
            (self._make_payload('jsonrpc.echo', version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', ['Flask'], version=v), 'Hello Flask'),
            (self._make_payload('jsonrpc.echo', None, version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', [], version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', {}, version=v), 'Hello Flask JSON-RPC'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_notify(self):
        T = [[
            (self._make_payload('jsonrpc.notify', ['this is a string'], version=v, is_notify=True), b''),
        ] for v in ['2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_strangeEcho(self):
        T = [[
            (self._make_payload('jsonrpc.strangeEcho', {'1': 'this is a string', '2': 'this is omg', 'wtf': 'pants', 'nowai': 'nopants'}, version=v), ['1', '2', 'wtf', 'nowai', 'Default']),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_safeEcho(self):
        T = [[
            (self._make_payload('jsonrpc.safeEcho', ['this is string'], version=v), 'this is string'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_strangeSafeEcho(self):
        T = [[
            (self._make_payload('jsonrpc.strangeSafeEcho', {'1': 'this is a string', '2': 'this is omg', 'wtf': 'pants', 'nowai': 'nopants'}, version=v), ['1', '2', 'wtf', 'nowai', 'Default']),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_protectedEcho(self):
        T = [[
            (self._make_payload('jsonrpc.checkedEcho', ['hai', 'hai'], version=v), 'haihai'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_protectedArgsEcho(self):
        T = [[
            (self._make_payload('jsonrpc.checkedArgsEcho', ['hai', 'hai'], version=v), 'haihai'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_protectedReturnEcho(self):
        T = [[
            (self._make_payload('jsonrpc.checkedReturnEcho', [], version=v), 'this is a string'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_authCheckedEcho(self):
        T = [[
            (self._make_payload('jsonrpc.authCheckedEcho', [1.0, [1,2,3]], version=v), {'obj1': 1.0, 'arr1': [1,2,3]}),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_checkedVarArgsEcho(self):
        T = [[
            (self._make_payload('jsonrpc.varArgs', ['hai', 'hai', ' -> \o/'], version=v), ['hai', 'hai', ' -> \o/']),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        

if __name__ == '__main__':
    unittest.main()