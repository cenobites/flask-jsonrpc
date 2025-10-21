# Copyright (c) 2023-2024, Cenobit Technologies, Inc. http://cenobit.es/
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

# Added in version 3.11.
from typing_extensions import Self

DEFAULTS = {'DEFAULT_JSONRPC_METHOD': {'VALIDATE': True, 'NOTIFICATION': True}}


class JSONRPCSettings:
    def __init__(self: Self, defaults: dict[str, t.Any] | None = None) -> None:
        # XXX: https://mypyc.readthedocs.io/en/latest/differences_from_python.html#monkey-patching
        for attr, val in (defaults or DEFAULTS).items():
            setattr(JSONRPCSettings, attr, val)

    def __getattr__(self: Self, attr: str) -> t.Any:  # noqa: ANN401  pragma: no cover
        val = getattr(JSONRPCSettings, attr, None)
        if val is None:
            raise AttributeError(f'invalid setting: {attr!r}') from None
        return val

    def __setattr__(self: Self, attr: str, val: t.Any) -> None:  # noqa: ANN401
        setattr(JSONRPCSettings, attr, val)


settings = JSONRPCSettings(DEFAULTS)
