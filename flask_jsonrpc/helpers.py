# -*- coding: utf-8 -*-
# Copyright (c) 2020-2020, Cenobit Technologies, Inc. http://cenobit.es/
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
import itertools
from typing import TYPE_CHECKING, Any, Dict
from operator import getitem

from .types import Types, Object

if TYPE_CHECKING:
    from .types import JSONRPCNewType


def urn(name: str, *args: Any) -> str:
    """Return the URN name.

    >>> urn('python')
    'urn::python'
    >>> urn('python', 'Flask', 'JsonRPC')
    'urn::python:flask.jsonrpc'
    >>> urn('python', '/api/browse')
    'urn::python:api.browse'
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
        raise ValueError('name is required')
    splited_args = [arg.split('/') for arg in args]
    st = '.'.join(list(itertools.chain(*splited_args)))
    st = st.rstrip('.').lstrip('.')
    sep = ':' if len(args) > 0 else ''
    return 'urn::{0}{1}{2}'.format(name, sep, st.replace('..', '.')).lower()


def from_python_type(tp: Any) -> 'JSONRPCNewType':
    """Convert Python type to JSONRPCNewType.

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
    """
    for t in Types:
        if t.check_type(tp):
            return t
    return Object


def get(obj: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Get the value at any depth of a nested object based on the path
    described by `path`. If path doesn't exist, `default` is returned.
    Args:
        obj (dict): Object to process.
        path (str): List or ``.`` delimited string of path describing
            path.
    Keyword Arguments:
        default (mixed): Default value to return if path doesn't exist.
            Defaults to ``None``.
    Returns:
        mixed: Value of `obj` at path.

    Example:

    >>> get(None, 'a')

    >>> get(None, 'a', 'default')
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

    obj_val = obj
    keys = path.split('.')
    for key in keys:
        try:
            obj_val = getitem(obj_val, key)
        except KeyError:
            return default
    return obj_val


if __name__ == '__main__':
    import doctest

    doctest.testmod()
