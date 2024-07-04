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
import typing as t
from inspect import _empty, ismethod, signature, isfunction
from collections import OrderedDict

from typeguard import typechecked

from .settings import settings

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if t.TYPE_CHECKING:
    from .site import JSONRPCSite
    from .views import JSONRPCView


class JSONRPCDecoratorMixin:
    def _method_options(self: Self, options: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        default_options = {
            'validate': settings.DEFAULT_JSONRPC_METHOD['VALIDATE'],
            'notification': settings.DEFAULT_JSONRPC_METHOD['NOTIFICATION'],
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
        if self._method_has_parameters(fn) and not fn_annotations:
            return False
        return True

    def _get_function(self: Self, fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
        if isfunction(fn):
            return fn
        if ismethod(fn) and getattr(fn, '__func__', None):
            return fn.__func__  # pytype: disable=attribute-error,bad-return-type
        raise ValueError('the view function must be either a function or a method')

    def _get_type_hints_by_signature(
        self: Self, fn: t.Callable[..., t.Any], fn_annotations: t.Dict[str, t.Any]
    ) -> t.Dict[str, t.Any]:
        sig = signature(fn)
        parameters = OrderedDict()
        for name in sig.parameters:
            parameters[name] = fn_annotations.get(name, t.Any)
        parameters['return'] = fn_annotations.get(
            'return', t.Any if sig.return_annotation is _empty else sig.return_annotation
        )
        return parameters

    def _get_annotations(self: Self, fn: t.Callable[..., t.Any], fn_options: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        fn_annotations = t.get_type_hints(fn)
        if not fn_options['validate']:
            fn_annotations = self._get_type_hints_by_signature(fn, fn_annotations)
        if fn_annotations.get('self', None) == Self or ('self' in fn_annotations and not fn_options['validate']):
            del fn_annotations['self']
        if fn_annotations.get('cls', None) == t.Type[Self] or ('cls' in fn_annotations and not fn_options['validate']):
            del fn_annotations['cls']
        return fn_annotations

    def get_jsonrpc_site(self: Self) -> 'JSONRPCSite':
        raise NotImplementedError('.get_jsonrpc_site must be overridden')

    def get_jsonrpc_site_api(self: Self) -> t.Type['JSONRPCView']:
        raise NotImplementedError('.get_jsonrpc_site_api must be overridden')

    def register_view_function(
        self: Self, view_func: t.Callable[..., t.Any], name: t.Optional[str] = None, **options: t.Dict[str, t.Any]
    ) -> t.Callable[..., t.Any]:
        fn = self._get_function(view_func)
        fn_options = self._method_options(options)
        fn_annotations = self._get_annotations(fn, fn_options)
        method_name = name if name else getattr(fn, '__name__', '<noname>')
        view_func_wrapped = typechecked(view_func) if fn_options['validate'] else view_func
        setattr(view_func_wrapped, 'jsonrpc_method_name', method_name)  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_sig', fn_annotations)  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_return', fn_annotations.pop('return', None))  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_method_params', fn_annotations)  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_validate', fn_options['validate'])  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_notification', fn_options['notification'])  # noqa: B010
        setattr(view_func_wrapped, 'jsonrpc_options', fn_options)  # noqa: B010
        self.get_jsonrpc_site().register(method_name, view_func_wrapped)
        return view_func_wrapped

    def method(self: Self, name: t.Optional[str] = None, **options: t.Dict[str, t.Any]) -> t.Callable[..., t.Any]:
        validate = options.get('validate', settings.DEFAULT_JSONRPC_METHOD['VALIDATE'])

        def decorator(fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
            method_name = name if name else getattr(fn, '__name__', '<noname>')
            if validate and not self._validate(fn):
                raise ValueError(f'no type annotations present to: {method_name}')
            return self.register_view_function(fn, name, **options)

        return decorator
