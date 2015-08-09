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
from flask_jsonrpc.types import Type, Any, Object, Number, Boolean, String, Array, Nil


class JSONRPCTypesTestCase(unittest.TestCase):

    def test_number_types(self):
        self.assertEqual(type(1), Number)
        self.assertEqual(type(-13), Number)
        self.assertEqual(type(1.0), Number)
        self.assertEqual(type(-34.54555), Number)
        self.assertEqual(type(1+3j), Number)
        self.assertEqual(type(99999999999999999), Number)
        self.assertNotEqual(type(''), Number)
        self.assertNotEqual(type({}), Number)
        self.assertNotEqual(type([]), Number)
        self.assertNotEqual(type(set()), Number)
        self.assertNotEqual(type(frozenset()), Number)
        self.assertNotEqual(type(tuple()), Number)
        self.assertNotEqual(type(True), Number)
        self.assertNotEqual(type(False), Number)
        self.assertNotEqual(type(None), Number)

    def test_string_types(self):
        self.assertEqual(type(''), String)
        self.assertNotEqual(type(1), String)
        self.assertNotEqual(type(1.0), String)
        self.assertNotEqual(type(-1.0), String)
        self.assertNotEqual(type({}), String)
        self.assertNotEqual(type([]), String)
        self.assertNotEqual(type(set()), String)
        self.assertNotEqual(type(frozenset()), String)
        self.assertNotEqual(type(tuple()), String)
        self.assertNotEqual(type(True), String)
        self.assertNotEqual(type(False), String)
        self.assertNotEqual(type(None), String)

    def test_object_types(self):
        self.assertEqual(type({}), Object)
        self.assertNotEqual(type(''), Object)
        self.assertNotEqual(type(1), Object)
        self.assertNotEqual(type(1.0), Object)
        self.assertNotEqual(type(-1.0), Object)
        self.assertNotEqual(type([]), Object)
        self.assertNotEqual(type(set()), Object)
        self.assertNotEqual(type(frozenset()), Object)
        self.assertNotEqual(type(tuple()), Object)
        self.assertNotEqual(type(True), Object)
        self.assertNotEqual(type(False), Object)
        self.assertNotEqual(type(None), Object)

    def test_array_types(self):
        self.assertEqual(type([]), Array)
        self.assertEqual(type((1, '12', -3, {})), Array)
        self.assertEqual(type(set()), Array)
        self.assertEqual(type(frozenset()), Array)
        self.assertNotEqual(type(''), Array)
        self.assertNotEqual(type(1), Array)
        self.assertNotEqual(type(1.0), Array)
        self.assertNotEqual(type(-1.0), Array)
        self.assertNotEqual(type({}), Array)
        self.assertNotEqual(type(True), Array)
        self.assertNotEqual(type(False), Array)
        self.assertNotEqual(type(None), Array)

    def test_boolean_types(self):
        self.assertEqual(type(True), Boolean)
        self.assertEqual(type(False), Boolean)
        self.assertEqual(type(bool()), Boolean)
        self.assertNotEqual(type(''), Boolean)
        self.assertNotEqual(type(1), Boolean)
        self.assertNotEqual(type(1.0), Boolean)
        self.assertNotEqual(type(-1.0), Boolean)
        self.assertNotEqual(type([]), Boolean)
        self.assertNotEqual(type(set()), Boolean)
        self.assertNotEqual(type(frozenset()), Boolean)
        self.assertNotEqual(type({}), Boolean)
        self.assertNotEqual(type(None), Boolean)

    def test_nil_types(self):
        self.assertEqual(type(None), Nil)
        self.assertNotEqual(type(''), Nil)
        self.assertNotEqual(type(1), Nil)
        self.assertNotEqual(type(1.0), Nil)
        self.assertNotEqual(type(-1.0), Nil)
        self.assertNotEqual(type([]), Nil)
        self.assertNotEqual(type(set()), Nil)
        self.assertNotEqual(type(frozenset()), Nil)
        self.assertNotEqual(type({}), Nil)
        self.assertNotEqual(type(True), Nil)

    def test_any_types(self):
        self.assertEqual(type(1), Any)
        self.assertEqual(type(-13), Any)
        self.assertEqual(type(1.0), Any)
        self.assertEqual(type(-34.54555), Any)
        self.assertEqual(type(1+3j), Any)
        self.assertEqual(type(99999999999999999), Any)
        self.assertEqual(type(''), Any)
        self.assertEqual(type({}), Any)
        self.assertEqual(type([]), Any)
        self.assertEqual(type((1, '12', -3, {})), Any)
        self.assertEqual(type(set()), Any)
        self.assertEqual(type(frozenset()), Any)
        self.assertEqual(type(True), Any)
        self.assertEqual(type(False), Any)
        self.assertEqual(type(bool()), Any)
        self.assertEqual(type(None), Any)

    def test_kind_types(self):
        self.assertEqual(String.kind(''), String)
        self.assertEqual(Any.kind(''), String)
        self.assertEqual(Any.kind({}), Object)
        self.assertEqual(Any.kind(None), Nil)

    def test_decode_types(self):
        self.assertEqual(Any.decode('obj'), Object)
        self.assertEqual(Any.decode('num'), Number)
        self.assertEqual(Any.decode('bool'), Boolean)
        self.assertEqual(Any.decode('str'), String)
        self.assertEqual(Any.decode('arr'), Array)
        self.assertEqual(Any.decode('nil'), Nil)
        self.assertEqual(Any.decode('any'), Any)
