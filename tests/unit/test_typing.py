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
from collections import OrderedDict

from pydantic import ValidationError

import pytest

from flask_jsonrpc.typing import Error, Field, Method, Server, Example, ExampleField, ServiceDescribe


def test_field_model() -> None:
    field = Field(name='field1', type='string')

    assert field.name == 'field1'
    assert field.type == 'string'
    assert field.summary is None
    assert field.description is None
    assert field.properties is None
    assert field.examples is None
    assert field.required is None
    assert field.deprecated is None
    assert field.nullable is None
    assert field.minimum is None
    assert field.maximum is None
    assert field.multiple_of is None
    assert field.min_length is None
    assert field.max_length is None
    assert field.pattern is None
    assert field.allow_inf_nan is None
    assert field.max_digits is None
    assert field.decimal_places is None


def test_example_field_model() -> None:
    example_field = ExampleField(name='example1', value='example_value')

    assert example_field.name == 'example1'
    assert example_field.value == 'example_value'
    assert example_field.summary is None
    assert example_field.description is None


def test_example_model() -> None:
    example = Example(
        name='example1', params=None, summary='This is a summary', description='Description of example', returns=None
    )

    assert example.name == 'example1'
    assert example.params is None
    assert example.summary == 'This is a summary'
    assert example.description == 'Description of example'
    assert example.returns is None


def test_error_model() -> None:
    error = Error(code=400, message='Bad Request', data=None, status_code=400)

    assert error.code == 400
    assert error.message == 'Bad Request'
    assert error.data is None
    assert error.status_code == 400


def test_method_model_required_fields() -> None:
    method = Method(
        name='method1',
        type='method',
        validation=True,
        notification=True,
        params=[],
        returns=Field(name='return_field', type='string'),
    )

    assert method.name == 'method1'
    assert method.type == 'method'
    assert method.validation is True
    assert method.notification is True
    assert method.params == []
    assert method.returns.name == 'return_field'
    assert method.returns.type == 'string'


def test_method_model_optional_fields() -> None:
    method = Method(
        name='method1',
        type='method',
        validation=True,
        notification=True,
        params=[],
        returns=Field(name='return_field', type='string'),
        tags=['tag1', 'tag2'],
        errors=[Error(code=404, message='Not Found', data=None, status_code=404)],
        examples=[
            Example(
                name='example1', params=[], summary='Example summary', description='Example description', returns=None
            )
        ],
    )

    assert method.tags == ['tag1', 'tag2']
    assert method.errors is not None
    assert len(method.errors) == 1
    assert method.errors[0].code == 404
    assert method.examples is not None
    assert len(method.examples) == 1
    assert method.examples[0].name == 'example1'


def test_server_model() -> None:
    server = Server(url='http://example.com', description='Test Server')

    assert server.url == 'http://example.com'
    assert server.description == 'Test Server'


def test_service_describe_model() -> None:
    method1 = Method(
        name='method1',
        type='method',
        validation=True,
        notification=False,
        params=[Field(name='param1', type='string')],
        returns=Field(name='return_field', type='string'),
    )

    service = ServiceDescribe(
        id='service1',
        name='Test Service',
        version='1.0',
        title='My Test Service',
        description='A sample service',
        servers=[Server(url='http://server1.com')],
        methods=OrderedDict({'method1': method1}),
    )

    assert service.id == 'service1'
    assert service.name == 'Test Service'
    assert service.version == '1.0'
    assert service.title == 'My Test Service'
    assert service.description == 'A sample service'
    assert len(service.servers) == 1
    assert service.servers[0].url == 'http://server1.com'
    assert 'method1' in service.methods
    assert service.methods['method1'].name == 'method1'


def test_invalid_method() -> None:
    with pytest.raises(ValidationError):
        Method(name='method1', type='method', validation=True, notification=True, params=[], returns=None)


def test_invalid_service_describe() -> None:
    with pytest.raises(ValidationError):
        ServiceDescribe(
            id='service1',
            name='Invalid Service',
            version='1.0',
            servers=[Server(url='http://server1.com')],
            methods=OrderedDict({'invalid_method': 'not_a_method_object'}),
        )
