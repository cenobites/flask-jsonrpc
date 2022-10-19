# Copyright (c) 2020-2022, Cenobit Technologies, Inc. http://cenobit.es/
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

import pytest

from flask_jsonrpc.helpers import urn, from_python_type


def test_urn():
    with pytest.raises(ValueError, match='name is required'):
        urn(None)
    with pytest.raises(ValueError, match='name is required'):
        urn('')
    assert urn('a', 'b', 'c', 'd') == 'urn:a:b:c:d'


def test_from_python_type():
    assert str(from_python_type(str)) == 'String'
    assert str(from_python_type(t.AnyStr)) == 'String'
    assert str(from_python_type(int)) == 'Number'
    assert str(from_python_type(float)) == 'Number'
    assert str(from_python_type(dict)) == 'Object'
    assert str(from_python_type(list)) == 'Array'
    assert str(from_python_type(tuple)) == 'Array'
    assert str(from_python_type(bool)) == 'Boolean'
    assert str(from_python_type(type(None))) == 'Null'
