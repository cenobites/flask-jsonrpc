#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Cenobit Technologies, Inc. http://cenobit.es/
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
import sys
import time
import uuid
import unittest
import tempfile
import subprocess
from optparse import OptionParser

from flask import json

from flask_jsonrpc.proxy import ServiceProxy
from flask_jsonrpc.site import validate_params
from flask_jsonrpc import _parse_sig, OrderedDict, JSONRPC
from flask_jsonrpc.types import Any, Object, Number, Boolean, String, Array, Nil
from flask_jsonrpc.exceptions import (Error, ParseError, InvalidRequestError, 
                                      MethodNotFoundError, InvalidParamsError, 
                                      ServerError, RequestPostError,
                                      InvalidCredentialsError, OtherError)

from run import app, jsonrpc

SERVER_HOSTNAME = 'localhost'
SERVER_PORT = 5001

def check_auth(username, password):
    return True

@jsonrpc.method('jsonrpc.echo')
def echo(name='Flask JSON-RPC'):
    return 'Hello %s' % name

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
    return list(args) + kw.values()


class JSONRPCFunctionalTests(unittest.TestCase):

    def test_method_parser(self):
        working_sigs = [
            ('jsonrpc', 'jsonrpc', OrderedDict(), Any),
            ('jsonrpc.methodName', 'jsonrpc.methodName', OrderedDict(), Any),
            ('jsonrpc.methodName() -> list', 'jsonrpc.methodName', OrderedDict(), list),
            ('jsonrpc.methodName(str, str, str ) ', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str), ('c', str)]), Any),
            ('jsonrpc.methodName(str, b=str, c=str)', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str), ('c', str)]), Any),
            ('jsonrpc.methodName(str, b=str) -> dict', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str)]), dict),
            ('jsonrpc.methodName(str, str, c=Any) -> Any', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str), ('c', Any)]), Any),
            ('jsonrpc(Any ) -> Any', 'jsonrpc', OrderedDict([('a', Any)]), Any),
        ]
        error_sigs = [
            ('jsonrpc(str) -> nowai', ValueError),
            ('jsonrpc(nowai) -> Any', ValueError),
            ('jsonrpc(nowai=str, str)', ValueError),
            ('jsonrpc.methodName(nowai*str) -> Any', ValueError)
        ]
        for sig in working_sigs:
            ret = _parse_sig(sig[0], list(iter(sig[2])))
            self.assertEquals(ret[0], sig[1])
            self.assertEquals(ret[1], sig[2])
            self.assertEquals(ret[2], sig[3])
        for sig in error_sigs:
            e = None
            try:
                _parse_sig(sig[0], ['a'])
            except Exception, exc:
                e = exc
            self.assert_(type(e) is sig[1])
  
    def test_validate_args(self):
        sig = 'jsonrpc(String, String) -> String'
        M = jsonrpc.method(sig, validate=True)(lambda s1, s2: s1+s2)
        self.assert_(validate_params(M, {'params': ['omg', u'wtf']}) is None)
        
        E = None
        try:
            validate_params(M, {'params': [['omg'], ['wtf']]})
        except Exception, e:
            E = e
        self.assert_(type(E) is InvalidParamsError)
  
    def test_validate_args_any(self):
        sig = 'jsonrpc(s1=Any, s2=Any)'
        M = jsonrpc.method(sig, validate=True)(lambda s1, s2: s1+s2)
        self.assert_(validate_params(M, {'params': ['omg', 'wtf']}) is None)
        self.assert_(validate_params(M, {'params': [['omg'], ['wtf']]}) is None)
        self.assert_(validate_params(M, {'params': {'s1': 'omg', 's2': 'wtf'}}) is None)
  
    def test_types(self):
        assert type(u'') == String
        assert type('') == String
        assert not type('') == Object
        assert not type([]) == Object
        assert type([]) == Array
        assert type('') == Any
        assert Any.kind('') == String
        assert Any.decode('str') == String
        assert Any.kind({}) == Object
        assert Any.kind(None) == Nil


