# Copyright (c) 2022-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
import json

from playwright.sync_api import Page, expect

BROWSABLE_API_URL = os.environ['BROWSABLE_API_URL']


def test_index(page: Page) -> None:
    page.goto(f'{BROWSABLE_API_URL}/')
    logo_link = page.locator('#logo-link')
    expect(logo_link).to_have_text('Web browsable API')

    method_signature_title_element = page.locator('.method-title')
    expect(method_signature_title_element).to_contain_text('Api.welcome')

    method_signature_element = page.locator('.method-signature')
    expect(method_signature_element).to_contain_text('Api.welcome() -> String')

    method_signature_summary_element = page.locator('.method-summary')
    expect(method_signature_summary_element).to_contain_text('Welcome Flask JSON-RPC')

    method_signature_description_element = page.locator('.method-description')
    expect(method_signature_description_element).to_contain_text('Welcome to web browsable API')

    request_element = page.locator('.request-content')
    expect(request_element).to_be_visible()
    request_text = request_element.text_content()
    request_data = json.loads(request_text or '{}')
    assert 'id' in request_data
    assert request_data['jsonrpc'] == '2.0'
    assert request_data['method'] == 'Api.welcome'
    assert request_data['params'] == []

    response_element = page.locator('.response-content')
    expect(response_element).to_be_visible()
    response_text = response_element.text_content()
    response_data = json.loads(response_text or '{}')
    assert 'id' in response_data
    assert response_data['jsonrpc'] == '2.0'
    assert response_data['result'] == 'Welcome to Flask JSON-RPC'
