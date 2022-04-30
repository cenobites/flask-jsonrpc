#!/usr/bin/env python
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
import sys
import asyncio
import functools
from typing import Any, Dict, List, Tuple, Union

from flask import Flask

try:
    from flask_jsonrpc import JSONRPC
except ModuleNotFoundError:
    project_dir, project_module_name = os.path.split(os.path.dirname(os.path.realpath(__file__)))
    flask_jsonrpc_project_dir = os.path.join(project_dir, os.pardir, os.pardir, 'src')
    if os.path.exists(flask_jsonrpc_project_dir) and flask_jsonrpc_project_dir not in sys.path:
        sys.path.append(flask_jsonrpc_project_dir)

    from flask_jsonrpc import JSONRPC


class App:
    def index(self, name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @staticmethod
    def greeting(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @classmethod
    def hello(cls, name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    def echo(self, string: str, _some: Any = None) -> str:
        return string

    def notify(self, _string: str = None) -> None:
        pass

    def fails(self, n: int) -> int:
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')


def async_jsonrcp_decorator(fn):
    @functools.wraps(fn)
    async def wrapped(*args, **kwargs):
        rv = await fn(*args, **kwargs)
        return f'{rv} from decorator, ;)'

    return wrapped


def create_async_app(test_config=None):  # noqa: C901  pylint: disable=W0612
    """Create and configure an instance of the Flask application."""
    flask_app = Flask('apptest', instance_relative_config=True)
    if test_config:
        flask_app.config.update(test_config)

    jsonrpc = JSONRPC(flask_app, '/api', enable_web_browsable_api=True)

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.greeting')
    async def greeting(name: str = 'Flask JSON-RPC') -> str:
        await asyncio.sleep(0)
        return f'Hello {name}'

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.echo')
    async def echo(string: str, _some: Any = None) -> str:
        await asyncio.sleep(0)
        return string

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.notify')
    async def notify(_string: str = None) -> None:
        await asyncio.sleep(0)

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.fails')
    async def fails(n: int) -> int:
        await asyncio.sleep(0)
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.strangeEcho')
    async def strange_echo(
        string: str, omg: Dict[str, Any], wtf: List[str], nowai: int, yeswai: str = 'Default'
    ) -> List[Any]:
        await asyncio.sleep(0)
        return [string, omg, wtf, nowai, yeswai]

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.sum')
    async def sum_(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        await asyncio.sleep(0)
        return a + b

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.decorators')
    @async_jsonrcp_decorator
    async def decorators(string: str) -> str:
        await asyncio.sleep(0)
        return f'Hello {string}'

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnStatusCode')
    async def return_status_code(s: str) -> Tuple[str, int]:
        await asyncio.sleep(0)
        return f'Status Code {s}', 201

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnHeaders')
    async def return_headers(s: str) -> Tuple[str, Dict[str, Any]]:
        await asyncio.sleep(0)
        return f'Headers {s}', {'X-JSONRPC': '1'}

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnStatusCodeAndHeaders')
    async def return_status_code_and_headers(s: str) -> Tuple[str, int, Dict[str, Any]]:
        await asyncio.sleep(0)
        return f'Status Code and Headers {s}', 400, {'X-JSONRPC': '1'}

    class_app = App()
    jsonrpc.register(class_app.index, name='classapp.index')
    jsonrpc.register(class_app.greeting)
    jsonrpc.register(class_app.hello)
    jsonrpc.register(class_app.echo)
    jsonrpc.register(class_app.notify)
    jsonrpc.register(class_app.fails)

    return flask_app


if __name__ == '__main__':
    app = create_async_app()
    app.run(host='0.0.0.0')
