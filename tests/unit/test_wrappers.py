# Copyright (c) 2024-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
from functools import wraps

from flask_jsonrpc.views import JSONRPCView
from flask_jsonrpc.wrappers import JSONRPCDecoratorMixin

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class MockJSONRPCSite:
    def register(self: Self, name: str, view_func: t.Callable[..., t.Any]) -> None:
        pass

    def register_error_handler(self: Self, exception: type[Exception], fn: t.Callable[[t.Any], t.Any]) -> None:
        pass


mock_jsonrpc_site = MockJSONRPCSite()


class JSONRPCApp(JSONRPCDecoratorMixin):
    def get_jsonrpc_site(self: Self) -> MockJSONRPCSite:
        return mock_jsonrpc_site

    def get_jsonrpc_site_api(self: Self) -> type[JSONRPCView]:
        raise NotImplementedError('.get_jsonrpc_site_api must be overridden') from None


def test_jsonrpc_register_view_function_simple() -> None:
    def view_func(name: str) -> str:
        return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.register_view_function(view_func, 'view_func')
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_decorated() -> None:
    def decorator(fn: t.Callable[[str], str]) -> t.Callable[[str], str]:
        def wrapped(name: str) -> str:
            return fn(name)

        return wrapped

    @decorator
    def view_func(name: str) -> str:
        return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.register_view_function(view_func, 'view_func')
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_wrapped_decorator() -> None:
    def decorator(fn: t.Callable[[str], str]) -> t.Callable[[str], str]:
        @wraps(fn)
        def wrapped(name: str) -> str:
            return fn(name)

        return wrapped

    @decorator
    def view_func(name: str) -> str:
        return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.register_view_function(view_func, 'view_func')
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}
