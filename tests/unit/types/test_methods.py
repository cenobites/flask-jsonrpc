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
import typing_extensions

import pytest

from flask_jsonrpc.types.methods import (
    Tag,
    Error,
    Example,
    Summary,
    Validate,
    Deprecated,
    Description,
    ExampleField,
    Notification,
    MethodAnnotated,
)


def test_summary_dataclass() -> None:
    summary = Summary(summary='This is a summary')
    assert summary.summary == 'This is a summary'


def test_description_dataclass() -> None:
    description = Description(description='This is a description')
    assert description.description == 'This is a description'


def test_validate_dataclass() -> None:
    validate = Validate(validate=True)
    assert validate.validate is True


def test_notification_dataclass() -> None:
    notification = Notification(notification=True)
    assert notification.notification is True


def test_deprecated_dataclass() -> None:
    deprecated = Deprecated(deprecated=True)
    assert deprecated.deprecated is True


def test_tag_dataclass() -> None:
    tag = Tag(name='example', summary='Example summary', description='Example description')
    assert tag.name == 'example'
    assert tag.summary == 'Example summary'
    assert tag.description == 'Example description'


def test_example_field() -> None:
    field = ExampleField(name='field1', value='Some value', summary='Field summary', description='Field description')
    assert field.name == 'field1'
    assert field.value == 'Some value'
    assert field.summary == 'Field summary'
    assert field.description == 'Field description'


def test_example() -> None:
    field1 = ExampleField(name='param1', value='Value1')
    field2 = ExampleField(name='param2', value='Value2')
    example = Example(
        name='example1',
        params=[field1, field2],
        summary='Example summary',
        description='Example description',
        returns=field1,
    )

    assert example.name == 'example1'
    assert example.params == [field1, field2]
    assert example.summary == 'Example summary'
    assert example.description == 'Example description'
    assert example.returns == field1


def test_error() -> None:
    error = Error(code=404, message='Not found', status_code=404)
    assert error.code == 404
    assert error.message == 'Not found'
    assert error.status_code == 404
    assert error.data is None


def test_methodannotated_instantiation() -> None:
    with pytest.raises(TypeError):
        MethodAnnotated()


def test_methodannotated_class_getitem() -> None:
    annotated = MethodAnnotated[Summary, Description]
    assert isinstance(annotated, typing_extensions._AnnotatedAlias)  # type: ignore


def test_methodannotated_raises_exception_when_is_subclass() -> None:
    with pytest.raises(TypeError):

        class NewAnnotated(MethodAnnotated):
            pass


def test_methodannotated_with_no_tuple_as_param() -> None:
    MethodAnnotated['Only one param']
