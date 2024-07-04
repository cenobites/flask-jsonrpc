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
import typing as t
from dataclasses import fields, is_dataclass

from dacite import from_dict

from .typing import Method, OpenRPCSchema


def _dataclass_to_dict(obj: t.Any) -> t.Dict[str, t.Any]:  # noqa: ANN401
    data: t.Dict[str, t.Any] = {}
    for field in fields(obj):
        field_metadata = field.metadata
        field_name = field_metadata.get('field_name', field.name)
        field_value = getattr(obj, field.name)

        if field_value is None:
            continue

        if is_dataclass(field_value):
            data[field_name] = _dataclass_to_dict(field_value)
            continue

        if isinstance(field_value, list):
            col_items = []
            for item in field_value:
                item_value = _dataclass_to_dict(item) if is_dataclass(item) else item
                col_items.append(item_value)
            data[field_name] = col_items
            continue

        if isinstance(field_value, dict):
            map_items: t.Dict[str, t.Any] = {}
            for k, v in field_value.items():
                map_items[k] = _dataclass_to_dict(v) if is_dataclass(v) else v
            data[field_name] = map_items
            continue

        decode = field_metadata.get('decode')
        if decode is not None:
            data[field_name] = decode(field_value)
            continue

        data[field_name] = field_value
    return data


def openrpc_schema_to_dict(openrpc_schema: OpenRPCSchema) -> t.Dict[str, t.Any]:
    """Return the fields of the OpenRPCSchema dataclass instance as a
    new dictionary mapping field names to field values.
    """
    return _dataclass_to_dict(openrpc_schema)


def openrpc_method_schema_from_dict(data: t.Dict[str, t.Any]) -> Method:
    """Create a Method data class instance from a dictionary."""
    return from_dict(data_class=Method, data=data)
