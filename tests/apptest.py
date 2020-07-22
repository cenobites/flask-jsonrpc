# -*- coding: utf-8 -*-
# Copyright (c) 2020-2020, Cenobit Technologies, Inc. http://cenobit.es/
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
import functools
from typing import Any, Dict, List, Tuple, Union

from flask import Flask

from flask_jsonrpc import JSONRPC


class App:
    def index(self, name: str = 'Flask JSON-RPC') -> str:
        return 'Hello {0}'.format(name)

    @staticmethod
    def greeting(name: str = 'Flask JSON-RPC') -> str:
        return 'Hello {0}'.format(name)

    @classmethod
    def hello(cls, name: str = 'Flask JSON-RPC') -> str:
        return 'Hello {0}'.format(name)

    def echo(self, string: str, _some: Any = None) -> str:
        return string

    def notify(self, _string: str = None) -> None:
        pass

    def fails(self, n: int) -> int:
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')


def jsonrcp_decorator(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        rv = fn(*args, **kwargs)
        return '{0} from decorator, ;)'.format(rv)

    return wrapped


def create_app(test_config=None):  # noqa: C901  pylint: disable=W0612
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    if test_config:
        app.config.update(test_config)

    jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.greeting')
    def greeting(name: str = 'Flask JSON-RPC') -> str:
        return 'Hello {0}'.format(name)

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.echo')
    def echo(string: str, _some: Any = None) -> str:
        return string

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.notify')
    def notify(_string: str = None) -> None:
        pass

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.fails')
    def fails(n: int) -> int:
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.strangeEcho')
    def strangeEcho(
        string: str, omg: Dict[str, Any], wtf: List[str], nowai: int, yeswai: str = 'Default'
    ) -> List[Any]:
        return [string, omg, wtf, nowai, yeswai]

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.sum')
    def sum_(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a + b

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.decorators')
    @jsonrcp_decorator
    def decorators(string: str) -> str:
        return 'Hello {0}'.format(string)

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnStatusCode')
    def return_status_code(s: str) -> Tuple[str, int]:
        return 'Status Code {0}'.format(s), 201

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnHeaders')
    def return_headers(s: str) -> Tuple[str, Dict[str, Any]]:
        return 'Headers {0}'.format(s), {'X-JSONRPC': '1'}

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnStatusCodeAndHeaders')
    def return_status_code_and_headers(s: str) -> Tuple[str, int, Dict[str, Any]]:
        return 'Status Code and Headers {0}'.format(s), 400, {'X-JSONRPC': '1'}

    class_app = App()
    jsonrpc.register(class_app.index, name='classapp.index')
    jsonrpc.register(class_app.greeting)
    jsonrpc.register(class_app.hello)
    jsonrpc.register(class_app.echo)
    jsonrpc.register(class_app.notify)
    jsonrpc.register(class_app.fails)

    return app
