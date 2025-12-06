# Copyright (c) 2012-2025, Cenobit Technologies, Inc. http://cenobit.es/
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

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc import JSONRPCBlueprint

user = JSONRPCBlueprint('user', __name__)


class UserException(Exception):
    def __init__(self: Self, *args: object) -> None:
        super().__init__(*args)


class UserNotFoundException(UserException):
    def __init__(self: Self, message: str, user_id: int) -> None:
        super().__init__(message)
        self.user_id = user_id


class User:
    def __init__(self: Self, id: int, name: str) -> None:
        self.id = id
        self.name = name


def handle_user_not_found_exception(ex: UserNotFoundException) -> dict[str, t.Any]:
    return {'message': f'User {ex.user_id} not found', 'code': '1001'}


user.register_error_handler(UserNotFoundException, handle_user_not_found_exception)


@user.method('User.index')
def index() -> str:
    return 'Welcome to User API'


@user.method('User.getUser')
def get_user(id: int) -> User:
    if id > 10:
        raise UserNotFoundException('User not found', user_id=id)
    return User(id, 'Founded')


@user.method('User.removeUser')
def remove_user(id: int) -> User:
    if id > 10:
        raise ValueError('User not found')
    return User(id, 'Removed')
