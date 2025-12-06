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
from io import BytesIO
import os
import sys
import typing as t

from flask.globals import app_ctx as _app_ctx
from flask.testing import EnvironBuilder

import pytest
import requests
from werkzeug.test import run_wsgi_app
from urllib3.response import HTTPResponse
from requests.adapters import BaseAdapter, HTTPAdapter as RequestsHTTPAdapter
from werkzeug.datastructures import Headers

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if t.TYPE_CHECKING:
    from flask import Flask

    from pytest import MonkeyPatch
    from requests import Response, PreparedRequest


class HTTPAdapter(RequestsHTTPAdapter):
    def init_poolmanager(self: Self, connections: int, maxsize: int, block: bool = False, **pool_kwargs: t.Any) -> None:  # noqa: ANN401
        self.poolmanager = None


class FlaskClientAdapter(BaseAdapter):
    def __init__(self: Self, app: 'Flask', path: str = '/', base_url: str | None = None) -> None:
        self.app = app
        self.path = path
        self.base_url = base_url
        self.http_adapter = HTTPAdapter()
        self.environ_base = {'REMOTE_ADDR': '127.0.0.1', 'HTTP_USER_AGENT': 'FlaskClientAdapter/0.0.1'}

    def _build_response(self: Self, req: 'PreparedRequest', resp: tuple[t.Iterable[bytes], str, Headers]) -> 'Response':
        rv, status_code, headers = resp
        if rv:
            fh = BytesIO()
            for chunk in rv:
                fh.write(chunk)
            fh.seek(0)
            rv = fh
        else:
            rv = BytesIO()

        code, reason = status_code.split(None, 1)
        resp_wrapped = HTTPResponse(body=rv, headers=headers, status=int(code), reason=reason, preload_content=False)

        return self.http_adapter.build_response(req, resp_wrapped)

    def send(self: Self, request: 'PreparedRequest', **kwargs: t.Any) -> 'Response':  # noqa: ANN401
        kwargs = {
            'environ_base': self.environ_base,
            'method': request.method,
            'data': request.body,
            'headers': request.headers.items(),
        }
        builder = EnvironBuilder(app=self.app, path=request.path_url, **kwargs)
        if self.base_url:
            builder.base_url = self.base_url

        try:
            environ = builder.get_environ()
        finally:
            builder.close()

        resp = run_wsgi_app(self.app, environ, buffered=True)
        return self._build_response(request, resp)

    def close(self: Self) -> None:
        pass


@pytest.fixture(scope='session')
def api_url() -> str:
    return 'http://localhost/api'


@pytest.fixture(scope='function')
def test_apps(monkeypatch: 'MonkeyPatch') -> t.Generator[None, None, None]:
    monkeypatch.syspath_prepend(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'test_apps'))
    original_modules = set(sys.modules.keys())

    yield None

    # Remove any imports cached during the test. Otherwise "import app"
    # will work in the next test even though it's no longer on the path.
    for key in sys.modules.keys() - original_modules:
        sys.modules.pop(key)


@pytest.fixture(scope='function')
def app(test_apps: 't.Generator[MonkeyPatch]') -> 't.Generator[Flask]':
    """Create and configure a new app instance for each test."""
    from app.app import create_app  # type: ignore

    flask_app = create_app({'TESTING': True})
    yield flask_app


@pytest.fixture(scope='function')
def async_app(test_apps: 't.Generator[MonkeyPatch]') -> 't.Generator[Flask]':
    """Create and configure a new async app instance for each test."""
    from async_app.app import create_app  # type: ignore

    flask_app = create_app({'TESTING': True})
    yield flask_app


@pytest.fixture(autouse=True)
def leak_detector() -> t.Generator[None, None, None]:
    """Fails if any app contexts are still pushed when a test ends. Pops all
    contexts so subsequent tests are not affected.
    """

    yield None

    leaks = []
    while _app_ctx:
        leaks.append(_app_ctx._get_current_object())
        _app_ctx.pop()

    assert not leaks, f'Leaked {len(leaks)} app context(s): {leaks!r}'


@pytest.fixture(scope='function')
def session(app: 'Flask') -> t.Generator[requests.Session, None, None]:
    """A test client for the app."""
    session = requests.Session()
    session.verify = False
    session.mount('http://', FlaskClientAdapter(app=app))

    yield session

    session.close()


@pytest.fixture(scope='function')
def async_session(async_app: 'Flask') -> t.Generator[requests.Session, None, None]:
    """A test async client for the app."""
    session = requests.Session()
    session.verify = False
    session.mount('http://', FlaskClientAdapter(app=async_app))

    yield session

    session.close()
