# Copyright (c) 2012-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
import typing as t
from pathlib import Path

import pytest
import urllib3
import requests
from playwright.sync_api import Page, expect

BROWSABLE_API_URL = os.environ['BROWSABLE_API_URL']
WEB_DRIVER_SCREENSHOT_DIR = Path(os.environ['PYTEST_CACHE_DIR']) / 'screenshots'


@pytest.fixture(autouse=True, scope='module')
def setup_module() -> None:
    urllib3.disable_warnings()


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args: dict[str, t.Any]) -> dict[str, t.Any]:
    return {**browser_context_args, 'ignore_https_errors': True, 'viewport': {'width': 1280, 'height': 720}}


@pytest.fixture(autouse=True, scope='function')
def page_session(page: Page) -> t.Generator[t.Callable[..., Page], None, None]:
    def goto(jsonrpc_method: str) -> Page:
        page.goto(f'{BROWSABLE_API_URL}/')
        jsonrpc_module = jsonrpc_method.split('.')[0] if '.' in jsonrpc_method else jsonrpc_method
        jsonrpc_module_link = page.locator('a').filter(has=page.get_by_text(jsonrpc_module, exact=True))
        jsonrpc_module_link_class_attr = jsonrpc_module_link.get_attribute('class') or ''
        jsonrpc_method_link = page.locator('a').filter(has=page.get_by_text(jsonrpc_method, exact=True))
        if 'collapsed' in jsonrpc_module_link_class_attr or not jsonrpc_method_link.is_visible():
            jsonrpc_module_link.click()
        jsonrpc_method_link.scroll_into_view_if_needed()
        jsonrpc_method_link.click()
        expect(page).to_have_url(f'{BROWSABLE_API_URL}/#/{jsonrpc_method}')
        return page

    yield goto


@pytest.fixture(autouse=True, scope='function')
def jsonrpc_page_info(page_session: t.Callable[..., Page]) -> t.Generator[t.Callable[..., Page], None, None]:
    def page_info(jsonrpc_method: str, method_title: str, method_signature: str, method_description: str) -> Page:
        page = page_session(jsonrpc_method)

        method_title_element = page.locator('.method-title')
        expect(method_title_element).to_contain_text(method_title)

        method_signature_element = page.locator('.method-signature')
        expect(method_signature_element).to_contain_text(method_signature)

        if method_description:
            method_description_element = page.locator('.method-description')
            expect(method_description_element).to_contain_text(method_description)

        return page

    yield page_info


@pytest.fixture(autouse=True, scope='function')
def jsonrpc_call(page_session: t.Callable[..., Page]) -> t.Generator[t.Callable[..., Page], None, None]:
    def form_submit(
        jsonrpc_method: str,
        test_input: dict[str, t.Any],
        request_expected: dict[str, t.Any],
        response_expected: dict[str, t.Any],
    ) -> Page:
        page = page_session(jsonrpc_method)
        page.get_by_role('button', name='Play', exact=True).click()
        page.wait_for_selector('input[type=text], textarea')
        fields = page.locator('input[type=text]')
        for i in range(fields.count()):
            fields.nth(i).fill('', force=True)
        for name, value in test_input.items():
            page.fill(f'input[name="{name}"]', value if isinstance(value, str) else json.dumps(value), force=True)
        page.get_by_role('button', name='Run', exact=True).click()

        request_element = page.locator('.request-content')
        expect(request_element).to_be_visible()
        request_text = request_element.text_content()
        request_data = json.loads(request_text or '{}')
        assert 'id' in request_data, f"Expected 'id' in request data, got {request_data}"
        for name, value in request_expected.items():
            assert request_data[name] == value, f'Expected {name} to be {value}, got {request_data[name]}'

        response_element = page.locator('.response-content')
        expect(response_element).to_be_visible()
        response_text = response_element.text_content()
        response_data = json.loads(response_text or '{}')
        assert 'id' in response_data, f"Expected 'id' in response data, got {response_data}"
        for name, value in response_expected.items():
            if name == 'error':
                for err_name, err_value in value.items():
                    assert response_data[name][err_name] == err_value, (
                        f'Expected {err_name} to be {err_value}, got {response_data[name][err_name]}'
                    )
                continue
            assert response_data[name] == value, f'Expected {name} to be {value}, got {response_data[name]}'

        return page

    yield form_submit


@pytest.fixture(scope='function')
def session() -> t.Generator[requests.Session, None, None]:
    session = requests.Session()
    session.verify = False
    yield session
    session.close()


@pytest.fixture(scope='function')
def async_session() -> t.Generator[requests.Session, None, None]:
    session = requests.Session()
    session.verify = False
    yield session
    session.close()
