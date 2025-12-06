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
from uuid import UUID, uuid4
import typing as t
from collections import OrderedDict
import dataclasses

from pydantic import BaseModel

from flask_jsonrpc import typing as fjt
from flask_jsonrpc.descriptor import JSONRPCServiceDescriptor
import flask_jsonrpc.types.params as tp
import flask_jsonrpc.types.methods as tm

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class MockJSONRPCSite:
    def __init__(self: Self) -> None:
        self.path = '/'
        self.base_url = None
        self.view_funcs: t.OrderedDict[str, t.Callable[..., t.Any]] = OrderedDict()
        self.uuid: UUID = uuid4()
        self.name: str = 'Flask-JSONRPC'
        self.version: str = '1.0.0'

    def register(self: Self, name: str, view_func: t.Callable[..., t.Any]) -> None:
        pass


def test_descriptor_describe() -> None:
    mock_jsonrpc_site = MockJSONRPCSite()
    jsonrpc_serv_descriptor = JSONRPCServiceDescriptor(mock_jsonrpc_site)
    view_func_describe = jsonrpc_serv_descriptor.describe
    assert view_func_describe.jsonrpc_method_name == 'rpc.describe'
    assert view_func_describe.jsonrpc_method_sig == {'return': t.Annotated[fjt.ServiceDescribe, None]}
    assert view_func_describe.jsonrpc_method_return is t.Annotated[fjt.ServiceDescribe, None]
    assert view_func_describe.jsonrpc_method_params == {}
    assert (
        view_func_describe.jsonrpc_method_annotations
        == tm.MethodAnnotated[
            tm.Summary('RPC Describe'),
            tm.Description('Service description for JSON-RPC 2.0'),
            tm.Validate(False),
            tm.Notification(False),
        ]
    )
    assert view_func_describe.jsonrpc_validate is False
    assert view_func_describe.jsonrpc_notification is False
    assert view_func_describe.jsonrpc_options == {'notification': False, 'validate': False}

    describe = view_func_describe()
    assert describe.id == f'urn:uuid:{mock_jsonrpc_site.uuid}'
    assert describe.version == '1.0.0'
    assert describe.name == 'Flask-JSONRPC'
    assert describe.servers == [fjt.Server(url='/')]
    assert describe.methods == OrderedDict()


def test_descriptor_describe_with_method_not_annotated() -> None:
    def view_func(param1: str) -> dict[str, str]:
        return {param1: param1}

    mock_jsonrpc_site = MockJSONRPCSite()
    mock_jsonrpc_site.view_funcs = OrderedDict({'view_func': view_func})

    jsonrpc_serv_descriptor = JSONRPCServiceDescriptor(mock_jsonrpc_site)
    view_func_describe = jsonrpc_serv_descriptor.describe
    assert view_func_describe.jsonrpc_method_name == 'rpc.describe'
    assert view_func_describe.jsonrpc_method_sig == {'return': t.Annotated[fjt.ServiceDescribe, None]}
    assert view_func_describe.jsonrpc_method_return is t.Annotated[fjt.ServiceDescribe, None]
    assert view_func_describe.jsonrpc_method_params == {}
    assert (
        view_func_describe.jsonrpc_method_annotations
        == tm.MethodAnnotated[
            tm.Summary('RPC Describe'),
            tm.Description('Service description for JSON-RPC 2.0'),
            tm.Validate(False),
            tm.Notification(False),
        ]
    )
    assert view_func_describe.jsonrpc_validate is False
    assert view_func_describe.jsonrpc_notification is False
    assert view_func_describe.jsonrpc_options == {'notification': False, 'validate': False}

    describe = view_func_describe()
    assert describe.id == f'urn:uuid:{mock_jsonrpc_site.uuid}'
    assert describe.version == '1.0.0'
    assert describe.name == 'Flask-JSONRPC'
    assert describe.servers == [fjt.Server(url='/')]
    assert describe.methods == OrderedDict(
        {
            'view_func': fjt.Method(
                name='view_func',
                type='method',
                validation=True,
                notification=True,
                params=[],
                returns=fjt.Field(name='default', type='Null'),
            )
        }
    )


