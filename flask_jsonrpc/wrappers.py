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
from typing import TYPE_CHECKING, Any, Type, Callable, Optional, get_type_hints
from inspect import ismethod, signature, isfunction

from typeguard import typechecked

if TYPE_CHECKING:
    from .site import JSONRPCSite
    from .views import JSONRPCView


class JSONRCPDecoratorMixin:
    def _method_has_parameters(self, fn: Callable[..., Any]) -> bool:
        fn_signature = signature(fn)
        return bool(fn_signature.parameters)

    def _method_has_return(self, fn: Callable[..., Any]) -> bool:
        fn_annotations = get_type_hints(fn)
        return 'return' in fn_annotations

    def _validate(self, fn: Callable[..., Any]) -> bool:
        if not self._method_has_parameters(fn) and not self._method_has_return(fn):
            return True
        if not getattr(fn, '__annotations__', None):
            return False
        fn_annotations = get_type_hints(fn)
        fn_annotations.pop('return', None)
        if self._method_has_parameters(fn):
            if not fn_annotations:
                return False
        return True

    def _get_function(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        if isfunction(fn):
            return fn
        if ismethod(fn) and getattr(fn, '__func__', None):
            return fn.__func__  # type: ignore
        raise ValueError('the view function must be either a function or a method')

    def get_jsonrpc_site(self) -> 'JSONRPCSite':
        raise NotImplementedError

    def get_jsonrpc_site_api(self) -> Type['JSONRPCView']:
        raise NotImplementedError

    def register_view_function(
        self, view_func: Callable[..., Any], name: Optional[str] = None, validate: bool = True, **options: Any
    ) -> Callable[..., Any]:
        fn = self._get_function(view_func)
        fn_annotations = get_type_hints(fn)
        method_name = getattr(fn, '__name__', '<noname>') if not name else name
        setattr(fn, 'jsonrpc_method_name', method_name)
        setattr(fn, 'jsonrpc_method_sig', fn_annotations)
        setattr(fn, 'jsonrpc_method_return', fn_annotations.pop('return', None))
        setattr(fn, 'jsonrpc_method_params', fn_annotations)
        setattr(fn, 'jsonrpc_validate', validate)
        setattr(fn, 'jsonrpc_options', options)
        view_func_wrapped = typechecked(view_func) if validate else view_func
        self.get_jsonrpc_site().register(method_name, view_func_wrapped)
        return view_func_wrapped

    def method(self, name: Optional[str] = None, validate: bool = True, **options: Any) -> Callable[..., Any]:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            method_name = getattr(fn, '__name__', '<noname>') if not name else name
            if validate and not self._validate(fn):
                raise ValueError('no type annotations present to: {0}'.format(method_name))
            return self.register_view_function(fn, name, validate, **options)

        return decorator
