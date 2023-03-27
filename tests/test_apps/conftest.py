# Copyright (c) 2012-2022, Cenobit Technologies, Inc. http://cenobit.es/
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
import time
import unittest
from pathlib import Path

import urllib3
import requests
from selenium import webdriver

WEB_DRIVER_SCREENSHOT_DIR = Path(os.environ['PYTEST_CACHE_DIR']) / 'screenshots'


class APITestCase(unittest.TestCase):
    def setUp(self) -> None:
        urllib3.disable_warnings()
        session = requests.Session()
        session.headers.update(
            {
                'Content-Type': 'application/json',
            }
        )
        session.verify = False
        self.requests = session


class WebDriverTestCase(unittest.TestCase):
    def setUp(self) -> None:
        chrome_prefs = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_experimental_option('prefs', chrome_prefs)
        chrome_options.accept_insecure_certs = True
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(10)
        self.addCleanup(self.driver.quit)
        self.addCleanup(self.take_screenshot)
        if not WEB_DRIVER_SCREENSHOT_DIR.exists():
            WEB_DRIVER_SCREENSHOT_DIR.mkdir(parents=True)

    def take_screenshot(self):
        self.driver.get_screenshot_as_file(str(WEB_DRIVER_SCREENSHOT_DIR / f'{self.id()}-{time.time()}.png'))