def test_descriptor_describe_with_method_annotated() -> None:
    class MyPydanticModel(BaseModel):
        name: str
        age: int

    def view_func(
        string: str, integer: int, floating: float, my_model: MyPydanticModel | None = None
    ) -> dict[str, t.Any]:
        return {
            'string': string,
            'integer': integer,
            'floating': floating,
            'my_model': my_model.model_dump() if my_model is not None else None,
        }

    annotations = {
        'string': str,
        'integer': int,
        'floating': float,
        'my_model': MyPydanticModel | None,
        'return': dict[str, t.Any],
    }
    setattr(view_func, 'jsonrpc_method_name', 'view_func')  # noqa: B010
    setattr(view_func, 'jsonrpc_method_sig', annotations.copy())  # noqa: B010
    setattr(view_func, 'jsonrpc_method_return', annotations.pop('return'))  # noqa: B010
    setattr(view_func, 'jsonrpc_method_params', annotations)  # noqa: B010
    setattr(  # noqa: B010
        view_func,
        'jsonrpc_method_annotations',
        tm.MethodAnnotated[
            tm.Summary('method summary'),
            tm.Description('method description'),
            tm.Validate(),
            tm.Notification(),
            tm.Deprecated(False),
            tm.Tag('tag1'),
            tm.Example(
                name='default',
                summary='default example summary',
                description='default example description',
                params=[
                    tm.ExampleField(
                        name='string',
                        value='value1',
                        summary='example string param summary',
                        description='example string param description',
                    ),
                    tm.ExampleField(
                        name='integer',
                        value=5,
                        summary='example integer param summary',
                        description='example integer param description',
                    ),
                    tm.ExampleField(
                        name='floating',
                        value=9.99,
                        summary='example floating param summary',
                        description='example floating param description',
                    ),
                    tm.ExampleField(
                        name='my_model',
                        value={'name': 'John', 'age': 10},
                        summary='example my_model param summary',
                        description='example my_model param description',
                    ),
                ],
                returns=tm.ExampleField(
                    name='default',
                    value={'string': 'value1', 'integer': 5, 'floating': 9.99, 'my_model': {'name': 'John', 'age': 10}},
                    summary='example default return summary',
                    description='example default return description',
                ),
            ),
            tm.Error(code=-32000, message='MessageError', status_code=422, data={'message': 'Message Error'}),
        ],
    )
    setattr(view_func, 'jsonrpc_validate', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_notification', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_options', {'notification': True, 'validate': True})  # noqa: B010

    mock_jsonrpc_site = MockJSONRPCSite()
    mock_jsonrpc_site.view_funcs = OrderedDict({'view_func': view_func})

    jsonrpc_serv_descriptor = JSONRPCServiceDescriptor(mock_jsonrpc_site)
    view_func_describe = jsonrpc_serv_descriptor.describe
    assert view_func_describe.jsonrpc_method_name == 'rpc.describe'
    assert view_func_describe.jsonrpc_method_sig == {'return': t.Annotated[fjt.ServiceDescribe, None]}
    assert view_func_describe.jsonrpc_method_return is t.Annotated[fjt.ServiceDescribe, None]
    assert view_func_describe.jsonrpc_method_params == {}
    assert (
        view_func_describe.jsonrpc_method_annotations
        == tm.MethodAnnotated[
            tm.Summary('RPC Describe'),
            tm.Description('Service description for JSON-RPC 2.0'),
            tm.Validate(False),
            tm.Notification(False),
        ]
    )
    assert view_func_describe.jsonrpc_validate is False
    assert view_func_describe.jsonrpc_notification is False
    assert view_func_describe.jsonrpc_options == {'notification': False, 'validate': False}

    describe = view_func_describe()
    assert describe.id == f'urn:uuid:{mock_jsonrpc_site.uuid}'
    assert describe.version == '1.0.0'
    assert describe.name == 'Flask-JSONRPC'
    assert describe.servers == [fjt.Server(url='/')]
    assert describe.methods == OrderedDict(
        {
            'view_func': fjt.Method(
                name='view_func',
                type='method',
                summary='method summary',
                description='method description',
                validation=True,
                notification=True,
                deprecated=False,
                params=[
                    fjt.Field(name='string', type='String'),
                    fjt.Field(name='integer', type='Number'),
                    fjt.Field(name='floating', type='Number'),
                    fjt.Field(
                        name='my_model',
                        type='Object',
                        properties={
                            'name': fjt.Field(name='name', type='String'),
                            'age': fjt.Field(name='age', type='Number'),
                        },
                    ),
                ],
                returns=fjt.Field(name='default', type='Object'),
                tags=['tag1'],
                errors=[
                    fjt.Error(code=-32000, message='MessageError', data={'message': 'Message Error'}, status_code=422)
                ],
                examples=[
                    fjt.Example(
                        name='default',
                        summary='default example summary',
                        description='default example description',
                        params=[
                            fjt.ExampleField(
                                name='string',
                                value='value1',
                                summary='example string param summary',
                                description='example string param description',
                            ),
                            fjt.ExampleField(
                                name='integer',
                                value=5,
                                summary='example integer param summary',
                                description='example integer param description',
                            ),
                            fjt.ExampleField(
                                name='floating',
                                value=9.99,
                                summary='example floating param summary',
                                description='example floating param description',
                            ),
                            fjt.ExampleField(
                                name='my_model',
                                value={'name': 'John', 'age': 10},
                                summary='example my_model param summary',
                                description='example my_model param description',
                            ),
                        ],
                        returns=fjt.ExampleField(
                            name='default',
                            value={
                                'string': 'value1',
                                'integer': 5,
                                'floating': 9.99,
                                'my_model': {'name': 'John', 'age': 10},
                            },
                            summary='example default return summary',
                            description='example default return description',
                        ),
                    )
                ],
            )
        }
    )


