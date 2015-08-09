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

from flask import json

from flask_jsonrpc._compat import text_type

from apptest import FlaskJSONRPCServerTestCase


class JSONRPCBrowseTestCase(FlaskJSONRPCServerTestCase):

    def test_index(self):
        with self.app:
            r = self.app.get('/api/browse/')
            data = text_type(r.data)
            self.assertEqual(200, r.status_code)
            self.assertIn('Flask JSON-RPC', data)
            self.assertIn('Web browsable API', data)
            self.assertIn('https://github.com/cenobites/flask-jsonrpc', data)

    def test_json_packages(self):
        with self.app:
            r = self.app.get('/api/browse/packages.json')
            data = json.loads(r.data)
            self.assertEqual(200, r.status_code)
            self.assertIsNotNone(data['jsonrpc'])
            self.assertIn({
                'params': [{'type': 'any', 'name': 'name'}],
                'return': {'type': 'any'},
                'name': 'jsonrpc.echo',
                'summary': None,
                'idempotent': False
            }, data['jsonrpc'])

    def test_json_method(self):
        with self.app:
            r = self.app.get('/api/browse/jsonrpc.echo.json')
            data = json.loads(r.data)
            self.assertEqual(200, r.status_code)
            self.assertIsNotNone(data)
            self.assertEqual({
                'params': [{'type': 'any', 'name': 'name'}],
                'return': {'type': 'any'},
                'name': 'jsonrpc.echo',
                'summary': None,
                'idempotent': False
            }, data)

    def test_partials_dashboard(self):
        with self.app:
            r = self.app.get('/api/browse/partials/dashboard.html')
            data = text_type(r.data)
            self.assertEqual(200, r.status_code)
            self.assertIn('Welcome to web browsable API', data)

    def test_response_object(self):
        with self.app:
            r = self.app.get('/api/browse/partials/response_object.html')
            data = text_type(r.data)
            self.assertEqual(200, r.status_code)
            self.assertIn('HTTP', data)
