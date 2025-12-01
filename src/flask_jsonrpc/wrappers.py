# Copyright (c) 2020-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
from __future__ import annotations

import typing as t
from inspect import Parameter, _empty, signature, isfunction
import logging
import functools
from collections import OrderedDict

import typing_inspect

# Added in version 3.11.
from typing_extensions import Self

from typeguard import typechecked
from werkzeug.utils import cached_property

from .conf import settings
from .types.methods import MethodAnnotatedType

if t.TYPE_CHECKING:
    from .site import JSONRPCSite
    from .views import JSONRPCView


class JSONRPCDecoratorMixin:
    def _method_options(self: Self, options: dict[str, t.Any]) -> dict[str, t.Any]:
        default_options = {
            'validate': settings.DEFAULT_JSONRPC_METHOD_VALIDATE,
            'notification': settings.DEFAULT_JSONRPC_METHOD_NOTIFICATION,
        }
        return {**default_options, **options}

    def _method_has_parameters(self: Self, fn: t.Callable[..., t.Any]) -> bool:
        fn_signature = signature(fn)
        return bool(fn_signature.parameters)

    def _method_has_return(self: Self, fn: t.Callable[..., t.Any]) -> bool:
        fn_annotations = t.get_type_hints(fn)
        return 'return' in fn_annotations and fn_annotations['return'] is not type(None)  # noqa: E721

    def _validate(self: Self, fn: t.Callable[..., t.Any]) -> bool:
        if not self._method_has_parameters(fn) and not self._method_has_return(fn):
            return True
        if not getattr(fn, '__annotations__', None):
            return False
        fn_annotations = t.get_type_hints(fn)
        fn_annotations.pop('return', None)
        return not (self._method_has_parameters(fn) and not fn_annotations)

    def _get_function(self: Self, fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
        if isfunction(fn):
            return fn
        raise ValueError('the view function must be either a function or a staticmethod') from None

    def _get_function_and_wrappers(self: Self, fn: t.Callable[..., t.Any]) -> list[t.Callable[..., t.Any]]:
        fn_wrapped = fn
        wrapped_view_funcs = [fn]
        while hasattr(fn_wrapped, '__wrapped__'):
            fn_wrapped = fn_wrapped.__wrapped__
            wrapped_view_funcs.append(fn_wrapped)
        return wrapped_view_funcs

    def _get_type_hints_by_signature(
        self: Self, fn: t.Callable[..., t.Any], fn_annotations: dict[str, t.Any]
    ) -> dict[str, t.Any]:
        sig = signature(fn)
        parameters = OrderedDict()
        for name in sig.parameters:
            parameters[name] = fn_annotations.get(name, t.Any)
        parameters['return'] = fn_annotations.get(
            'return', t.Any if sig.return_annotation is _empty else sig.return_annotation
        )
        return parameters

    def _get_default_params(self: Self, fn: t.Callable[..., t.Any]) -> dict[str, t.Any]:
        sig = signature(fn)
        return {k: v.default for k, v in sig.parameters.items() if v.default is not Parameter.empty}

    def _get_annotations(self: Self, fn: t.Callable[..., t.Any], fn_options: dict[str, t.Any]) -> dict[str, t.Any]:
        # Changed in version 3.11: Previously, Optional[t] was added
        # for function and method annotations if a default value equal
        # to None was set. Now the annotation is returned unchanged.
        fn_annotations = t.get_type_hints(fn, include_extras=True)
        default_params = self._get_default_params(fn)
        for k, v in default_params.items():
            if fn_annotations.get(k) is type(None):
                continue
            if v is None and typing_inspect.is_optional_type(fn_annotations.get(k)):
                kv_args = t.get_args(fn_annotations[k])
                if t.get_origin(kv_args[0]) is t.Annotated:  # pragma: no cover
                    fn_annotations[k] = kv_args[0]
        if not fn_options['validate']:
            fn_annotations = self._get_type_hints_by_signature(fn, fn_annotations)
        return fn_annotations

    def _typechecked_wraps(self: Self, view_func: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
        wrapped_view_funcs = self._get_function_and_wrappers(view_func)
        new_view_func = typechecked(wrapped_view_funcs.pop())
        wrapped_view_funcs.append(new_view_func)

        fn_wrapper = fn_wrapped = wrapped_view_funcs.pop()
        while len(wrapped_view_funcs) > 0:
            fn_wrapper = wrapped_view_funcs.pop()
            functools.update_wrapper(fn_wrapper, fn_wrapped)
            fn_wrapped = fn_wrapper
        return fn_wrapper

    @cached_property
    def logger(self: Self) -> logging.Logger:
        logger = logging.getLogger('flask_jsonrpc')
        return logger

    def get_jsonrpc_site(self: Self) -> JSONRPCSite:
        raise NotImplementedError('.get_jsonrpc_site must be overridden') from None

    def get_jsonrpc_site_api(self: Self) -> type[JSONRPCView]:
        raise NotImplementedError('.get_jsonrpc_site_api must be overridden') from None

    def register_view_function(
        self: Self,
        view_func: t.Callable[..., t.Any],
        name: str | None = None,
        annotation: MethodAnnotatedType | None = None,
        **options: dict[str, t.Any],
    ) -> t.Callable[..., t.Any]:
        fn = self._get_function(view_func)
        fn_options = self._method_options(options)
        fn_annotations = self._get_annotations(fn, fn_options)
        fn_default_params = self._get_default_params(fn)
        method_name = name if name else getattr(fn, '__name__', '<noname>')
        view_func_wrapped = self._typechecked_wraps(view_func) if fn_options['validate'] else view_func
        setattr(view_func_wrapped, 'jsonrpc_method_name', method_name)  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_sig', fn_annotations.copy())  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_return', fn_annotations.pop('return', type(None)))  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_params', fn_annotations)  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_default_params', fn_default_params)  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_annotations', annotation)  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_validate', fn_options['validate'])  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_notification', fn_options['notification'])  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_options', fn_options)  # noqa: B010
        self.get_jsonrpc_site().register(method_name, view_func_wrapped)
        return view_func_wrapped

    def method(
        self: Self, name: str | None = None, annotation: MethodAnnotatedType | None = None, **options: dict[str, t.Any]
    ) -> t.Callable[..., t.Any]:
        validate = options.get('validate', settings.DEFAULT_JSONRPC_METHOD_VALIDATE)

        def decorator(fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
            fns = self._get_function_and_wrappers(fn)
            method_name = name if name else getattr(fn, '__name__', '<noname>')
            if validate and not all(self._validate(f) for f in fns):
                raise ValueError(f'no type annotations present to: {method_name}') from None
            return self.register_view_function(fn, name, annotation, **options)

        return decorator

    def register_error_handler(self: Self, exception: type[Exception], fn: t.Callable[[t.Any], t.Any]) -> None:
        self.get_jsonrpc_site().register_error_handler(exception, fn)

    def errorhandler(
        self: Self, exception: type[Exception]
    ) -> t.Callable[[t.Callable[[t.Any], t.Any]], t.Callable[[t.Any], t.Any]]:
        def decorator(fn: t.Callable[[t.Any], t.Any]) -> t.Callable[[t.Any], t.Any]:
            self.register_error_handler(exception, fn)
            return fn

        return decorator
