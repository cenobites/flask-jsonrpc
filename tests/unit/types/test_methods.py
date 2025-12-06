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
import typing as t
import operator

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
    BaseMethodAnnotatedOrigin,
    _MethodAnnotated,
    _MethodAnnotatedAlias,
    _MethodAnnotatedProxy,
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
    _MethodAnnotated()


def test_methodannotated_class_getitem() -> None:
    annotated = _MethodAnnotated[Summary, Description]
    assert isinstance(annotated, t._GenericAlias)  # type: ignore


def test_methodannotatedproxy_instantiation() -> None:
    _MethodAnnotatedProxy()


def test_methodannotatedproxy_getitem() -> None:
    proxy = _MethodAnnotatedProxy()
    annotated = proxy[Summary(summary='Test summary')]
    assert isinstance(annotated, t._GenericAlias)  # type: ignore


def test_methodannotatedproxy_getitem_tuple() -> None:
    proxy = _MethodAnnotatedProxy()
    summary = Summary(summary='Test summary')
    description = Description(description='Test description')
    annotated = proxy[(summary, description)]

    assert isinstance(annotated, t._GenericAlias)  # type: ignore
    assert isinstance(annotated, _MethodAnnotatedAlias)
    assert len(annotated.__metadata__) == 2
    assert summary in annotated.__metadata__
    assert description in annotated.__metadata__


def test_methodannotatedalias_init_with_origin_and_metadata() -> None:
    summary = Summary(summary='Test summary')
    description = Description(description='Test description')
    alias = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary, description))

    assert alias.origin == BaseMethodAnnotatedOrigin
    assert alias.metadata == (summary, description)
    assert alias.__metadata__ == (summary, description)
    assert alias.__origin__ == BaseMethodAnnotatedOrigin


def test_methodannotatedalias_init_with_nested_alias_basic() -> None:
    sum_meta = Summary(summary='First summary')
    first = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (sum_meta,))

    val_meta = Validate(validate=True)
    second = _MethodAnnotatedAlias(first, (val_meta,))  # type: ignore[arg-type]

    assert second.origin == BaseMethodAnnotatedOrigin
    assert second.__metadata__ == (sum_meta, val_meta)
    assert len(second.__metadata__) == 2


def test_methodannotatedalias_repr() -> None:
    summary = Summary(summary='Test summary')
    description = Description(description='Test description')
    alias = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary, description))

    repr_str = repr(alias)
    assert 'flask_jsonrpc.types.methods._MethodAnnotated' in repr_str
    assert 'BaseMethodAnnotatedOrigin' in repr_str
    assert "summary='Test summary'" in repr_str
    assert "description='Test description'" in repr_str


def test_methodannotatedalias_reduce() -> None:
    summary = Summary(summary='Test summary')
    description = Description(description='Test description')
    alias = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary, description))

    reduced = alias.__reduce__()
    assert len(reduced) == 2
    assert reduced[0] == operator.getitem
    assert reduced[1][0] == _MethodAnnotated
    assert reduced[1][1] == (BaseMethodAnnotatedOrigin, summary, description)


def test_methodannotatedalias_eq_same_origin_and_metadata() -> None:
    summary = Summary(summary='Test summary')
    description = Description(description='Test description')

    alias1 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary, description))
    alias2 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary, description))

    assert alias1 == alias2


def test_methodannotatedalias_eq_different_metadata() -> None:
    summary1 = Summary(summary='Test summary 1')
    summary2 = Summary(summary='Test summary 2')

    alias1 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary1,))
    alias2 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary2,))

    assert alias1 != alias2


def test_methodannotatedalias_eq_different_origin() -> None:
    class CustomOrigin(BaseMethodAnnotatedOrigin):
        pass

    summary = Summary(summary='Test summary')

    alias1 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary,))
    alias2 = _MethodAnnotatedAlias(CustomOrigin, (summary,))

    assert alias1 != alias2


def test_methodannotatedalias_eq_not_alias_type() -> None:
    summary = Summary(summary='Test summary')
    alias = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary,))

    result = alias.__eq__('not an alias')
    assert result == NotImplemented

    result = alias.__eq__(42)
    assert result == NotImplemented

    result = alias.__eq__(None)
    assert result == NotImplemented


def test_methodannotatedalias_hash() -> None:
    summary = Summary(summary='Test summary')
    description = Description(description='Test description')

    alias1 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary, description))
    alias2 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary, description))

    assert hash(alias1) == hash(alias2)

    alias_set = {alias1, alias2}
    assert len(alias_set) == 1


def test_methodannotatedalias_hash_different_metadata() -> None:
    summary1 = Summary(summary='Test summary 1')
    summary2 = Summary(summary='Test summary 2')

    alias1 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary1,))
    alias2 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (summary2,))

    assert hash(alias1) != hash(alias2)

    alias_set = {alias1, alias2}
    assert len(alias_set) == 2


def test_methodannotatedalias_with_multiple_metadata_types() -> None:
    summary = Summary(summary='Test summary')
    description = Description(description='Test description')
    validate = Validate(validate=False)
    notification = Notification(notification=True)
    deprecated = Deprecated(deprecated=True)
    tag = Tag(name='test-tag', summary='Tag summary')
    error = Error(code=404, message='Not found', status_code=404)

    alias = _MethodAnnotatedAlias(
        BaseMethodAnnotatedOrigin, (summary, description, validate, notification, deprecated, tag, error)
    )

    assert len(alias.metadata) == 7
    assert summary in alias.metadata
    assert description in alias.metadata
    assert validate in alias.metadata
    assert notification in alias.metadata
    assert deprecated in alias.metadata
    assert tag in alias.metadata
    assert error in alias.metadata


def test_methodannotatedalias_empty_metadata() -> None:
    alias = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, ())

    assert alias.origin == BaseMethodAnnotatedOrigin
    assert alias.metadata == ()
    assert alias.__metadata__ == ()


def test_methodannotatedalias_chained_nesting_complete() -> None:
    sum_meta = Summary(summary='Summary chained')
    desc_meta = Description(description='Description chained')
    val_meta = Validate(validate=True)
    notif_meta = Notification(notification=False)

    a1 = _MethodAnnotatedAlias(BaseMethodAnnotatedOrigin, (sum_meta,))
    assert len(a1.__metadata__) == 1
    assert sum_meta in a1.__metadata__

    a2 = _MethodAnnotatedAlias(a1, (desc_meta,))  # type: ignore[arg-type]
    assert len(a2.__metadata__) == 2
    assert sum_meta in a2.__metadata__
    assert desc_meta in a2.__metadata__

    a3 = _MethodAnnotatedAlias(a2, (val_meta,))  # type: ignore[arg-type]
    assert len(a3.__metadata__) == 3
    assert sum_meta in a3.__metadata__
    assert desc_meta in a3.__metadata__
    assert val_meta in a3.__metadata__

    a4 = _MethodAnnotatedAlias(a3, (notif_meta,))  # type: ignore[arg-type]
    assert len(a4.__metadata__) == 4
    assert sum_meta in a4.__metadata__
    assert desc_meta in a4.__metadata__
    assert val_meta in a4.__metadata__
    assert notif_meta in a4.__metadata__
