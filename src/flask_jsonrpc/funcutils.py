# Copyright (c) 2024-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
import typing as t
from decimal import Decimal
import inspect
from collections import defaultdict
import dataclasses
from collections.abc import Set, Mapping, Sequence, Collection, MutableSet, MutableMapping, MutableSequence

import typing_inspect
from typing_extensions import Buffer

from pydantic import ValidationError
from pydantic.main import BaseModel, create_model

from flask_jsonrpc.types import types as jsonrpc_types
from flask_jsonrpc.helpers import from_python_type


def loads(param_type: t.Any, param_value: t.Any) -> t.Any:  # noqa: ANN401, C901
    """Deserialize a JSON-RPC parameter value to the specified type.

    Args:
        param_type (typing.Any): The type to deserialize to.
        param_value (typing.Any): The parameter value to deserialize.

    Returns:
        typing.Any: The deserialized parameter value.

    Raises:
        TypeError: If the parameter value cannot be deserialized to the specified type.
        TypeError: If an unsupported union type is provided.

    Examples:
        >>> loads(int, 42)
        42
        >>> loads(list[int], [1, 2, 3])
        [1, 2, 3]
        >>> from enum import Enum
        >>> class Color(Enum):
        ...     RED = 'red'
        ...     GREEN = 'green'
        >>> loads(Color, 'red')
        <Color.RED: 'red'>
        >>> from pydantic import BaseModel
        >>> class User(BaseModel):
        ...     id: int
        ...     name: str
        >>> loads(User, {'id': 1, 'name': 'Alice'})
        User(id=1, name='Alice')
    """
    if param_value is None:
        return param_value

    if param_type is t.Any:
        return param_value

    origin_type = t.get_origin(param_type)
    if origin_type is t.Annotated:
        annotated_origin_type = getattr(param_type, '__origin__', type(None))
        return loads(annotated_origin_type, param_value)

    # XXX: The only type of union that is supported is: typing.Union[T, None] or typing.Optional[T]
    if typing_inspect.is_union_type(param_type) or typing_inspect.is_optional_type(param_type):
        obj_types = t.get_args(param_type)
        if len(obj_types) == 2:
            actual_type, check_type = obj_types
            if actual_type is type(None):
                actual_type, check_type = check_type, actual_type
            if check_type is type(None):
                return loads(actual_type, param_value)
        raise TypeError(
            'the only type of union that is supported is: typing.Union[T, None] or typing.Optional[T]'
        ) from None

    jsonrpc_type = from_python_type(param_type, default=None)
    if jsonrpc_type is None:
        if inspect.isclass(param_type):
            if issubclass(param_type, Enum):
                return param_type(param_value)

            if issubclass(param_type, BaseModel):
                base_model = t.cast(type[BaseModel], param_type)  # type: ignore
                model = create_model(base_model.__name__, __base__=base_model)
                try:
                    return model.model_validate(param_value)
                except ValidationError as e:
                    raise TypeError(str(e)) from e

            # XXX: typing.NamedTuple
            if issubclass(param_type, tuple) and not typing_inspect.is_tuple_type(param_type):
                return param_type(**param_value)

            if dataclasses.is_dataclass(param_type):
                return param_type(**param_value)

            return param_type(**param_value)
        return param_value

    if (
        jsonrpc_types.Number.name == jsonrpc_type.name
        and inspect.isclass(param_type)
        and issubclass(param_type, Decimal)
    ):
        return param_type(str(param_value))

    if jsonrpc_types.Object.name == jsonrpc_type.name:
        loaded_dict = {}
        key_type, value_type = t.get_args(param_type)
        for key, value in param_value.items():
            loaded_key = loads(key_type, key)
            loaded_value = loads(value_type, value)
            loaded_dict[loaded_key] = loaded_value
        dict_param_type_origin: t.Any = t.get_origin(param_type)
        if dict_param_type_origin is defaultdict:
            return defaultdict(None, loaded_dict)
        if any(dict_param_type_origin is tp for tp in (Mapping, MutableMapping)):
            return loaded_dict
        return dict_param_type_origin(loaded_dict)

    if jsonrpc_types.Array.name == jsonrpc_type.name:
        loaded_list = []
        item_type = t.get_args(param_type)[0]
        for item in param_value:
            loaded_list.append(loads(item_type, item))
        list_param_type_origin: t.Any = t.get_origin(param_type)
        if any(list_param_type_origin is tp for tp in (Sequence, MutableSequence, Collection)):
            return loaded_list
        if any(list_param_type_origin is tp for tp in (Set, MutableSet)):
            return set(loaded_list)
        return list_param_type_origin(loaded_list)

    if typing_inspect.is_literal_type(param_type):
        return param_value

    if typing_inspect.is_final_type(param_type):
        return param_value

    if issubclass(param_type, bytes | bytearray):
        return param_type(param_value.encode('utf-8'))

    if issubclass(param_type, Buffer):  # pyright: ignore[reportGeneralTypeIssues]
        return memoryview(param_value.encode('utf-8'))

    return param_value


def bindfy(view_func: t.Callable[..., t.Any], params: dict[str, t.Any]) -> dict[str, t.Any]:  # noqa: ANN401
    """Bind JSON-RPC parameters to a view function's parameters with type deserialization.

    Args:
        view_func (typing.Callable[..., typing.Any]): The view function to bind parameters to.
        params (dict[str, typing.Any]): The JSON-RPC parameters to bind.

    Returns:
        dict[str, typing.Any]: The bound parameters with deserialized values.

    See Also:
        :func:`flask_jsonrpc.funcutils.loads`
    """
    binded_params = {}
    view_func_params = getattr(view_func, 'jsonrpc_method_params', {})
    view_func_default_params = getattr(view_func, 'jsonrpc_method_default_params', {})
    for param_name, param_type in view_func_params.items():
        param_value = params.get(param_name)
        param_default_value = view_func_default_params.get(param_name, None)
        binded_params[param_name] = loads(param_type, param_value if param_value is not None else param_default_value)
    return binded_params
