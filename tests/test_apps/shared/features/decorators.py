# Copyright (c) 2024-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
import functools

from flask_jsonrpc import JSONRPCBlueprint


def jsonrpc_decorator(fn: t.Callable[..., str]) -> t.Callable[..., str]:
    def decorator(string: str) -> str:
        rv = fn(string)
        return f'{rv} from decorator, ;)'

    return decorator


def jsonrpc_decorator_wrapped(fn: t.Callable[..., str]) -> t.Callable[..., str]:
    @functools.wraps(fn)
    def decorator(string: str) -> str:
        rv = fn(string)
        return f'{rv} from decorator, ;)'

    return decorator


jsonrpc = JSONRPCBlueprint('decorators', __name__)


@jsonrpc.method('decorators.decorator')
@jsonrpc_decorator
def decorator(string: str) -> str:
    return f'Hello {string}'


@jsonrpc.method('decorators.wrappedDecorator')
@jsonrpc_decorator_wrapped
def wrappedDecorator(string: str) -> str:
    return f'Hello {string}'
