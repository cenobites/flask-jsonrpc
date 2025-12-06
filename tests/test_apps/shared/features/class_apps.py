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
import typing as t

from flask_jsonrpc import JSONRPCBlueprint


class App:
    @staticmethod
    def index(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @staticmethod
    def greeting(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @staticmethod
    def hello(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @staticmethod
    def echo(string: str, _some: t.Any = None) -> str:  # noqa: ANN401
        return string

    @staticmethod
    def notify(_string: str | None = None) -> None:
        pass

    @staticmethod
    def not_allow_notify(_string: str | None = None) -> str:
        return 'Now allow notify'

    @staticmethod
    def fails(n: int) -> int:
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')


class_app = App()

jsonrpc = JSONRPCBlueprint('class_apps', __name__)
jsonrpc.register(class_app.index, name='class_apps.index')
jsonrpc.register(class_app.greeting, name='class_apps.greeting')
jsonrpc.register(class_app.hello, name='class_apps.hello')
jsonrpc.register(class_app.echo, name='class_apps.echo')
jsonrpc.register(class_app.notify, name='class_apps.notify')
jsonrpc.register(class_app.not_allow_notify, name='class_apps.not_allow_notify', notification=False)
jsonrpc.register(class_app.fails, name='class_apps.fails')
