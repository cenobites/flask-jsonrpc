# Copyright (c) 2025-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

import os
import typing as t

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc.conf import global_settings

empty = object()


class LazyObject(t.Protocol):  # pragma: no cover
    @property
    def _wrapped(self: Self) -> t.Any: ...  # noqa: ANN401

    def _setup(self: Self) -> None: ...


def new_method_proxy(
    getter: t.Callable[..., t.Any],
    setter: t.Callable[..., None],
    checker: t.Callable[[t.Any, str], bool],
    fallback_settings: t.MutableMapping[str, t.Any] | None = None,
) -> t.Callable[..., t.Any]:
    def inner(self: LazyObject, *args: t.Any) -> t.Any:  # noqa: ANN401
        _wrapped = self._wrapped
        if _wrapped is empty:
            self._setup()
            _wrapped = self._wrapped
        if (
            fallback_settings is not None
            and not checker(_wrapped, *args)
            and len(args) == 1
            and args[0] in fallback_settings
        ):
            setter(_wrapped, args[0], fallback_settings[args[0]])
        return getter(_wrapped, *args)

    inner._mask_wrapped = False  # type: ignore[attr-defined]
    return inner


class Settings:
    def __init__(self: Self) -> None:
        # XXX: https://mypyc.readthedocs.io/en/latest/differences_from_python.html#monkey-patching
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))


class LazySettings:
    _wrapped = None

    def __init__(self: Self) -> None:
        self._wrapped = empty

    def __getattribute__(self, name: str) -> t.Any:  # noqa: ANN401
        if name == '_wrapped':
            return super().__getattribute__(name)
        value = super().__getattribute__(name)
        if not getattr(value, '_mask_wrapped', True):
            raise AttributeError
        return value

    __getattr__ = new_method_proxy(getattr, setattr, hasattr, fallback_settings=os.environ)

    def __setattr__(self, name: str, value: t.Any) -> None:  # noqa: ANN401
        if name == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name: str) -> None:
        if name == '_wrapped':
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self: Self) -> None:
        self._wrapped = Settings()


settings = LazySettings()
