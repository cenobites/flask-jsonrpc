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
import logging
from functools import wraps

# Python 3.11+
from typing_extensions import Self

import pytest

from flask_jsonrpc.views import JSONRPCView
from flask_jsonrpc.wrappers import JSONRPCDecoratorMixin
from flask_jsonrpc.types.methods import Summary, MethodAnnotated, MethodAnnotatedType


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


def test_logger() -> None:
    jsonrpc_app = JSONRPCApp()
    logger = jsonrpc_app.logger
    assert logger.name == 'flask_jsonrpc'
    assert logger.level == logging.NOTSET
    assert logger.handlers == []


def test_jsonrpc_register_view_function_simple() -> None:
    def view_func(name: str) -> str:
        return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.register_view_function(view_func, 'view_func')
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str, 'return': str}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}

    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str, 'return': str}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_without_params() -> None:
    def view_func() -> str:
        return 'Hello world'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'return': str}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_without_return() -> None:
    def view_func(name: str) -> None:
        pass

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str, 'return': type(None)}
    assert view_func_wrapped.jsonrpc_method_return is type(None)
    assert view_func_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_without_params_and_return() -> None:
    def view_func() -> None:
        pass

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'return': type(None)}
    assert view_func_wrapped.jsonrpc_method_return is type(None)
    assert view_func_wrapped.jsonrpc_method_params == {}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_with_default_params() -> None:
    def view_func(name: str = 'World', person: str | None = None) -> str:
        return f'Hello {name}, {person or "Anonymous"}!'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'return': str, 'name': str, 'person': str | None}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str, 'person': str | None}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_with_none_params_and_returns() -> None:
    def view_func(person: type(None) = None) -> None:  # type: ignore
        pass

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'return': type(None), 'person': type(None)}
    assert view_func_wrapped.jsonrpc_method_return is type(None)
    assert view_func_wrapped.jsonrpc_method_params == {'person': type(None)}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_annotated() -> None:
    def view_func(
        name: t.Annotated[str, 'metadata'], person: t.Annotated[str | None, 'metadata'] = None
    ) -> t.Annotated[str, 'metadata']:
        return f'Hello {name}, {person or "Anonymous"}!'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func', MethodAnnotated[Summary('summary')])(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {
        'name': t.Annotated[str, 'metadata'],
        'person': t.Annotated[str | None, 'metadata'],
        'return': t.Annotated[str, 'metadata'],
    }
    assert view_func_wrapped.jsonrpc_method_return is t.Annotated[str, 'metadata']
    assert view_func_wrapped.jsonrpc_method_params == {
        'name': t.Annotated[str, 'metadata'],
        'person': t.Annotated[str | None, 'metadata'],
    }
    assert isinstance(view_func_wrapped.jsonrpc_method_annotations, MethodAnnotatedType)
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_not_validate() -> None:
    def view_func(name):  # noqa: ANN001, ANN202
        return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func', None, **{'validate': False})(view_func)  # type: ignore
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': t.Any, 'return': t.Any}
    assert view_func_wrapped.jsonrpc_method_return == t.Any
    assert view_func_wrapped.jsonrpc_method_params == {'name': t.Any}
    assert view_func_wrapped.jsonrpc_validate is False
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': False}


def test_jsonrpc_register_view_function_without_type_hints() -> None:
    def view_func(name):  # noqa: ANN001, ANN202
        return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.register_view_function(view_func, 'view_func')
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {}
    assert view_func_wrapped.jsonrpc_method_return is type(None)
    assert view_func_wrapped.jsonrpc_method_params == {}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}

    with pytest.raises(ValueError):
        jsonrpc_app.method('view_func')(view_func)


def test_jsonrpc_register_view_function_decorated() -> None:
    def decorator(fn: t.Callable[[str], str]) -> t.Callable[[str], str]:
        def wrapped(name: str) -> str:
            return fn(name)

        return wrapped

    @decorator
    def view_func(name: str) -> str:
        return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str, 'return': str}
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
    view_func_wrapped = jsonrpc_app.method('view_func')(view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str, 'return': str}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}


def test_jsonrpc_register_view_function_from_class() -> None:
    class Api:
        def view_func(self: Self, name: str) -> str:
            return f'Hello {name}'

        @staticmethod
        def view_func_staticmethod(name: str) -> str:
            return f'Hello {name}'

        @classmethod
        def view_func_classmethod(cls: 'type[Api]', name: str) -> str:
            return f'Hello {name}'

    jsonrpc_app = JSONRPCApp()
    view_func_wrapped = jsonrpc_app.method('view_func')(Api.view_func)
    assert view_func_wrapped.jsonrpc_method_name == 'view_func'
    assert view_func_wrapped.jsonrpc_method_sig == {'name': str, 'return': str, 'self': Self}
    assert view_func_wrapped.jsonrpc_method_return is str
    assert view_func_wrapped.jsonrpc_method_params == {'name': str, 'self': Self}
    assert view_func_wrapped.jsonrpc_validate is True
    assert view_func_wrapped.jsonrpc_notification is True
    assert view_func_wrapped.jsonrpc_options == {'notification': True, 'validate': True}

    view_func_staticmethod_wrapped = jsonrpc_app.method('view_func_staticmethod')(Api.view_func_staticmethod)
    assert view_func_staticmethod_wrapped.jsonrpc_method_name == 'view_func_staticmethod'
    assert view_func_staticmethod_wrapped.jsonrpc_method_sig == {'name': str, 'return': str}
    assert view_func_staticmethod_wrapped.jsonrpc_method_return is str
    assert view_func_staticmethod_wrapped.jsonrpc_method_params == {'name': str}
    assert view_func_staticmethod_wrapped.jsonrpc_validate is True
    assert view_func_staticmethod_wrapped.jsonrpc_notification is True
    assert view_func_staticmethod_wrapped.jsonrpc_options == {'notification': True, 'validate': True}

    with pytest.raises(ValueError):
        jsonrpc_app.register_view_function(Api.view_func_classmethod, 'view_func_classmethod')


def test_jsonrpc_register_error_handler_simple() -> None:
    def value_error_handle(ex: ValueError) -> str:
        return 'ValueError'

    jsonrpc_app = JSONRPCApp()
    jsonrpc_app.register_error_handler(ValueError, value_error_handle)
    jsonrpc_app.errorhandler(ValueError)(value_error_handle)
