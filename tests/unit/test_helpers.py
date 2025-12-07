# Copyright (c) 2020-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
from dataclasses import dataclass

from pydantic.main import BaseModel

import pytest

from flask_jsonrpc.helpers import Node, get, urn, from_python_type


def test_basic_tree() -> None:
    root = Node(name='root')
    child1 = Node(name='child1')
    child2 = Node(name='child2')
    grandchild1 = Node(name='grandchild1')

    root.add_child(child2)
    root.add_child(child1)
    child1.add_child(grandchild1)

    assert root.find_child('root') is None
    assert root.find_child('child1') == child1
    assert root.find_child('child2') == child2
    assert root.find_child('grandchild1') is None
    assert child1.find_child('grandchild1') == grandchild1
    assert root.find_child('nonexistent') is None

    assert root.to_dict() == {
        'name': 'root',
        'items': [],
        'children': [
            {'name': 'child2', 'items': [], 'children': []},
            {'name': 'child1', 'items': [], 'children': [{'name': 'grandchild1', 'items': [], 'children': []}]},
        ],
    }

    root.sort()
    assert root.to_dict() == {
        'name': 'root',
        'items': [],
        'children': [
            {'name': 'child1', 'items': [], 'children': [{'name': 'grandchild1', 'items': [], 'children': []}]},
            {'name': 'child2', 'items': [], 'children': []},
        ],
    }

    root.add_child(Node(name=''))
    root.add_child(Node(name='child0'))
    assert root.to_dict() == {
        'name': 'root',
        'items': [],
        'children': [
            {'name': 'child1', 'items': [], 'children': [{'name': 'grandchild1', 'items': [], 'children': []}]},
            {'name': 'child2', 'items': [], 'children': []},
            {'name': '', 'items': [], 'children': []},
            {'name': 'child0', 'items': [], 'children': []},
        ],
    }

    root.clean()
    assert root.to_dict() == {'name': 'root', 'items': [], 'children': []}

    root.add_child(child1)
    child1.insert_item({'key': 'value'})
    root.clean()
    assert root.to_dict() == {
        'name': 'root',
        'items': [],
        'children': [{'name': 'child1', 'items': [{'key': 'value'}], 'children': []}],
    }


def test_complex_tree() -> None:
    root = Node(name=None)
    node_a = Node(name='A')
    node_a.insert_item({'a1': 'example_value'})
    node_a.insert_item({'a2': 123})
    node_b = Node(name='B')
    node_b.insert_item({'b1': True})
    node_c = Node(name='C')
    node_c.insert_item({'c1': [1, 2, 3]})
    node_c.insert_item({'c2': {'nested_key': 'nested_value'}})
    node_d = Node(name='D')
    node_d.insert_item({'d1': 3.14})
    node_e = Node(name='E')
    node_e.insert_item({'e1': None})
    node_e.insert_item({'e2': 'value_e2'})
    node_e.insert_item({'e3': 42})

    root.add_child(node_b)
    root.add_child(node_a)
    node_a.add_child(node_d)
    node_a.add_child(node_c)
    node_c.add_child(node_e)

    root.sort()
    assert root.to_dict() == {
        'name': None,
        'items': [],
        'children': [
            {
                'name': 'A',
                'items': [{'a1': 'example_value'}, {'a2': 123}],
                'children': [
                    {
                        'name': 'C',
                        'items': [{'c1': [1, 2, 3]}, {'c2': {'nested_key': 'nested_value'}}],
                        'children': [
                            {'name': 'E', 'items': [{'e1': None}, {'e2': 'value_e2'}, {'e3': 42}], 'children': []}
                        ],
                    },
                    {'name': 'D', 'items': [{'d1': 3.14}], 'children': []},
                ],
            },
            {'name': 'B', 'items': [{'b1': True}], 'children': []},
        ],
    }


def test_urn_valid_name() -> None:
    assert urn('a', 'b', 'c', 'd') == 'urn:a:b:c:d'


def test_urn_valid_name_and_no_args() -> None:
    assert urn('example') == 'urn:example'


def test_urn_valid_name_with_single_arg() -> None:
    assert urn('example', 'path/to/resource') == 'urn:example:path:to:resource'


def test_urn_valid_name_with_multiple_args() -> None:
    assert urn('example', 'path/to/resource', 'another/path') == 'urn:example:path:to:resource:another:path'


def test_urn_valid_name_with_empty_string_arg() -> None:
    assert urn('example', '') == 'urn:example'


def test_urn_valid_name_with_leading_trailing_slashes() -> None:
    assert urn('example', '/path/to/resource/') == 'urn:example:path:to:resource'


