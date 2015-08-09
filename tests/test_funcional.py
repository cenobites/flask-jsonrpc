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
from __future__ import unicode_literals
import unittest

from flask_jsonrpc._compat import b, u, text_type
from flask_jsonrpc.site import validate_params
from flask_jsonrpc import _parse_sig, OrderedDict
from flask_jsonrpc.exceptions import InvalidParamsError
from flask_jsonrpc.types import Any, Object, Number, Boolean, String, Array, Nil

from apptest import jsonrpc


class JSONRPCFunctionalTestCase(unittest.TestCase):

    def test_method_parser(self):
        working_sigs = [
            ('jsonrpc', 'jsonrpc', OrderedDict(), Any),
            ('jsonrpc.methodName', 'jsonrpc.methodName', OrderedDict(), Any),
            ('jsonrpc.methodName() -> list', 'jsonrpc.methodName', OrderedDict(), list),
            ('jsonrpc.methodName(str, str, str) ', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str), ('c', str)]), Any),
            ('jsonrpc.methodName(str, b=str, c=str)', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str), ('c', str)]), Any),
            ('jsonrpc.methodName(str, b=str) -> dict', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str)]), dict),
            ('jsonrpc.methodName(str, str, c=Any) -> Any', 'jsonrpc.methodName', OrderedDict([('a', str), ('b', str), ('c', Any)]), Any),
            ('jsonrpc(Any) -> Any', 'jsonrpc', OrderedDict([('a', Any)]), Any),
        ]
        error_sigs = [
            ('jsonrpc(nowai) -> Any', ValueError),
            ('jsonrpc(str) -> nowai', ValueError),
            ('jsonrpc(nowai=str, str)', ValueError),
            ('jsonrpc.methodName(nowai*str) -> Any', ValueError)
        ]
        for sig in working_sigs:
            ret = _parse_sig(sig[0], list(iter(sig[2])))
            self.assertEqual(ret[0], sig[1])
            self.assertEqual(ret[1], sig[2])
            self.assertEqual(ret[2], sig[3])
        for sig in error_sigs:
            e = None
            try:
                p = _parse_sig(sig[0], ['a'])
            except Exception as exc:
                e = exc
            self.assertTrue(type(e) is sig[1])

    def test_validate_args(self):
        sig = 'jsonrpc(String, String) -> String'
        M = jsonrpc.method(sig, validate=True)(lambda s1, s2: s1+s2)
        self.assertTrue(validate_params(M, {'params': ['omg', 'wtf']}) is None)

        E = None
        try:
            validate_params(M, {'params': [['omg'], ['wtf']]})
        except Exception as e:
            E = e
        self.assertTrue(type(E) is InvalidParamsError)

    def test_validate_args_any(self):
        sig = 'jsonrpc(s1=Any, s2=Any)'
        M = jsonrpc.method(sig, validate=True)(lambda s1, s2: s1+s2)
        self.assertTrue(validate_params(M, {'params': ['omg', 'wtf']}) is None)
        self.assertTrue(validate_params(M, {'params': [['omg'], ['wtf']]}) is None)
        self.assertTrue(validate_params(M, {'params': {'s1': 'omg', 's2': 'wtf'}}) is None)

    def test_types(self):
        self.assertEqual(type(1), Number)
        self.assertEqual(type(1.0), Number)
        self.assertEqual(type(1+3j), Number)
        self.assertEqual(type(-34.54555), Number)
        self.assertEqual(type(99999999999999999), Number)
        self.assertEqual(type(u''), String)
        self.assertEqual(type(''), String)
        self.assertEqual(type({}), Object)
        self.assertEqual(type(set()), Array)
        self.assertEqual(type(frozenset()), Array)
        self.assertNotEqual(type(''), Object)
        self.assertNotEqual(type([]), Object)
        self.assertEqual(type([]), Array)
        self.assertEqual(type(''), Any)
        self.assertEqual(Any.kind(''), String)
        self.assertEqual(Any.decode('str'), String)
        self.assertEqual(Any.kind({}), Object)
        self.assertEqual(Any.kind(None), Nil)
