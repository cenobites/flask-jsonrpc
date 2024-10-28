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

if t.TYPE_CHECKING:
    from requests import Session


def test_app_decorators(session: 'Session', api_url: str) -> None:
    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.decorator', 'params': ['Python']}
    rv = session.post(f'{api_url}/decorators', json=data)
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'}
    assert rv.status_code == 200

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.decorator', 'params': 'Python'}
    rv = session.post(f'{api_url}/decorators', json=data)
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'Parameter structures are by-position (list) or by-name (dict): Python'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.decorator', 'params': [1]}
    rv = session.post(f'{api_url}/decorators', json=data)
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'argument "string" (int) is not an instance of str'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400


def test_app_decorators_wrapped(session: 'Session', api_url: str) -> None:
    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.wrappedDecorator', 'params': ['Python']}
    rv = session.post(f'{api_url}/decorators', json=data)
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello Python from decorator, ;)'}
    assert rv.status_code == 200

    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.wrappedDecorator', 'params': 'Python'}
    rv = session.post(f'{api_url}/decorators', json=data)
    assert rv.json() == {
        'id': 1,
        'jsonrpc': '2.0',
        'error': {
            'code': -32602,
            'data': {'message': 'Parameter structures are by-position (list) or by-name (dict): Python'},
            'message': 'Invalid params',
            'name': 'InvalidParamsError',
        },
    }
    assert rv.status_code == 400

    # XXX: Typeguard does not instrument wrapped functions
    data = {'id': 1, 'jsonrpc': '2.0', 'method': 'jsonrpc.wrappedDecorator', 'params': [1]}
    rv = session.post(f'{api_url}/decorators', json=data)
    assert rv.json() == {'id': 1, 'jsonrpc': '2.0', 'result': 'Hello 1 from decorator, ;)'}
    assert rv.status_code == 200
