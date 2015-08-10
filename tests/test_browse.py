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

from apptest import FlaskJSONRPCServerTestCase


class JSONRPCBrowseTestCase(FlaskJSONRPCServerTestCase):

    def test_index(self):
        with self.app:
            r = self.app.get('/api/browse/')
            self.assertEqual(200, r.status_code)
            self.assertTrue('Flask JSON-RPC' in r.data)
            self.assertTrue('Web browsable API' in r.data)
            self.assertTrue('https://github.com/cenobites/flask-jsonrpc' in r.data)

    def test_json_packages(self):
        with self.app:
            r = self.app.get('/api/browse/packages.json')
            data = json.loads(r.data)
            self.assertEqual(200, r.status_code)
            self.assertTrue(not data['jsonrpc'] is None)
            self.assertTrue({
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
            self.assertTrue(not data is None)
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
            self.assertEqual(200, r.status_code)
            self.assertTrue('Welcome to web browsable API' in r.data)

    def test_response_object(self):
        with self.app:
            r = self.app.get('/api/browse/partials/response_object.html')
            self.assertEqual(200, r.status_code)
            self.assertTrue('HTTP' in r.data)
