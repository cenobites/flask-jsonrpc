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
from __future__ import annotations

import typing as t
from operator import getitem
import itertools
from dataclasses import field, asdict, dataclass

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc.types.types import Types, Object

if t.TYPE_CHECKING:
    from flask_jsonrpc.types.types import JSONRPCNewType


@dataclass
class Node:
    """A node in a tree structure.

    Args:
        name (str | None): Name of the node.
        items (list[dict[str, typing.Any]]): List of items in the node.
        children (list[Node]): List of child nodes.

    Attributes:
        name (str | None): Name of the node.
        items (list[dict[str, typing.Any]]): List of items in the node.
        children (list[Node]): List of child nodes.

    Examples:
        >>> root = Node(name='root')
        >>> child1 = Node(name='child1')
        >>> child2 = Node(name='child2')
        >>> root.add_child(child1)
        >>> root.add_child(child2)
        >>> child1.insert_item({'name': 'item1'})
        >>> child2.insert_item({'name': 'item2'})
        >>> assert root.to_dict() == {
        ...     'name': 'root',
        ...     'items': [],
        ...     'children': [
        ...         {'name': 'child1', 'items': [{'name': 'item1'}], 'children': []},
        ...         {'name': 'child2', 'items': [{'name': 'item2'}], 'children': []},
        ...     ],
        ... }
        >>> root.find_child('child1').to_dict()
        {'name': 'child1', 'items': [{'name': 'item1'}], 'children': []}
        >>>
        >>> root.find_child('child3') is None
        True
        >>> root.clean()
        >>> root.sort()
        >>> assert root.to_dict() == {
        ...     'name': 'root',
        ...     'items': [],
        ...     'children': [
        ...         {'name': 'child1', 'items': [{'name': 'item1'}], 'children': []},
        ...         {'name': 'child2', 'items': [{'name': 'item2'}], 'children': []},
        ...     ],
        ... }
    """

    name: str | None
    items: list[dict[str, t.Any]] = field(default_factory=list)
    children: list[Node] = field(default_factory=list)

    def find_child(self: Self, name: str) -> Node | None:
        """Find a child node by name.

        Args:
            name (str): Name of the child node to find.

        Returns:
            Node | None: The child node if found, otherwise `None`.
        """
        for child in self.children:
            if child.name == name:
                return child
        return None

    def add_child(self: Self, node: Node) -> None:
        """Add a child node.

        Args:
            node (Node): Child node to add.
        """
        self.children.append(node)

    def insert_item(self: Self, val: dict[str, t.Any]) -> None:
        """Insert an item into the node.

        Args:
            val (dict[str, typing.Any]): Item to insert.
        """
        self.items.append(val)

    def clean(self: Self) -> None:
        """Clean the node by removing empty children."""
        for child in self.children:
            child.clean()
        self.children = [child for child in self.children if child.items or child.children]

    def sort(self: Self) -> None:
        """Sort the node's children and items by name."""

        def sort_by_name(n: Node) -> str:
            return n.name or ''

        self.children.sort(key=sort_by_name)
        self.items.sort(key=lambda i: i.get('name', ''))
        for child in self.children:
            child.sort()

    def to_dict(self: Self) -> dict[str, t.Any]:
        """Convert the node to a dictionary.

        Returns:
            dict[str, typing.Any]: Dictionary representation of the node.
        """
        return asdict(self)


def urn(name: str, *args: t.Any) -> str:  # noqa: ANN401
    """Return the URN name.

    Args:
        name (str): Name.
        *args (typing.Any): Additional name parts.

    Returns:
        str: URN name.

    Examples:
        >>> urn('python')
        'urn:python'
        >>> urn('python.flask')
        'urn:python:flask'
        >>> urn('python', 'Flask', 'JsonRPC')
        'urn:python:flask:jsonrpc'
        >>> urn('python', '/api/browse')
        'urn:python:api:browse'
        >>> urn(None)
        Traceback (most recent call last):
            ...
        ValueError: name is required
        >>> urn('')
        Traceback (most recent call last):
            ...
        ValueError: name is required
    """
    if not name:
        raise ValueError('name is required') from None
    splitted_params = [arg.replace('.', '/').replace(':', '/').split('/') for arg in [name] + list(args)]
    values = ['urn'] + [st for st in list(itertools.chain(*splitted_params)) if st != '']
    return ':'.join(values).lower()


def from_python_type(tp: t.Any, default: JSONRPCNewType | None = Object) -> JSONRPCNewType | None:  # noqa: ANN401
    """Convert Python type to JSONRPCNewType.

    Args:
        tp (typing.Any): Python type.
        default (flask_jsonrpc.types.types.JSONRPCNewType | None, optional): Default type if no match is found.
            Defaults to Object.

    Returns:
        flask_jsonrpc.types.types.JSONRPCNewType | None: Corresponding JSONRPCNewType or `default`.

    Examples:
        >>> str(from_python_type(str))
        'String'
        >>> str(from_python_type(int))
        'Number'
        >>> str(from_python_type(dict))
        'Object'
        >>> str(from_python_type(list))
        'Array'
        >>> str(from_python_type(bool))
        'Boolean'
        >>> str(from_python_type(None))
        'Null'
        >>> str(from_python_type(t.NoReturn))
        'Null'
    """
    for typ in Types:
        if typ.check_type(tp):
            return typ
    return default


def get(obj: t.Any, path: str, default: t.Any = None) -> t.Any:  # noqa: ANN401
    """Get the value at any depth of a nested object based on the path
    described by `path`. If path doesn't exist, `default` is returned.

    Args:
        obj (dict): Object to process.
        path (str): List or `.` delimited string of path describing path.

    Keyword Arguments:
        default (typing.Any): Default value to return if path doesn't exist.
        Defaults to ``None``.

    Returns:
        typing.Any: Value of `obj` at path.

    Examples:
        >>> get(None, 'a')

        >>> get(None, 'a', 'default')
        'default'
        >>> get('a', 'a.b.c', 'default')
        'default'
        >>> get({'a': 1}, 'a')
        1
        >>> get({'a': 1}, 'b')

        >>> get({'a': 1}, 'b', 'default')
        'default'
        >>> get({'a': {'b': {'c': 1}}}, 'a.b.c')
        1
        >>> get({}, 'a.b.c')

        >>> get([], 'a.b.c')

        >>> get([], 'a.b.c', None)

    """
    if obj is None:
        return default
    if not isinstance(obj, dict):
        return default
    if path in obj:
        return getitem(obj, path)

    obj_val = obj
    keys = path.split('.')
    try:
        for key in keys:
            obj_val = getitem(obj_val, key)
    except (TypeError, KeyError):
        return default
    return obj_val
