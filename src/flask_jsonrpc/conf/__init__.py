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
    """A protocol for lazy objects that defer initialization until accessed."""

    @property
    def _wrapped(self: Self) -> t.Any: ...  # noqa: ANN401

    def _setup(self: Self) -> None: ...


def new_method_proxy(getter: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
    """Create a method proxy that initializes the lazy object on first access.

    Args:
        getter (typing.Callable[..., typing.Any]): The method to proxy.

    Returns:
        typing.Callable[..., typing.Any]: The proxied method.
    """

    def inner(self: LazyObject, *args: t.Any) -> t.Any:  # noqa: ANN401
        _wrapped = self._wrapped
        if _wrapped is empty:
            self._setup()
            _wrapped = self._wrapped
        return getter(_wrapped, *args)

    inner._mask_wrapped = False  # type: ignore[attr-defined]
    return inner


class Settings:
    """Settings object that loads configuration from global settings and allows fallback settings.

    If a setting is not found in the global settings, it will look for it in the provided fallback settings.

    Args:
        fallback_settings (typing.MutableMapping[str, typing.Any] | None): Optional fallback settings.
    """

    def __init__(self: Self, fallback_settings: t.MutableMapping[str, t.Any] | None = None) -> None:
        self._fallback_settings = fallback_settings
        # XXX: https://mypyc.readthedocs.io/en/latest/differences_from_python.html#monkey-patching
        for setting in dir(global_settings):
            if setting.isupper() and not setting.startswith('_'):
                setattr(self, setting, getattr(global_settings, setting))

    def __getattr__(self: Self, name: str) -> t.Any:  # noqa: ANN401
        if self._fallback_settings is not None:
            env_key = global_settings.CONFIG_TO_ENV(name)
            if env_key in self._fallback_settings:
                return self._fallback_settings[env_key]
        raise AttributeError(f'{type(self).__name__!r} object has no attribute {name!r}')


class LazySettings:
    """A lazy settings object that initializes the settings on first access.

    If a setting is not found in the global settings, it will look for it in the provided fallback settings.

    Args:
        fallback_settings (typing.MutableMapping[str, typing.Any] | None): Optional fallback settings.
    """

    _wrapped = None
    _fallback_settings = None

    def __init__(self: Self, /, *, fallback_settings: t.MutableMapping[str, t.Any] | None = None) -> None:
        self._wrapped = empty
        self._fallback_settings = fallback_settings

    def __getattribute__(self, name: str) -> t.Any:  # noqa: ANN401
        if name in ('_wrapped', '_fallback_settings'):
            return super().__getattribute__(name)
        value = super().__getattribute__(name)
        if not getattr(value, '_mask_wrapped', True):
            raise AttributeError
        return value

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name: str, value: t.Any) -> None:  # noqa: ANN401
        if name in ('_wrapped', '_fallback_settings'):
            self.__dict__[name] = value
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
        self._wrapped = Settings(self._fallback_settings)


settings = LazySettings(fallback_settings=os.environ)
