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

from flask_jsonrpc import JSONRPCBlueprint


class MyException(Exception):
    pass


class MyExceptionWithCustomStatusCode(Exception):
    status_code = 409


class MyNotRegisteredException(Exception):
    pass


jsonrpc = JSONRPCBlueprint('error_handlers', __name__)


@jsonrpc.errorhandler(MyException)
def handle_my_exception(ex: MyException) -> dict[str, t.Any]:
    return {'message': 'It is a custom exception', 'code': '0001'}


@jsonrpc.errorhandler(MyExceptionWithCustomStatusCode)
def handle_my_exception_with_custom_status_code(ex: MyExceptionWithCustomStatusCode) -> tuple[dict[str, t.Any], int]:
    return {'message': 'It is a custom exception with status code', 'code': '0001'}, ex.status_code


@jsonrpc.method('error_handlers.failsWithCustomException')
def fails_with_custom_exception(_string: str | None = None) -> t.NoReturn:
    raise MyException('example of fail with custom exception that will be handled')


@jsonrpc.method('error_handlers.failsWithCustomExceptionWithStatusCode')
def fails_with_custom_exception_with_status_code(_string: str | None = None) -> t.NoReturn:
    raise MyExceptionWithCustomStatusCode('example of fail with custom exception with status code that will be handled')


@jsonrpc.method('error_handlers.failsWithCustomExceptionNotRegistered')
def fails_with_custom_exception_not_registered(_string: str | None = None) -> t.NoReturn:
    raise MyNotRegisteredException('example of fail with custom exception that will not be handled')
