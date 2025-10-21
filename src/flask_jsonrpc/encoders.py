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
from __future__ import annotations

from enum import Enum
from types import GeneratorType
import typing as t
import inspect
from pathlib import PurePath
from collections import deque
import dataclasses

from typing_extensions import Buffer  # pytype: disable=not-supported-yet

from flask import typing as ft, jsonify as _jsonify

from pydantic.main import BaseModel


def serializable(obj: t.Any) -> t.Any:  # noqa: ANN401, C901
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode('utf-8')
    if isinstance(obj, Buffer):
        return bytes(obj).decode('utf-8')
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)
    if isinstance(obj, dict):
        encoded_dict = {}
        for key, value in obj.items():
            encoded_key = serializable(key)
            encoded_value = serializable(value)
            encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple, deque)):
        encoded_list = []
        for item in obj:
            encoded_list.append(serializable(item))
        return encoded_list
    if dataclasses.is_dataclass(obj):
        obj_dict = dataclasses.asdict(obj)  # type: ignore
        return serializable(obj_dict)
    if isinstance(obj, BaseModel):
        return serializable(obj.model_dump(exclude_none=True, by_alias=True))
    if not inspect.isbuiltin(obj) and getattr(obj, '__module__', '') != 'builtins' and hasattr(obj, '__dict__'):
        return obj.__dict__
    return obj


def jsonify(obj: t.Any) -> ft.ResponseValue:  # noqa: ANN401
    return _jsonify(serializable(obj))
