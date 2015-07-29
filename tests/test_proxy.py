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

from flask_jsonrpc.proxy import ServiceProxy

from apptest import ServerTestCase

SERVER_HOSTNAME = 'localhost'
SERVER_PORT = 5001


class ServiceProxyTestCase(ServerTestCase):

    def test_positional_args(self):
        proxy = ServiceProxy(self.service_url, version='1.0')
        self.assertTrue(proxy.jsonrpc.echo()['result'] == 'Hello Flask JSON-RPC')
        try:
            proxy.jsonrpc.echo(name='Hello')
        except Exception as e:
            print (e.args)
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
                (proxy.jsonrpc.echoMyStr('Hello Flask JSON-RPC'), 'Hello Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Hello Flask'), 'Hello Flask'),
                (proxy.jsonrpc.echoMyStr('Kolby Witaj JSON-RPC'), 'Kolby Witaj JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('JSON-RPC قارورة مرحبا'), 'JSON-RPC قارورة مرحبا'),
                (proxy.jsonrpc.echoMyStr('Flask Բարեւ JSON-RPC'), 'Flask Բարեւ JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Настой Добры дзень JSON-RPC'), 'Настой Добры дзень JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('বোতল হ্যালো JSON-RPC'), 'বোতল হ্যালো JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Čutura Hello JSON-RPC'), 'Čutura Hello JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Flascó Hola JSON-RPC'), 'Flascó Hola JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('瓶喂的JSON-RPC'), '瓶喂的JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('瓶餵的JSON-RPC'), '瓶餵的JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Baňka Hello JSON-RPC'), 'Baňka Hello JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Flakono Saluton JSON-RPC'), 'Flakono Saluton JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Kolb Tere JSON-RPC'), 'Kolb Tere JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Prasko Kamusta JSON-RPC'), 'Prasko Kamusta JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Pulloon Hei JSON-RPC'), 'Pulloon Hei JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Flacon Bonjour JSON-RPC'), 'Flacon Bonjour JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Hello Flask JSON-RPC'), 'Hello Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Flask გამარჯობა JSON-RPC'), 'Flask გამარჯობა JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Hallo Flask JSON-RPC'), 'Hallo Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Γεια Φιάλη JSON-RPC'), 'Γεια Φιάλη JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('હેલો બાટલી JSON-RPC'), 'હેલો બાટલી JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Bonjou flakon JSON-RPC'), 'Bonjou flakon JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('JSON-RPC שלום צפחת'), 'JSON-RPC שלום צפחת'),
                (proxy.jsonrpc.echoMyStr('हैलो फ्लास्क JSON-RPC'), 'हैलो फ्लास्क JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Halló flösku JSON-RPC'), 'Halló flösku JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('こんにちはフラスコJSON-RPC'), 'こんにちはフラスコJSON-RPC'),
                (proxy.jsonrpc.echoMyStr('ಹಲೋ ಫ್ಲಾಸ್ಕ್ JSON-ಆರ್.ಪಿ.ಸಿ.'), 'ಹಲೋ ಫ್ಲಾಸ್ಕ್ JSON-ಆರ್.ಪಿ.ಸಿ.'),
                (proxy.jsonrpc.echoMyStr('ជំរាបសួរ Flask JSON-RPC'), 'ជំរាបសួរ Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('안녕하세요 플라스크 JSON-RPC'), '안녕하세요 플라스크 JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('ສະບາຍດີ Flask JSON-RPC'), 'ສະບາຍດີ Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Здраво Колба JSON-RPC'), 'Здраво Колба JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('हॅलो चंबू JSON-RPC'), 'हॅलो चंबू JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Сайн байна уу колбонд JSON-RPC'), 'Сайн байна уу колбонд JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('नमस्ते फ्लास्क जेएसओएन-RPC'), 'नमस्ते फ्लास्क जेएसओएन-RPC'),
                (proxy.jsonrpc.echoMyStr('خوش فلاسک JSON-RPC'), 'خوش فلاسک JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Olá Flask JSON-RPC'), 'Olá Flask JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('ਹੈਲੋ ਕਿ ਫਲਾਸਕ JSON-RPC'), 'ਹੈਲੋ ਕਿ ਫਲਾਸਕ JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Здравствуйте Настой JSON-RPC'), 'Здравствуйте Настой JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Здраво Пљоска ЈСОН-РПЦ'), 'Здраво Пљоска ЈСОН-РПЦ'),
                (proxy.jsonrpc.echoMyStr('Dobrý deň, Banka JSON-RPC'), 'Dobrý deň, Banka JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Pozdravljeni Bučka JSON-RPC'), 'Pozdravljeni Bučka JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('வணக்கம் குடுவை JSON-RPC'), 'வணக்கம் குடுவை JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('హలో జాడీలో JSON-RPC'), 'హలో జాడీలో JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('สวัสดีขวด JSON-RPC'), 'สวัสดีขวด JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Здравствуйте Настій JSON-RPC'), 'Здравствуйте Настій JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('خوش فلاسک JSON-RPC'), 'خوش فلاسک JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('Xin chào Bình JSON-RPC'), 'Xin chào Bình JSON-RPC'),
                (proxy.jsonrpc.echoMyStr('העלא פלאַסק דזשסאָן-רפּק'), 'העלא פלאַסק דזשסאָן-רפּק')
                ]
            ]