class ServiceProxyTestCase(unittest.TestCase):
    
    def setUp(self):
        self.service_url = 'http://%s:%s/api' % (SERVER_HOSTNAME, SERVER_PORT)
        
    def tearDown(self):
        pass

    def test_positional_args(self):
        proxy = ServiceProxy(self.service_url)
        self.assert_(proxy.jsonrpc.echo()[u'result'] == 'Hello Flask JSON-RPC')
        try:
            proxy.jsonrpc.echo(name='Hello')
        except Exception, e:
            self.assert_(e.args[0] == 'Unsupported arg type for JSON-RPC 1.0 '
                                      '(the default version for this client, '
                                      'pass version="2.0" to use keyword arguments)')
  
    def test_keyword_args(self):
        proxy = ServiceProxy(self.service_url, version='2.0')
        self.assert_(proxy.jsonrpc.echo(name='Flask')[u'result'] == 'Hello Flask')
        self.assert_(proxy.jsonrpc.echo('JSON-RPC')[u'result'] == 'Hello JSON-RPC')


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
        assert st == resp, '%s != %s' % (st, resp)
    
    def test_echo(self):
        T = [[
            (self._make_payload('jsonrpc.echo', version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', ['Flask'], version=v), 'Hello Flask'),
            (self._make_payload('jsonrpc.echo', None, version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', [], version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', {}, version=v), 'Hello Flask JSON-RPC'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_my_str(self):
        T = [[
            (self._make_payload('jsonrpc.echoMyStr', ['Hello Flask JSON-RPC'], version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', ['Hello Flask'], version=v), 'Hello Flask'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_auth(self):
        T = [[
            (self._make_payload('jsonrpc.echoAuth', ['username', 'password', 'Hello Flask JSON-RPC'], version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoAuth', ['username', 'password', 'Hello Flask'], version=v), 'Hello Flask'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_auth_checked(self):
        T = [[
            (self._make_payload('jsonrpc.echoAuthChecked', {'username': 'flask', 'password': 'jsonrpc', 'string': 'Hello Flask JSON-RPC'}, version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoAuthChecked', {'username': 'flask', 'password': 'jsonrpc', 'string': 'Hello Flask'}, version=v), 'Hello Flask'),
        ] for v in ['1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_notify(self):
        T = [[
            (self._make_payload('jsonrpc.notify', ['this is a string'], version=v, is_notify=True), ''),
        ] for v in ['2.0']]
        [[self._assert_equals((self.app.post(self.service_url, data=req)).data, resp) for req, resp in t] for t in T]
        
    def test_strangeEcho(self):
        T = [
            (self._make_payload('jsonrpc.strangeEcho', {u'1': u'this is a string', u'2': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version='1.0'), ['1', '2', 'wtf', 'nowai', 'Default']),
            (self._make_payload('jsonrpc.strangeEcho', {u'1': u'this is a string', u'2': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version='1.1'), [u'this is a string', u'this is omg', u'pants', u'nopants', u'Default']),
            (self._make_payload('jsonrpc.strangeEcho', {u'string': u'this is a string', u'omg': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version='2.0'), [u'this is a string', u'this is omg', u'pants', u'nopants', u'Default']),
        ]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in T]
        
    def test_safeEcho(self):
        T = [[
            (self._make_payload('jsonrpc.safeEcho', [u'this is string'], version=v), 'this is string'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
        
    def test_strangeSafeEcho(self):
        T = [
            (self._make_payload('jsonrpc.strangeSafeEcho', {u'1': u'this is a string', u'2': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version='1.0'), ['1', '2', 'wtf', 'nowai', 'Default']),
            (self._make_payload('jsonrpc.strangeSafeEcho', {u'1': u'this is a string', u'2': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version='1.1'), [u'this is a string', u'this is omg', u'pants', u'nopants', u'Default']),
            (self._make_payload('jsonrpc.strangeSafeEcho', {u'string': u'this is a string', u'omg': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version='2.0'), [u'this is a string', u'this is omg', u'pants', u'nopants', u'Default']),
        ]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in T]
        
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


class FlaskTestClient(object):
    proc = None

    def __enter__(self):
        return self._run()

    def __exit__(self, type, value, traceback):
        self._kill()

    def _run(self):
        if FlaskTestClient.proc is None:
            FlaskTestClient.proc = subprocess.Popen([sys.executable, 
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                    'flask_jsonrpc_tests.py'), '--run'])
            time.sleep(1)
        return FlaskTestClient.proc

    def _kill(self):
        if not FlaskTestClient.proc is None \
                and not FlaskTestClient.proc.poll() is None:
            FlaskTestClient.proc.wait()
            FlaskTestClient.proc.terminate()
            time.sleep(1)
            if not FlaskTestClient.proc.poll() is None:
                FlaskTestClient.proc.kill()

def main():
    parser = OptionParser(usage='usage: %prog [options]')
    parser.add_option('-r', '--run',
        action='store_true', dest='run', default=False,
        help='Running Flask in subprocess')

    (options, args) = parser.parse_args()
    if options.run:
        return app.run(host=SERVER_HOSTNAME, port=SERVER_PORT)

    with FlaskTestClient():
        unittest.main()

if __name__ == '__main__':
    main()