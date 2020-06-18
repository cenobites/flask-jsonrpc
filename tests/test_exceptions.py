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
from flask_jsonrpc.exceptions import (
    ParseError,
    ServerError,
    JSONRPCError,
    InternalError,
    InvalidParamsError,
    InvalidRequestError,
    MethodNotFoundError,
)


def test_jsonrpc_error():
    error = JSONRPCError(message="I'm a teapot", code=-32768, data={'data': [1, 2, 3]}, status_code=418)
    assert error.code == -32768
    assert error.message == "I'm a teapot"
    assert error.data == {'data': [1, 2, 3]}
    assert error.status_code == 418
    assert error.jsonrpc_format == {
        'code': -32768,
        'data': {'data': [1, 2, 3]},
        'message': "I'm a teapot",
        'name': 'JSONRPCError',
    }


def test_jsonrpc_error_with_default_params():
    error = JSONRPCError()
    assert error.code == 0
    assert error.message is None
    assert error.data is None
    assert error.status_code == 400
    assert error.jsonrpc_format == {
        'code': 0,
        'data': None,
        'message': None,
        'name': 'JSONRPCError',
    }


def test_parser_error():
    error = ParseError()
    assert error.code == -32700
    assert error.message == 'Parse error'
    assert error.data is None
    assert error.status_code == 400
    assert error.jsonrpc_format == {
        'code': -32700,
        'data': None,
        'message': 'Parse error',
        'name': 'ParseError',
    }


def test_invalid_request_error():
    error = InvalidRequestError()
    assert error.code == -32600
    assert error.message == 'Invalid Request'
    assert error.data is None
    assert error.status_code == 400
    assert error.jsonrpc_format == {
        'code': -32600,
        'data': None,
        'message': 'Invalid Request',
        'name': 'InvalidRequestError',
    }


def test_method_not_found_error():
    error = MethodNotFoundError()
    assert error.code == -32601
    assert error.message == 'Method not found'
    assert error.data is None
    assert error.status_code == 400
    assert error.jsonrpc_format == {
        'code': -32601,
        'data': None,
        'message': 'Method not found',
        'name': 'MethodNotFoundError',
    }


def test_invalid_params_error():
    error = InvalidParamsError()
    assert error.code == -32602
    assert error.message == 'Invalid params'
    assert error.data is None
    assert error.status_code == 400
    assert error.jsonrpc_format == {
        'code': -32602,
        'data': None,
        'message': 'Invalid params',
        'name': 'InvalidParamsError',
    }


def test_internal_error():
    error = InternalError()
    assert error.code == -32603
    assert error.message == 'Internal error'
    assert error.data is None
    assert error.status_code == 400
    assert error.jsonrpc_format == {
        'code': -32603,
        'data': None,
        'message': 'Internal error',
        'name': 'InternalError',
    }


def test_server_error():
    error = ServerError()
    assert error.code == -32000
    assert error.message == 'Server error'
    assert error.data is None
    assert error.status_code == 500
    assert error.jsonrpc_format == {
        'code': -32000,
        'data': None,
        'message': 'Server error',
        'name': 'ServerError',
    }
