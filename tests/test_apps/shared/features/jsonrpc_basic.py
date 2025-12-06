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

jsonrpc = JSONRPCBlueprint('jsonrpc_basic', __name__)


@jsonrpc.method('jsonrpc_basic.greeting')
def greeting(name: str = 'Flask JSON-RPC') -> str:
    return f'Hello {name}'


@jsonrpc.method('jsonrpc_basic.echo')
def echo(string: str, _some: t.Any = None) -> str:  # noqa: ANN401
    return string


@jsonrpc.method('jsonrpc_basic.notify')
def notify(_string: str | None = None) -> None:
    pass


@jsonrpc.method('jsonrpc_basic.not_allow_notify', notification=False)
def not_allow_notify(_string: str = 'None') -> str:
    return 'Not allow notify'


@jsonrpc.method('jsonrpc_basic.fails')
def fails(n: int) -> int:
    if n % 2 == 0:
        return n
    raise ValueError('number is odd')


@jsonrpc.method('jsonrpc_basic.strangeEcho')
def strange_echo(
    string: str, omg: dict[str, t.Any], wtf: list[str], nowai: int, yeswai: str = 'Default'
) -> list[t.Any]:
    return [string, omg, wtf, nowai, yeswai]


@jsonrpc.method('jsonrpc_basic.sum')
def sum_(a: float, b: float) -> float:
    return a + b


@jsonrpc.method('jsonrpc_basic.returnStatusCode')
def return_status_code(s: str) -> tuple[str, int]:
    return f'Status Code {s}', 201


@jsonrpc.method('jsonrpc_basic.returnHeaders')
def return_headers(s: str) -> tuple[str, dict[str, t.Any]]:
    return f'Headers {s}', {'X-JSONRPC': '1'}


@jsonrpc.method('jsonrpc_basic.returnStatusCodeAndHeaders')
def return_status_code_and_headers(s: str) -> tuple[str, int, dict[str, t.Any]]:
    return f'Status Code and Headers {s}', 400, {'X-JSONRPC': '1'}


@jsonrpc.method('jsonrpc_basic.not_validate', validate=False)
def not_validate(s='Oops!'):  # noqa: ANN001,ANN202,ANN201
    return f'Not validate: {s}'


@jsonrpc.method('jsonrpc_basic.mixin_not_validate', validate=False)
def mixin_not_validate(s, t: int, u, v: str, x, z):  # noqa: ANN001,ANN202,ANN201
    return f'Not validate: {s} {t} {u} {v} {x} {z}'


@jsonrpc.method('jsonrpc_basic.noReturn')
def no_return(_string: str | None = None) -> t.NoReturn:
    raise ValueError('no return')


@jsonrpc.method('jsonrpc_basic.optionalParamWithoutDefaultValue')
def optional_param_without_default_value(string: str | None) -> str | None:
    return string
