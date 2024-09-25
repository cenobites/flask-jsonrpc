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
import inspect
import dataclasses

from pydantic import ValidationError
from pydantic.main import BaseModel, create_model

from . import types as jsonrpc_types
from .helpers import from_python_type

# Python 3.10+
try:
    from types import NoneType, UnionType
except ImportError:  # pragma: no cover
    UnionType = None  # type: ignore
    NoneType = type(None)  # type: ignore


def loads(param_type: t.Any, param_value: t.Any) -> t.Any:  # noqa: ANN401, C901
    if param_value is None:
        return param_value

    if param_type is t.Any:
        return param_value

    jsonrpc_type = from_python_type(param_type, default=None)
    if jsonrpc_type is None:
        if inspect.isclass(param_type):
            if issubclass(param_type, BaseModel):
                base_model = t.cast(t.Type[BaseModel], param_type)  # type: ignore
                model = create_model(base_model.__name__, __base__=base_model)
                try:
                    return model.model_validate(param_value)
                except ValidationError as e:
                    raise TypeError(str(e)) from e

            if dataclasses.is_dataclass(param_type):
                return param_type(**param_value)

            return param_type(**param_value)

        # XXX: The only type of union that is supported is: typing.Union[T, None] or typing.Optional[T]
        origin_type = t.get_origin(param_type)
        if origin_type is not None and (origin_type is t.Union or origin_type is UnionType):
            obj_types = t.get_args(param_type)
            if len(obj_types) == 2:
                actual_type, check_type = obj_types
                if check_type is NoneType:
                    return loads(actual_type, param_value)
            raise TypeError(
                'the only type of union that is supported is: typing.Union[T, None] or typing.Optional[T]'
            ) from None
        return param_value

    if jsonrpc_types.Object.name == jsonrpc_type.name:
        loaded_dict = {}
        key_type, value_type = t.get_args(param_type)
        for key, value in param_value.items():
            loaded_key = loads(key_type, key)
            loaded_value = loads(value_type, value)
            loaded_dict[loaded_key] = loaded_value
        return loaded_dict

    if jsonrpc_types.Array.name == jsonrpc_type.name:
        loaded_list = []
        item_type = t.get_args(param_type)[0]
        for item in param_value:
            loaded_list.append(loads(item_type, item))
        return loaded_list
    return param_value


def bindfy(view_func: t.Callable[..., t.Any], params: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:  # noqa: ANN401
    binded_params = {}
    view_func_params = getattr(view_func, 'jsonrpc_method_params', {})
    for param_name, param_type in view_func_params.items():
        param_value = params.get(param_name)
        binded_params[param_name] = loads(param_type, param_value)
    return binded_params
