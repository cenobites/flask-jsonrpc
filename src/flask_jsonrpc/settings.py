# Copyright (c) 2023-2023, Cenobit Technologies, Inc. http://cenobit.es/
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

DEFAULTS = {'DEFAULT_JSONRPC_METHOD': {'VALIDATE': True, 'NOTIFICATION': True}}


class JSONRPCSettings:
    def __init__(self: Self, defaults: t.Optional[t.Dict[str, t.Any]] = None) -> None:
        self.defaults = defaults or DEFAULTS
        self.setup(self.defaults)

    def __getattr__(self: Self, attr: str) -> t.Any:  # noqa: ANN401
        if attr not in self.defaults:
            raise AttributeError(f'Invalid setting: {attr!r}')

        val = self.defaults[attr]

        setattr(self, attr, val)
        return val

    # XXX: https://mypyc.readthedocs.io/en/latest/differences_from_python.html#monkey-patching
    def setup(self: Self, defaults: t.Dict[str, t.Any]) -> None:
        for attr, val in defaults.items():
            setattr(JSONRPCSettings, attr, val)


settings = JSONRPCSettings(DEFAULTS)
