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

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if t.TYPE_CHECKING:
    from .site import JSONRPCSite


class JSONRPCErrorHandlerDecoratorMixin:
    def get_jsonrpc_site(self: Self) -> 'JSONRPCSite':
        raise NotImplementedError('.get_jsonrpc_site must be overridden') from None

    def register_error_handler(self: Self, exception: t.Type[Exception], fn: t.Callable[[t.Any], t.Any]) -> None:
        self.get_jsonrpc_site().register_error_handler(exception, fn)

    def errorhandler(
        self: Self, exception: t.Type[Exception]
    ) -> t.Callable[[t.Callable[[t.Any], t.Any]], t.Callable[[t.Any], t.Any]]:
        def decorator(fn: t.Callable[[t.Any], t.Any]) -> t.Callable[[t.Any], t.Any]:
            self.register_error_handler(exception, fn)
            return fn

        return decorator
