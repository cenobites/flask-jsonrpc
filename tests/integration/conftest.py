# Copyright (c) 2012-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
import typing as t
from pathlib import Path

import pytest
import urllib3
import requests

WEB_DRIVER_SCREENSHOT_DIR = Path(os.environ['PYTEST_CACHE_DIR']) / 'screenshots'


@pytest.fixture(autouse=True, scope='module')
def setup_module() -> None:
    urllib3.disable_warnings()


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args: dict[str, t.Any]) -> dict[str, t.Any]:
    return {**browser_context_args, 'ignore_https_errors': True, 'viewport': {'width': 1280, 'height': 720}}


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
