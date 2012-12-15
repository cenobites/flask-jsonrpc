#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
import os
import uuid
import unittest
import tempfile

from flask import json

from flask_jsonrpc.proxy import ServiceProxy 
from run import app, jsonrpc

@jsonrpc.method('jsonrpc.echo')
def echo(name='Flask JSON-RPC'):
    return 'Hello {}'.format(name)

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
        assert st == resp, '{} != {}'.format(st, resp)
    
    def test_echo(self):
        R = [[
            (self._make_payload('jsonrpc.echo', version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', ['Flask'], version=v), 'Hello Flask'),
            (self._make_payload('jsonrpc.echo', None, version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', [], version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', {}, version=v), 'Hello Flask JSON-RPC'),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_notify(self):
        R = [[
            (self._make_payload('jsonrpc.notify', ['this is a string'], version=v, is_notify=True), ''),
        ] for v in ['2.0']][0]
        [self._assert_equals((self.app.post(self.service_url, data=req)).data, resp) for req, resp in R]
        
    def test_strangeEcho(self):
        R = [[
            (self._make_payload('jsonrpc.strangeEcho', {u'1': u'this is a string', u'2': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version=v), ['1', '2', 'wtf', 'nowai', 'Default']),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_safeEcho(self):
        R = [[
            (self._make_payload('jsonrpc.safeEcho', [u'this is string'], version=v), 'this is string'),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_strangeSafeEcho(self):
        R = [[
            (self._make_payload('jsonrpc.strangeSafeEcho', {u'1': u'this is a string', u'2': u'this is omg', u'wtf': u'pants', u'nowai': 'nopants'}, version=v), ['1', '2', 'wtf', 'nowai', 'Default']),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_protectedEcho(self):
        R = [[
            (self._make_payload('jsonrpc.checkedEcho', ['hai', 'hai'], version=v), 'haihai'),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_protectedArgsEcho(self):
        R = [[
            (self._make_payload('jsonrpc.checkedArgsEcho', ['hai', 'hai'], version=v), 'haihai'),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_protectedReturnEcho(self):
        R = [[
            (self._make_payload('jsonrpc.checkedReturnEcho', [], version=v), 'this is a string'),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_authCheckedEcho(self):
        R = [[
            (self._make_payload('jsonrpc.authCheckedEcho', [1.0, [1,2,3]], version=v), {'obj1': 1.0, 'arr1': [1,2,3]}),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        
    def test_checkedVarArgsEcho(self):
        R = [[
            (self._make_payload('jsonrpc.varArgs', ['hai', 'hai', ' -> \o/'], version=v), ['hai', 'hai', ' -> \o/']),
        ] for v in ['1.0', '1.1', '2.0']][0]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in R]
        

if __name__ == '__main__':
    unittest.main()