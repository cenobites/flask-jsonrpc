# The MIT License (MIT)
#
# Copyright (c) 2017-2019 Ivan Levkivskyi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Code from: https://github.com/ilevkivskyi/typing_inspect
import sys
from typing import List, Tuple, Union, Generic, TypeVar

from flask_jsonrpc.typing_inspect import get_origin

NEW_TYPING = sys.version_info[:3] >= (3, 7, 0)  # PEP 560


# Does this raise an exception ?
#      from typing import ClassVar
if sys.version_info < (3, 5, 3):
    WITH_CLASSVAR = False
else:
    from typing import ClassVar

    WITH_CLASSVAR = True

# Does this raise an exception ?
#   Tuple[T][int]
#   List[Tuple[T]][int]
if sys.version_info[:3] == (3, 5, 3) or sys.version_info[:3] < (3, 5, 2):
    GENERIC_TUPLE_PARAMETRIZABLE = False
else:
    GENERIC_TUPLE_PARAMETRIZABLE = True


def test_origin():
    T = TypeVar('T')
    assert get_origin(int) is None
    if WITH_CLASSVAR:
        assert get_origin(ClassVar[int]) is None
    assert get_origin(Generic) is Generic
    assert get_origin(Generic[T]) is Generic
    assert get_origin(Union[int, float]) is Union
    if GENERIC_TUPLE_PARAMETRIZABLE:
        tp = List[Tuple[T, T]][int]
        assert get_origin(tp) is list if NEW_TYPING else List