def test_urn_valid_name_with_multiple_slashes() -> None:
    assert urn('example', 'path//to//resource') == 'urn:example:path:to:resource'


def test_urn_valid_name_with_empty_parts() -> None:
    assert urn('example', 'path//to//resource//') == 'urn:example:path:to:resource'


def test_urn_valid_name_with_special_characters() -> None:
    assert urn('example', 'path/with/special!@#$%&*()chars') == 'urn:example:path:with:special!@#$%&*()chars'


def test_urn_invalid_name() -> None:
    with pytest.raises(ValueError, match='name is required'):
        urn(None)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError, match='name is required'):
        urn('')


def test_urn_combined_slashes() -> None:
    assert urn('example', 'path///to///resource') == 'urn:example:path:to:resource'


def test_urn_leading_trailing_colons() -> None:
    assert urn('example', '::path::to::resource::') == 'urn:example:path:to:resource'


def test_urn_case_insensitivity() -> None:
    assert urn('Example') == 'urn:example'


def test_from_python_type_simple() -> None:
    assert str(from_python_type(str)) == 'String'
    assert str(from_python_type(t.AnyStr)) == 'String'
    assert str(from_python_type(int)) == 'Number'
    assert str(from_python_type(float)) == 'Number'
    assert str(from_python_type(dict)) == 'Object'
    assert str(from_python_type(list)) == 'Array'
    assert str(from_python_type(tuple)) == 'Array'
    assert str(from_python_type(bool)) == 'Boolean'
    assert str(from_python_type(type(None))) == 'Null'
    assert str(from_python_type(type)) == 'Object'
    assert str(from_python_type(t.NoReturn)) == 'Null'


def test_from_python_type_with_pure_class() -> None:
    class ClassTest:
        attr1: str
        attr2: int

    assert str(from_python_type(ClassTest)) == 'Object'
    assert str(from_python_type(t.Union[ClassTest, None])) == 'Object'  # noqa: UP007,UP045
    assert str(from_python_type(t.Optional[ClassTest])) == 'Object'  # noqa: UP007,UP045
    assert str(from_python_type(t.Optional[ClassTest], default=None)) == 'None'  # noqa: UP007,UP045

    assert str(from_python_type(ClassTest | None)) == 'Object'
    assert str(from_python_type(ClassTest | None, default=None)) == 'None'


def test_from_python_type_with_dataclass() -> None:
    @dataclass
    class ClassTest:
        attr1: str
        attr2: int

    assert str(from_python_type(ClassTest)) == 'Object'


def test_from_python_type_with_pydantic_model() -> None:
    class ClassTest(BaseModel):
        attr1: str
        attr2: int

    assert str(from_python_type(ClassTest)) == 'Object'


def test_get_none_obj() -> None:
    assert get(None, 'a') is None
    assert get(None, 'a', 'default') == 'default'


def test_get_non_dict_obj() -> None:
    assert get('a', 'a.b.c', 'default') == 'default'
    assert get([], 'a.b.c', 'default') == 'default'
    assert get(123, 'a.b.c', 'default') == 'default'


def test_get_existing_key() -> None:
    obj = {'a': 1}
    assert get(obj, 'a') == 1
    assert get(obj, 'b', 'default') == 'default'


def test_get_nested_keys() -> None:
    obj = {'a': {'b': {'c': 1}}}
    assert get(obj, 'a.b.c') == 1
    assert get(obj, 'a.b.d', 'default') == 'default'
    assert get(obj, 'a.d.c', 'default') == 'default'


def test_get_empty_dict() -> None:
    assert get({}, 'a.b.c') is None
    assert get({}, 'a.b.c', 'default') == 'default'


def test_get_empty_list() -> None:
    assert get([], 'a.b.c') is None
    assert get([], 'a.b.c', 'default') == 'default'


def test_get_complex_structure() -> None:
    obj = {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
    assert get(obj, 'a.b.c') == 1
    assert get(obj, 'a.b.d') == 2
    assert get(obj, 'e') == 3
    assert get(obj, 'a.b.e', 'default') == 'default'


def test_get_with_non_existent_path() -> None:
    obj = {'x': {'y': 5}}
    assert get(obj, 'x.y') == 5
    assert get(obj, 'x.z', 'default') == 'default'
    assert get(obj, 'a.b.c', 'default') == 'default'


def test_get_with_special_characters() -> None:
    obj = {'a.b': {'c.d': 1}}
    assert get(obj, 'a.b.c.d', 'default') == 'default'
    assert get(obj, 'a.b', 'default') == {'c.d': 1}