def test_descriptor_describe_with_params_annotated() -> None:
    class MyPydanticModel(BaseModel):
        name: str
        age: int

    def view_func(
        string: str, integer: int, floating: float, my_model: MyPydanticModel | None = None
    ) -> dict[str, t.Any]:
        return {
            'string': string,
            'integer': integer,
            'floating': floating,
            'my_model': my_model.model_dump() if my_model is not None else None,
        }

    annotations = {
        'string': t.Annotated[
            str,
            tp.Summary('string param summary'),
            tp.Description('string param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.MaxDigits(10),
            tp.MaxLength(10),
            tp.MinLength(1),
            tp.Pattern('a-zA-Z'),
        ],
        'integer': t.Annotated[
            int,
            tp.Summary('integer param summary'),
            tp.Description('integer param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.Maximum(100),
            tp.Minimum(1),
            tp.AllowInfNan(False),
        ],
        'floating': t.Annotated[
            float,
            tp.Summary('floating param summary'),
            tp.Description('floating param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.Maximum(100.0),
            tp.Minimum(1.0),
            tp.AllowInfNan(False),
            tp.DecimalPlaces(2),
        ],
        'my_model': t.Annotated[
            MyPydanticModel | None, tp.Summary('my_model param summary'), tp.Description('my_model param description')
        ],
        'return': t.Annotated[dict[str, t.Any], tp.Summary('return summary'), tp.Description('return description')],
    }
    setattr(view_func, 'jsonrpc_method_name', 'view_func')  # noqa: B010
    setattr(view_func, 'jsonrpc_method_sig', annotations.copy())  # noqa: B010
    setattr(view_func, 'jsonrpc_method_return', annotations.pop('return'))  # noqa: B010
    setattr(view_func, 'jsonrpc_method_params', annotations)  # noqa: B010
    setattr(view_func, 'jsonrpc_validate', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_notification', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_options', {'notification': True, 'validate': True})  # noqa: B010

    mock_jsonrpc_site = MockJSONRPCSite()
    mock_jsonrpc_site.view_funcs = OrderedDict({'view_func': view_func})

    jsonrpc_serv_descriptor = JSONRPCServiceDescriptor(mock_jsonrpc_site)
    view_func_describe = jsonrpc_serv_descriptor.describe
    assert view_func_describe.jsonrpc_method_name == 'rpc.describe'
    assert view_func_describe.jsonrpc_method_sig == {'return': t.Annotated[fjt.ServiceDescribe, None]}
    assert view_func_describe.jsonrpc_method_return is t.Annotated[fjt.ServiceDescribe, None]
    assert view_func_describe.jsonrpc_method_params == {}
    assert (
        view_func_describe.jsonrpc_method_annotations
        == tm.MethodAnnotated[
            tm.Summary('RPC Describe'),
            tm.Description('Service description for JSON-RPC 2.0'),
            tm.Validate(False),
            tm.Notification(False),
        ]
    )
    assert view_func_describe.jsonrpc_validate is False
    assert view_func_describe.jsonrpc_notification is False
    assert view_func_describe.jsonrpc_options == {'notification': False, 'validate': False}

    describe = view_func_describe()
    assert describe.id == f'urn:uuid:{mock_jsonrpc_site.uuid}'
    assert describe.version == '1.0.0'
    assert describe.name == 'Flask-JSONRPC'
    assert describe.servers == [fjt.Server(url='/')]
    assert describe.methods == OrderedDict(
        {
            'view_func': fjt.Method(
                name='view_func',
                type='method',
                validation=True,
                notification=True,
                params=[
                    fjt.Field(
                        name='string',
                        type='String',
                        summary='string param summary',
                        description='string param description',
                        required=True,
                        deprecated=False,
                        nullable=False,
                        min_length=1,
                        max_length=10,
                        pattern='a-zA-Z',
                        max_digits=10,
                    ),
                    fjt.Field(
                        name='integer',
                        type='Number',
                        summary='integer param summary',
                        description='integer param description',
                        required=True,
                        deprecated=False,
                        nullable=False,
                        minimum=1.0,
                        maximum=100.0,
                        allow_inf_nan=False,
                    ),
                    fjt.Field(
                        name='floating',
                        type='Number',
                        summary='floating param summary',
                        description='floating param description',
                        required=True,
                        deprecated=False,
                        nullable=False,
                        minimum=1.0,
                        maximum=100.0,
                        allow_inf_nan=False,
                        decimal_places=2,
                    ),
                    fjt.Field(
                        name='my_model',
                        type='Object',
                        summary='my_model param summary',
                        description='my_model param description',
                        properties={
                            'name': fjt.Field(name='name', type='String'),
                            'age': fjt.Field(name='age', type='Number'),
                        },
                    ),
                ],
                returns=fjt.Field(
                    name='default', type='Object', summary='return summary', description='return description'
                ),
            )
        }
    )


def test_descriptor_describe_with_params_annotated_with_properties() -> None:
    @dataclasses.dataclass
    class MyDataClass:
        name: str
        age: int
        extras: dict[str, str]

    def view_func(string: str, integer: int, floating: float, my_data_class: MyDataClass) -> dict[str, t.Any]:
        return {
            'string': string,
            'integer': integer,
            'floating': floating,
            'my_data_class': dataclasses.asdict(my_data_class),
        }

    annotations = {
        'string': t.Annotated[
            str,
            tp.Summary('string param summary'),
            tp.Description('string param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.MaxDigits(10),
            tp.MaxLength(10),
            tp.MinLength(1),
            tp.Pattern('a-zA-Z'),
            tp.Properties({'string': t.Annotated[str, tp.Required()]}),
        ],
        'integer': t.Annotated[
            int,
            tp.Summary('integer param summary'),
            tp.Description('integer param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.Maximum(100),
            tp.Minimum(1),
            tp.AllowInfNan(False),
            tp.Properties({'integer': t.Annotated[int, tp.Required()]}),
        ],
        'floating': t.Annotated[
            float,
            tp.Summary('floating param summary'),
            tp.Description('floating param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.Maximum(100.0),
            tp.Minimum(1.0),
            tp.AllowInfNan(False),
            tp.DecimalPlaces(2),
            tp.Properties({'floating': t.Annotated[float, tp.Required()]}),
        ],
        'my_data_class': t.Annotated[
            MyDataClass,
            tp.Summary('my_data_class param summary'),
            tp.Description('my_data_class param description'),
            tp.Properties(
                {
                    'name': t.Annotated[str, tp.Summary('name param')],
                    'age': t.Annotated[int, tp.Summary('age param')],
                    'extras': tp.Properties(
                        {
                            'param1': t.Annotated[str, tp.Summary('extras param1 param')],
                            'param2': tp.Properties(
                                {
                                    'param21': t.Annotated[str, tp.Summary('extras param21 param')],
                                    'param22': t.Annotated[str, tp.Summary('extras param22 param')],
                                }
                            ),
                        }
                    ),
                }
            ),
        ],
        'return': t.Annotated[
            dict[str, t.Any],
            tp.Summary('return summary'),
            tp.Description('return description'),
            tp.Properties(
                {
                    'string': t.Annotated[
                        str,
                        tp.Summary('string param summary'),
                        tp.Description('string param description'),
                        tp.Required(),
                        tp.Deprecated(False),
                        tp.Nullable(False),
                        tp.MaxDigits(10),
                        tp.MaxLength(10),
                        tp.MinLength(1),
                        tp.Pattern('a-zA-Z'),
                        tp.Example('default', 'Eve'),
                    ],
                    'integer': t.Annotated[
                        int,
                        tp.Summary('integer param summary'),
                        tp.Description('integer param description'),
                        tp.Required(),
                        tp.Deprecated(False),
                        tp.Nullable(False),
                        tp.Maximum(100),
                        tp.Minimum(1),
                        tp.MultipleOf(2),
                        tp.AllowInfNan(False),
                        tp.Example('default', 1),
                    ],
                    'floating': t.Annotated[
                        float,
                        tp.Summary('floating param summary'),
                        tp.Description('floating param description'),
                        tp.Required(),
                        tp.Deprecated(False),
                        tp.Nullable(False),
                        tp.Maximum(100.0),
                        tp.Minimum(1.0),
                        tp.AllowInfNan(False),
                        tp.DecimalPlaces(2),
                        tp.Example('default', 1.0),
                    ],
                    'my_data_class': t.Annotated[
                        MyDataClass,
                        tp.Example(
                            'default',
                            {
                                'name': 'Lou',
                                'age': 12,
                                'extras': {'param1': 'Eve', 'param2': {'param21': 'Tequila', 'param22': 'Mya'}},
                            },
                        ),
                        tp.Properties(
                            {
                                'name': t.Annotated[str, tp.Summary('name param')],
                                'age': t.Annotated[int, tp.Summary('age param')],
                                'extras': tp.Properties(
                                    {
                                        'param1': t.Annotated[str, tp.Summary('extras param1 param')],
                                        'param2': tp.Properties(
                                            {
                                                'param21': t.Annotated[str, tp.Summary('extras param21 param')],
                                                'param22': t.Annotated[str, tp.Summary('extras param22 param')],
                                            }
                                        ),
                                    }
                                ),
                            }
                        ),
                    ],
                }
            ),
        ],
    }
    setattr(view_func, 'jsonrpc_method_name', 'view_func')  # noqa: B010
    setattr(view_func, 'jsonrpc_method_sig', annotations.copy())  # noqa: B010
    setattr(view_func, 'jsonrpc_method_return', annotations.pop('return'))  # noqa: B010
    setattr(view_func, 'jsonrpc_method_params', annotations)  # noqa: B010
    setattr(view_func, 'jsonrpc_validate', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_notification', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_options', {'notification': True, 'validate': True})  # noqa: B010

    mock_jsonrpc_site = MockJSONRPCSite()
    mock_jsonrpc_site.view_funcs = OrderedDict({'view_func': view_func})

    jsonrpc_serv_descriptor = JSONRPCServiceDescriptor(mock_jsonrpc_site)
    view_func_describe = jsonrpc_serv_descriptor.describe
    assert view_func_describe.jsonrpc_method_name == 'rpc.describe'
    assert view_func_describe.jsonrpc_method_sig == {'return': t.Annotated[fjt.ServiceDescribe, None]}
    assert view_func_describe.jsonrpc_method_return is t.Annotated[fjt.ServiceDescribe, None]
    assert view_func_describe.jsonrpc_method_params == {}
    assert (
        view_func_describe.jsonrpc_method_annotations
        == tm.MethodAnnotated[
            tm.Summary('RPC Describe'),
            tm.Description('Service description for JSON-RPC 2.0'),
            tm.Validate(False),
            tm.Notification(False),
        ]
    )
    assert view_func_describe.jsonrpc_validate is False
    assert view_func_describe.jsonrpc_notification is False
    assert view_func_describe.jsonrpc_options == {'notification': False, 'validate': False}

    describe = view_func_describe()
    assert describe.id == f'urn:uuid:{mock_jsonrpc_site.uuid}'
    assert describe.version == '1.0.0'
    assert describe.name == 'Flask-JSONRPC'
    assert describe.servers == [fjt.Server(url='/')]
    assert describe.methods == OrderedDict(
        {
            'view_func': fjt.Method(
                name='view_func',
                type='method',
                validation=True,
                notification=True,
                params=[
                    fjt.Field(
                        name='string',
                        type='String',
                        summary='string param summary',
                        description='string param description',
                        properties={'string': fjt.Field(name='string', type='String', required=True)},
                        required=True,
                        deprecated=False,
                        nullable=False,
                        min_length=1,
                        max_length=10,
                        pattern='a-zA-Z',
                        max_digits=10,
                    ),
                    fjt.Field(
                        name='integer',
                        type='Number',
                        summary='integer param summary',
                        description='integer param description',
                        properties={'integer': fjt.Field(name='integer', type='Number', required=True)},
                        required=True,
                        deprecated=False,
                        nullable=False,
                        minimum=1,
                        maximum=100,
                        allow_inf_nan=False,
                    ),
                    fjt.Field(
                        name='floating',
                        type='Number',
                        summary='floating param summary',
                        description='floating param description',
                        properties={'floating': fjt.Field(name='floating', type='Number', required=True)},
                        required=True,
                        deprecated=False,
                        nullable=False,
                        minimum=1.0,
                        maximum=100.0,
                        decimal_places=2,
                        allow_inf_nan=False,
                    ),
                    fjt.Field(
                        name='my_data_class',
                        type='Object',
                        summary='my_data_class param summary',
                        description='my_data_class param description',
                        properties={
                            'name': fjt.Field(name='name', type='String', summary='name param'),
                            'age': fjt.Field(name='age', type='Number', summary='age param'),
                            'extras': fjt.Field(
                                name='extras',
                                type='Object',
                                properties={
                                    'param1': fjt.Field(name='param1', type='String', summary='extras param1 param'),
                                    'param2': fjt.Field(
                                        name='param2',
                                        type='Object',
                                        properties={
                                            'param21': fjt.Field(
                                                name='param21', type='String', summary='extras param21 param'
                                            ),
                                            'param22': fjt.Field(
                                                name='param22', type='String', summary='extras param22 param'
                                            ),
                                        },
                                    ),
                                },
                            ),
                        },
                    ),
                ],
                returns=fjt.Field(
                    name='default',
                    type='Object',
                    summary='return summary',
                    description='return description',
                    properties={
                        'string': fjt.Field(
                            name='string',
                            type='String',
                            summary='string param summary',
                            description='string param description',
                            required=True,
                            deprecated=False,
                            nullable=False,
                            min_length=1,
                            max_length=10,
                            pattern='a-zA-Z',
                            max_digits=10,
                            examples=['Eve'],
                        ),
                        'integer': fjt.Field(
                            name='integer',
                            type='Number',
                            summary='integer param summary',
                            description='integer param description',
                            required=True,
                            deprecated=False,
                            nullable=False,
                            minimum=1,
                            maximum=100,
                            multiple_of=2,
                            allow_inf_nan=False,
                            examples=[1],
                        ),
                        'floating': fjt.Field(
                            name='floating',
                            type='Number',
                            summary='floating param summary',
                            description='floating param description',
                            required=True,
                            deprecated=False,
                            nullable=False,
                            minimum=1.0,
                            maximum=100.0,
                            decimal_places=2,
                            allow_inf_nan=False,
                            examples=[1.0],
                        ),
                        'my_data_class': fjt.Field(
                            name='my_data_class',
                            type='Object',
                            properties={
                                'name': fjt.Field(name='name', type='String', summary='name param'),
                                'age': fjt.Field(name='age', type='Number', summary='age param'),
                                'extras': fjt.Field(
                                    name='extras',
                                    type='Object',
                                    properties={
                                        'param1': fjt.Field(
                                            name='param1', type='String', summary='extras param1 param'
                                        ),
                                        'param2': fjt.Field(
                                            name='param2',
                                            type='Object',
                                            properties={
                                                'param21': fjt.Field(
                                                    name='param21', type='String', summary='extras param21 param'
                                                ),
                                                'param22': fjt.Field(
                                                    name='param22', type='String', summary='extras param22 param'
                                                ),
                                            },
                                        ),
                                    },
                                ),
                            },
                            examples=[
                                {
                                    'name': 'Lou',
                                    'age': 12,
                                    'extras': {'param1': 'Eve', 'param2': {'param21': 'Tequila', 'param22': 'Mya'}},
                                }
                            ],
                        ),
                    },
                ),
            )
        }
    )


def test_descriptor_describe_with_params_annotated_with_no_return() -> None:
    def view_func(string: str, integer: int, floating: float) -> None:
        return None

    annotations = {
        'string': t.Annotated[
            str,
            tp.Summary('string param summary'),
            tp.Description('string param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.MaxDigits(10),
            tp.MaxLength(10),
            tp.MinLength(1),
            tp.Pattern('a-zA-Z'),
        ],
        'integer': t.Annotated[
            int,
            tp.Summary('integer param summary'),
            tp.Description('integer param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.Maximum(100),
            tp.Minimum(1),
            tp.AllowInfNan(False),
        ],
        'floating': t.Annotated[
            float,
            tp.Summary('floating param summary'),
            tp.Description('floating param description'),
            tp.Required(),
            tp.Deprecated(False),
            tp.Nullable(False),
            tp.Maximum(100.0),
            tp.Minimum(1.0),
            tp.AllowInfNan(False),
            tp.DecimalPlaces(2),
        ],
        'return': t.Annotated[None, tp.Summary('return summary'), tp.Description('return description')],
    }
    setattr(view_func, 'jsonrpc_method_name', 'view_func')  # noqa: B010
    setattr(view_func, 'jsonrpc_method_sig', annotations.copy())  # noqa: B010
    setattr(view_func, 'jsonrpc_method_return', annotations.pop('return'))  # noqa: B010
    setattr(view_func, 'jsonrpc_method_params', annotations)  # noqa: B010
    setattr(view_func, 'jsonrpc_validate', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_notification', True)  # noqa: B010
    setattr(view_func, 'jsonrpc_options', {'notification': True, 'validate': True})  # noqa: B010

    mock_jsonrpc_site = MockJSONRPCSite()
    mock_jsonrpc_site.view_funcs = OrderedDict({'view_func': view_func})

    jsonrpc_serv_descriptor = JSONRPCServiceDescriptor(mock_jsonrpc_site)
    view_func_describe = jsonrpc_serv_descriptor.describe
    assert view_func_describe.jsonrpc_method_name == 'rpc.describe'
    assert view_func_describe.jsonrpc_method_sig == {'return': t.Annotated[fjt.ServiceDescribe, None]}
    assert view_func_describe.jsonrpc_method_return is t.Annotated[fjt.ServiceDescribe, None]
    assert view_func_describe.jsonrpc_method_params == {}
    assert (
        view_func_describe.jsonrpc_method_annotations
        == tm.MethodAnnotated[
            tm.Summary('RPC Describe'),
            tm.Description('Service description for JSON-RPC 2.0'),
            tm.Validate(False),
            tm.Notification(False),
        ]
    )
    assert view_func_describe.jsonrpc_validate is False
    assert view_func_describe.jsonrpc_notification is False
    assert view_func_describe.jsonrpc_options == {'notification': False, 'validate': False}

    describe = view_func_describe()
    assert describe.id == f'urn:uuid:{mock_jsonrpc_site.uuid}'
    assert describe.version == '1.0.0'
    assert describe.name == 'Flask-JSONRPC'
    assert describe.servers == [fjt.Server(url='/')]
    assert describe.methods == OrderedDict(
        {
            'view_func': fjt.Method(
                name='view_func',
                type='method',
                validation=True,
                notification=True,
                params=[
                    fjt.Field(
                        name='string',
                        type='String',
                        summary='string param summary',
                        description='string param description',
                        required=True,
                        deprecated=False,
                        nullable=False,
                        min_length=1,
                        max_length=10,
                        pattern='a-zA-Z',
                        max_digits=10,
                    ),
                    fjt.Field(
                        name='integer',
                        type='Number',
                        summary='integer param summary',
                        description='integer param description',
                        required=True,
                        deprecated=False,
                        nullable=False,
                        minimum=1,
                        maximum=100,
                        allow_inf_nan=False,
                    ),
                    fjt.Field(
                        name='floating',
                        type='Number',
                        summary='floating param summary',
                        description='floating param description',
                        required=True,
                        deprecated=False,
                        nullable=False,
                        minimum=1.0,
                        maximum=100.0,
                        decimal_places=2,
                        allow_inf_nan=False,
                    ),
                ],
                returns=fjt.Field(
                    name='default', type='Null', summary='return summary', description='return description'
                ),
            )
        }
    )
