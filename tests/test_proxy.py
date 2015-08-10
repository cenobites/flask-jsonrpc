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
import unittest

from flask import current_app

from flask_jsonrpc.proxy import ServiceProxy

from apptest import FlaskJSONRPCServerTestCase


class JSONRPCServiceProxyTestCase(FlaskJSONRPCServerTestCase):

    def test_positional_args(self):
        proxy = ServiceProxy(self.service_url, version='1.0')
        self.assertTrue(proxy.jsonrpc.echo()['result'] == 'Hello Flask JSON-RPC')
        try:
            proxy.jsonrpc.echo(name='Hello')
        except Exception as e:
            self.assertTrue(e.args[0] == 'Unsupport arg type for JSON-RPC 1.0 (the default version for this '
                                         'client, pass version="2.0" to use keyword arguments)')

    def test_keyword_args(self):
        proxy = ServiceProxy(self.service_url)
        self.assertEquals('Hello Flask', proxy.jsonrpc.echo(name='Flask')['result'])
        self.assertEquals('Hello JSON-RPC', proxy.jsonrpc.echo('JSON-RPC')['result'])

    def test_encoded_args(self):
        proxy = ServiceProxy(self.service_url)
        self.assertEquals('Hello No%20Space', proxy.jsonrpc.echo(name='No%20Space')['result'])
        self.assertEquals('Hello No+Space', proxy.jsonrpc.echo(name='No+Space')['result'])
        self.assertEquals('Hello No=Equal', proxy.jsonrpc.echo(name='No=Equal')['result'])

    def test_my_str(self):
        for version in ['1.0', '1.1', '2.0']:
            proxy = ServiceProxy(self.service_url, version=version)
            [self.assertEquals(resp, req['result']) for req, resp in [
                (proxy.jsonrpc.echoMyStr(u'Hello Flask JSON-RPC'), u'Hello Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Hello Flask'), u'Hello Flask'),
                (proxy.jsonrpc.echoMyStr(u'Kolby Witaj JSON-RPC'), u'Kolby Witaj JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'JSON-RPC قارورة مرحبا'), u'JSON-RPC قارورة مرحبا'),
                (proxy.jsonrpc.echoMyStr(u'Flask Բարեւ JSON-RPC'), u'Flask Բարեւ JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Настой Добры дзень JSON-RPC'), u'Настой Добры дзень JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'বোতল হ্যালো JSON-RPC'), u'বোতল হ্যালো JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Čutura Hello JSON-RPC'), u'Čutura Hello JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Flascó Hola JSON-RPC'), u'Flascó Hola JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'瓶喂的JSON-RPC'), u'瓶喂的JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'瓶餵的JSON-RPC'), u'瓶餵的JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Baňka Hello JSON-RPC'), u'Baňka Hello JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Flakono Saluton JSON-RPC'), u'Flakono Saluton JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Kolb Tere JSON-RPC'), u'Kolb Tere JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Prasko Kamusta JSON-RPC'), u'Prasko Kamusta JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Pulloon Hei JSON-RPC'), u'Pulloon Hei JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Flacon Bonjour JSON-RPC'), u'Flacon Bonjour JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Hello Flask JSON-RPC'), u'Hello Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Flask გამარჯობა JSON-RPC'), u'Flask გამარჯობა JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Hallo Flask JSON-RPC'), u'Hallo Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Γεια Φιάλη JSON-RPC'), u'Γεια Φιάλη JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'હેલો બાટલી JSON-RPC'), u'હેલો બાટલી JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Bonjou flakon JSON-RPC'), u'Bonjou flakon JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'JSON-RPC שלום צפחת'), u'JSON-RPC שלום צפחת'),
                (proxy.jsonrpc.echoMyStr(u'हैलो फ्लास्क JSON-RPC'), u'हैलो फ्लास्क JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Halló flösku JSON-RPC'), u'Halló flösku JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'こんにちはフラスコJSON-RPC'), u'こんにちはフラスコJSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'ಹಲೋ ಫ್ಲಾಸ್ಕ್ JSON-ಆರ್.ಪಿ.ಸಿ.'), u'ಹಲೋ ಫ್ಲಾಸ್ಕ್ JSON-ಆರ್.ಪಿ.ಸಿ.'),
                (proxy.jsonrpc.echoMyStr(u'ជំរាបសួរ Flask JSON-RPC'), u'ជំរាបសួរ Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'안녕하세요 플라스크 JSON-RPC'), u'안녕하세요 플라스크 JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'ສະບາຍດີ Flask JSON-RPC'), u'ສະບາຍດີ Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Здраво Колба JSON-RPC'), u'Здраво Колба JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'हॅलो चंबू JSON-RPC'), u'हॅलो चंबू JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Сайн байна уу колбонд JSON-RPC'), u'Сайн байна уу колбонд JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'नमस्ते फ्लास्क जेएसओएन-RPC'), u'नमस्ते फ्लास्क जेएसओएन-RPC'),
                (proxy.jsonrpc.echoMyStr(u'خوش فلاسک JSON-RPC'), u'خوش فلاسک JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Olá Flask JSON-RPC'), u'Olá Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'ਹੈਲੋ ਕਿ ਫਲਾਸਕ JSON-RPC'), u'ਹੈਲੋ ਕਿ ਫਲਾਸਕ JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Здравствуйте Настой JSON-RPC'), u'Здравствуйте Настой JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Здраво Пљоска ЈСОН-РПЦ'), u'Здраво Пљоска ЈСОН-РПЦ'),
                (proxy.jsonrpc.echoMyStr(u'Dobrý deň, Banka JSON-RPC'), u'Dobrý deň, Banka JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Pozdravljeni Bučka JSON-RPC'), u'Pozdravljeni Bučka JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'வணக்கம் குடுவை JSON-RPC'), u'வணக்கம் குடுவை JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'హలో జాడీలో JSON-RPC'), u'హలో జాడీలో JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'สวัสดีขวด JSON-RPC'), u'สวัสดีขวด JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Здравствуйте Настій JSON-RPC'), u'Здравствуйте Настій JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'خوش فلاسک JSON-RPC'), u'خوش فلاسک JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'Xin chào Bình JSON-RPC'), u'Xin chào Bình JSON-RPC'),
                (proxy.jsonrpc.echoMyStr(u'העלא פלאַסק דזשסאָן-רפּק'), u'העלא פלאַסק דזשסאָן-רפּק')
                ]
            ]

    def test_decorators(self):
        for version in ['1.0', '1.1', '2.0']:
            proxy = ServiceProxy(self.service_url, version=version)
            [self.assertEquals(resp, req['result']) for req, resp in [
                (proxy.jsonrpc.decorators('Flask JSON-RPC'), 'Hello Flask JSON-RPC')
                ]
            ]

    def test_method_repr(self):
        proxy = ServiceProxy(self.service_url)
        self.assertEqual('{"jsonrpc": "2.0", "method": "jsonrpc.echo"}', repr(proxy.jsonrpc.echo))
