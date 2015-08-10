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
import sys
import uuid
import random
import unittest

from flask import json

from flask_jsonrpc.exceptions import (Error, ParseError, InvalidRequestError,
                                      MethodNotFoundError, InvalidParamsError,
                                      ServerError, RequestPostError,
                                      InvalidCredentialsError, OtherError)

from apptest import FlaskJSONRPCServerTestCase


class FlaskJSONRPCTestCase(FlaskJSONRPCServerTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _make_payload(self, method, params=None, version='1.0', is_notify=False):
        return json.dumps({
            'jsonrpc': version,
            'method': method,
            'params': params if params else [],
            'id': None if is_notify else str(uuid.uuid4())
        })

    def _call(self, request_data):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post(self.service_url, data=request_data, headers=headers)
        return json.loads(response.data)

    def _assert_equals(self, resp, st):
        self.assertEqual(st, resp, '{0!r} != {1!r}'.format(st, resp))

    def test_payload_id_integer(self):
        req_id = 123456
        for version in ['1.0', '1.1', '2.0']:
            req = json.dumps({'jsonrpc': version, 'method': 'jsonrpc.echo', 'id': req_id})
            resp = self._call(req)
            self.assertEqual(req_id, resp['id'])

    def test_payload_id_string(self):
        req_id = '123456'
        for version in ['1.0', '1.1', '2.0']:
            req = json.dumps({'jsonrpc': version, 'method': 'jsonrpc.echo', 'id': req_id})
            resp = self._call(req)
            self.assertEqual(req_id, resp['id'])

    def test_payload_id_empty(self):
        req_id = ''
        for version in ['1.0', '1.1', '2.0']:
            req = json.dumps({'jsonrpc': version, 'method': 'jsonrpc.echo', 'id': req_id})
            self._assert_equals(self._call(req)['result'], 'Hello Flask JSON-RPC')

    def test_payload_id_none(self):
        req_id = None
        for version in ['1.0', '1.1', '2.0']:
            req = json.dumps({'jsonrpc': version, 'method': 'jsonrpc.echo', 'id': req_id})
            resp = self.app.post(self.service_url, data=req, headers={'Content-Type': 'application/json'}).data
            self.assertEqual('', resp)

    def test_payload_id_null(self):
        for version in ['1.0', '1.1', '2.0']:
            req = json.dumps({'jsonrpc': version, 'method': 'jsonrpc.echo'})
            resp = self.app.post(self.service_url, data=req, headers={'Content-Type': 'application/json'}).data
            self.assertEqual('', resp)

    def test_payload_result_1_0(self):
        req = self._make_payload('jsonrpc.echo', version='1.0')
        resp = self._call(req)
        self.assertTrue('result' in resp)
        self.assertTrue('error' in resp)
        self.assertTrue(not resp['id'] is None)

    def test_payload_result(self):
        for version in ['1.1', '2.0']:
            req = self._make_payload('jsonrpc.echo', version=version)
            resp = self._call(req)
            self.assertTrue('result' in resp)
            self.assertFalse('error' in resp)
            self.assertTrue(not resp['id'] is None)

    def test_payload_error_1_0(self):
        req = self._make_payload('jsonrpc.echoNotFound', version='1.0')
        resp = self._call(req)
        self.assertTrue('result' in resp)
        self.assertTrue('error' in resp)
        self.assertTrue(not resp['id'] is None)

    def test_payload_error(self):
        for version in ['1.1', '2.0']:
            req = self._make_payload('jsonrpc.echoNotFound', version=version)
            resp = self._call(req)
            self.assertFalse('result' in resp)
            self.assertTrue('error' in resp)
            self.assertTrue(not resp['id'] is None)

    def test_payload_method_not_found(self):
        for version in ['1.0', '1.1', '2.0']:
            req = self._make_payload('jsonrpc.echoNotFound', version=version)
            resp = self._call(req)
            self.assertEqual('MethodNotFoundError', resp['error']['name'])
            self.assertTrue(not resp['id'] is None)

    def test_payload_parse_invalid(self):
        for version in ['1.0', '1.1', '2.0']:
            req_json = '{"jsonrpc": "2.0", "method"'
            resp = self._call(req_json)
            self.assertEqual('ParseError', resp['error']['name'])
            self.assertTrue(resp['id'] is None)

    # TODO: make test!
    # def test_payload_request_invalid(self):
    #     for version in ['1.0', '1.1', '2.0']:
    #         req = self._make_payload('1', 'bar', version=version)
    #         resp = self._call(req)
    #         self.assertEqual('RequestPostError', resp['error']['name'])

    def test_batch_invalid_json(self):
        req_json = '''[
          {"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},
          {"jsonrpc": "2.0", "method"
        ]'''
        resp = self._call(req_json)
        self.assertFalse('result' in resp)
        self.assertTrue('error' in resp)
        self.assertEqual('ParseError', resp['error']['name'])

    def test_batch_empty_json(self):
        req = json.dumps([])
        resp = self._call(req)
        self.assertFalse('result' in resp)
        self.assertTrue('error' in resp)
        self.assertEqual('InvalidRequestError', resp['error']['name'])

    def test_batch_invalid_but_not_empty(self):
        req = json.dumps([1])
        resp = self._call(req)
        self.assertTrue(len(resp) == 1)
        self.assertFalse('result' in resp[0])
        self.assertTrue('error' in resp[0])
        self.assertEqual('InvalidRequestError', resp[0]['error']['name'])

    def test_batch_invalid(self):
        req = json.dumps([
            {'jsonrpc': '2.0','method': 'jsonrpc.echoNotFound', 'params': [], 'id': str(uuid.uuid4())},
            {'jsonrpc': '2.0','method': 'jsonrpc.echo', 'params': [], 'id': str(uuid.uuid4())},
            {'jsonrpc': '2.0','method': 'jsonrpc.echoNotFound', 'params': [], 'id': str(uuid.uuid4())}
        ])
        resp = self._call(req)
        self.assertTrue(len(resp) == 3)
        self.assertFalse('result' in resp[0])
        self.assertTrue('error' in resp[0])
        self.assertEqual('Hello Flask JSON-RPC', resp[1]['result'])
        self.assertFalse('error' in resp[1])
        self.assertFalse('result' in resp[2])
        self.assertTrue('error' in resp[2])

    def test_batch_call(self):
        req = json.dumps([
            {'jsonrpc': '2.0','method': 'jsonrpc.echo', 'id': str(uuid.uuid4())},
            {'jsonrpc': '2.0','method': 'jsonrpc.echo', 'params': ['Flask'], 'id': str(uuid.uuid4())},
            {'jsonrpc': '2.0','method': 'jsonrpc.echo', 'params': None, 'id': str(uuid.uuid4())},
            {'jsonrpc': '2.0','method': 'jsonrpc.echo', 'params': [], 'id': str(uuid.uuid4())},
            {'jsonrpc': '2.0','method': 'jsonrpc.echo', 'params': {}, 'id': str(uuid.uuid4())},
            {'jsonrpc': '2.0','method': 'jsonrpc.echo', 'params': [u'フラスコ'], 'id': str(uuid.uuid4())}
        ])
        resp = self._call(req)
        self.assertTrue(len(resp) == 6)
        self.assertEqual('Hello Flask JSON-RPC', resp[0]['result'])
        self.assertFalse('error' in resp[0])
        self.assertEqual('Hello Flask', resp[1]['result'])
        self.assertFalse('error' in resp[1])
        self.assertEqual('Hello Flask JSON-RPC', resp[2]['result'])
        self.assertFalse('error' in resp[2])
        self.assertEqual('Hello Flask JSON-RPC', resp[3]['result'])
        self.assertFalse('error' in resp[3])
        self.assertEqual('Hello Flask JSON-RPC', resp[4]['result'])
        self.assertFalse('error' in resp[4])
        self.assertEqual(u'Hello フラスコ', resp[5]['result'])
        self.assertFalse('error' in resp[5])

    def test_batch_notify(self):
        req = json.dumps([
            {'jsonrpc': '2.0','method': 'jsonrpc.notify', 'params': ['Flask'], 'id': None},
            {'jsonrpc': '2.0','method': 'jsonrpc.notify', 'params': ['JSON-RPC'], 'id': None},
        ])
        resp = self.app.post(self.service_url, data=req).data
        self.assertEqual('', resp)

    def test_echo(self):
        T = [[
            (self._make_payload('jsonrpc.echo', version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', ['Flask'], version=v), 'Hello Flask'),
            (self._make_payload('jsonrpc.echo', None, version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', [], version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', {}, version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echo', [u'フラスコ'], version=v), u'Hello フラスコ'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_my_str(self):
        T = [[
            (self._make_payload('jsonrpc.echoMyStr', [u'Hello Flask JSON-RPC'], version=v), u'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Hello Flask'], version=v), u'Hello Flask'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Kolby Witaj JSON-RPC'], version=v), u'Kolby Witaj JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'JSON-RPC قارورة مرحبا'], version=v), u'JSON-RPC قارورة مرحبا'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Flask Բարեւ JSON-RPC'], version=v), u'Flask Բարեւ JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Настой Добры дзень JSON-RPC'], version=v), u'Настой Добры дзень JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'বোতল হ্যালো JSON-RPC'], version=v), u'বোতল হ্যালো JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Čutura Hello JSON-RPC'], version=v), u'Čutura Hello JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Flascó Hola JSON-RPC'], version=v), u'Flascó Hola JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'瓶喂的JSON-RPC'], version=v), u'瓶喂的JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'瓶餵的JSON-RPC'], version=v), u'瓶餵的JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Baňka Hello JSON-RPC'], version=v), u'Baňka Hello JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Flakono Saluton JSON-RPC'], version=v), u'Flakono Saluton JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Kolb Tere JSON-RPC'], version=v), u'Kolb Tere JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Prasko Kamusta JSON-RPC'], version=v), u'Prasko Kamusta JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Pulloon Hei JSON-RPC'], version=v), u'Pulloon Hei JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Flacon Bonjour JSON-RPC'], version=v), u'Flacon Bonjour JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Hello Flask JSON-RPC'], version=v), u'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Flask გამარჯობა JSON-RPC'], version=v), u'Flask გამარჯობა JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Hallo Flask JSON-RPC'], version=v), u'Hallo Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Γεια Φιάλη JSON-RPC'], version=v), u'Γεια Φιάλη JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'હેલો બાટલી JSON-RPC'], version=v), u'હેલો બાટલી JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Bonjou flakon JSON-RPC'], version=v), u'Bonjou flakon JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'JSON-RPC שלום צפחת'], version=v), u'JSON-RPC שלום צפחת'),
            (self._make_payload('jsonrpc.echoMyStr', [u'हैलो फ्लास्क JSON-RPC'], version=v), u'हैलो फ्लास्क JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Halló flösku JSON-RPC'], version=v), u'Halló flösku JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'こんにちはフラスコJSON-RPC'], version=v), u'こんにちはフラスコJSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'ಹಲೋ ಫ್ಲಾಸ್ಕ್ JSON-ಆರ್.ಪಿ.ಸಿ.'], version=v), u'ಹಲೋ ಫ್ಲಾಸ್ಕ್ JSON-ಆರ್.ಪಿ.ಸಿ.'),
            (self._make_payload('jsonrpc.echoMyStr', [u'ជំរាបសួរ Flask JSON-RPC'], version=v), u'ជំរាបសួរ Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'안녕하세요 플라스크 JSON-RPC'], version=v), u'안녕하세요 플라스크 JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'ສະບາຍດີ Flask JSON-RPC'], version=v), u'ສະບາຍດີ Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Здраво Колба JSON-RPC'], version=v), u'Здраво Колба JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'हॅलो चंबू JSON-RPC'], version=v), u'हॅलो चंबू JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Сайн байна уу колбонд JSON-RPC'], version=v), u'Сайн байна уу колбонд JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'नमस्ते फ्लास्क जेएसओएन-RPC'], version=v), u'नमस्ते फ्लास्क जेएसओएन-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'خوش فلاسک JSON-RPC'], version=v), u'خوش فلاسک JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Olá Flask JSON-RPC'], version=v), u'Olá Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'ਹੈਲੋ ਕਿ ਫਲਾਸਕ JSON-RPC'], version=v), u'ਹੈਲੋ ਕਿ ਫਲਾਸਕ JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Здравствуйте Настой JSON-RPC'], version=v), u'Здравствуйте Настой JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Здраво Пљоска ЈСОН-РПЦ'], version=v), u'Здраво Пљоска ЈСОН-РПЦ'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Dobrý deň, Banka JSON-RPC'], version=v), u'Dobrý deň, Banka JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Pozdravljeni Bučka JSON-RPC'], version=v), u'Pozdravljeni Bučka JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'வணக்கம் குடுவை JSON-RPC'], version=v), u'வணக்கம் குடுவை JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'హలో జాడీలో JSON-RPC'], version=v), u'హలో జాడీలో JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'สวัสดีขวด JSON-RPC'], version=v), u'สวัสดีขวด JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Здравствуйте Настій JSON-RPC'], version=v), u'Здравствуйте Настій JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'خوش فلاسک JSON-RPC'], version=v), u'خوش فلاسک JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'Xin chào Bình JSON-RPC'], version=v), u'Xin chào Bình JSON-RPC'),
            (self._make_payload('jsonrpc.echoMyStr', [u'העלא פלאַסק דזשסאָן-רפּק'], version=v), u'העלא פלאַסק דזשסאָן-רפּק'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_auth(self):
        T = [[
            (self._make_payload('jsonrpc.echoAuth', ['username', 'password', 'Hello Flask JSON-RPC'], version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoAuth', ['username', 'password', 'Hello Flask'], version=v), 'Hello Flask'),
            (self._make_payload('jsonrpc.echoAuth', ['username', 'password', u'خوش فلاسک JSON-RPC'], version=v), u'خوش فلاسک JSON-RPC'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_auth_checked(self):
        T = [[
            (self._make_payload('jsonrpc.echoAuthChecked', {'username': 'flask', 'password': 'jsonrpc', 'string': 'Hello Flask JSON-RPC'}, version=v), 'Hello Flask JSON-RPC'),
            (self._make_payload('jsonrpc.echoAuthChecked', {'username': 'flask', 'password': 'jsonrpc', 'string': 'Hello Flask'}, version=v), 'Hello Flask'),
            (self._make_payload('jsonrpc.echoAuthChecked', {'username': 'flask', 'password': 'jsonrpc', 'string': u'안녕하세요 플라스크 JSON-RPC'}, version=v), u'안녕하세요 플라스크 JSON-RPC'),
        ] for v in ['1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_notify(self):
        T = [[
            (self._make_payload('jsonrpc.notify', ['this is a string'], version=v, is_notify=True), ''),
            (self._make_payload('jsonrpc.notify', [u'瓶喂的JSON-RPC'], version=v, is_notify=True), ''),
        ] for v in ['2.0']]
        [[self._assert_equals((self.app.post(self.service_url, data=req)).data, resp) for req, resp in t] for t in T]

    def test_strangeEcho(self):
        T = [
            (self._make_payload('jsonrpc.strangeEcho', {'1': 'this is a string', '2': 'this is omg', 'wtf': 'pants', 'nowai': 'nopants'}, version='1.1'), ['this is a string', 'this is omg', 'pants', 'nopants', 'Default']),
        ]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in T]

    def test_safeEcho(self):
        T = [[
            (self._make_payload('jsonrpc.safeEcho', ['this is string'], version=v), 'this is string'),
            (self._make_payload('jsonrpc.safeEcho', [u'Здраво Пљоска ЈСОН-РПЦ'], version=v), u'Здраво Пљоска ЈСОН-РПЦ'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_strangeSafeEcho(self):
        T = [
            (self._make_payload('jsonrpc.strangeSafeEcho', {'1': 'this is a string', '2': 'this is omg', 'wtf': 'pants', 'nowai': 'nopants'}, version='1.1'), ['this is a string', 'this is omg', 'pants', 'nopants', 'Default']),
        ]
        [self._assert_equals(self._call(req)['result'], resp) for req, resp in T]

    def test_protectedEcho(self):
        T = [[
            (self._make_payload('jsonrpc.checkedEcho', ['hai', 'hai'], version=v), 'haihai'),
            (self._make_payload('jsonrpc.checkedEcho', [u'Pozdravljeni', 'Bučka'], version=v), u'PozdravljeniBučka'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_protectedArgsEcho(self):
        T = [[
            (self._make_payload('jsonrpc.checkedArgsEcho', ['hai', 'hai'], version=v), 'haihai'),
            (self._make_payload('jsonrpc.checkedArgsEcho', [u'שלום', 'צפחת'], version=v), u'שלוםצפחת'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_protectedReturnEcho(self):
        T = [[
            (self._make_payload('jsonrpc.checkedReturnEcho', [], version=v), 'this is a string'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_authCheckedEcho(self):
        T = [[
            (self._make_payload('jsonrpc.authCheckedEcho', [1.0, [1, 2, 3]], version=v), {'obj1': 1.0, 'arr1': [1, 2, 3]}),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_checkedVarArgsEcho(self):
        T = [[
            (self._make_payload('jsonrpc.varArgs', ['hai', 'hai', ' -> \o/'], version=v), ['hai', 'hai', ' -> \o/']),
            (self._make_payload('jsonrpc.varArgs', ['Flask', u'გამარჯობა', 'JSON-RPC'], version=v), ['Flask', u'გამარჯობა', 'JSON-RPC']),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_sum(self):
        T = [[
            (self._make_payload('jsonrpc.sum', [1, 1], version=v), 2),
            (self._make_payload('jsonrpc.sum', [19, 1], version=v), 20),
            (self._make_payload('jsonrpc.sum', [1.0, 1.0], version=v), 2.0),
            (self._make_payload('jsonrpc.sum', [1.5, 1.5], version=v), 3.0),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_subtract(self):
        T = [[
            (self._make_payload('jsonrpc.subtract', [1, 1], version=v), 0),
            (self._make_payload('jsonrpc.subtract', [5.0, 5.0], version=v), 0.0),
            (self._make_payload('jsonrpc.subtract', [10, 15], version=v), -5),
            (self._make_payload('jsonrpc.subtract', [15, 5.5], version=v), 9.5),
            (self._make_payload('jsonrpc.subtract', [1, 1.5], version=v), -0.5),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_divide(self):
        T = [[
            (self._make_payload('jsonrpc.divide', [1, 1], version=v), 1.0),
            (self._make_payload('jsonrpc.divide', [5.0, 2.0], version=v), 2.5),
            (self._make_payload('jsonrpc.divide', [10, 100], version=v), 0.1),
            (self._make_payload('jsonrpc.divide', [-5, 1], version=v), -5.0),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]

    def test_decorators(self):
        T = [[
            (self._make_payload('jsonrpc.decorators', ['Flask JSON-RPC'], version=v), 'Hello Flask JSON-RPC'),
        ] for v in ['1.0', '1.1', '2.0']]
        [[self._assert_equals(self._call(req)['result'], resp) for req, resp in t] for t in T]
