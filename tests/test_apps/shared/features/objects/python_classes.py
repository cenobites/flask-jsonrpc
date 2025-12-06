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

from flask_jsonrpc import JSONRPCBlueprint

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class NewColor:
    name: str
    tag: str

    def __init__(self: Self, name: str, tag: str) -> None:
        self.name = name
        self.tag = tag


class Color(NewColor):
    id: int

    def __init__(self: Self, id: int, name: str, tag: str) -> None:
        super().__init__(name, tag)
        self.id = id


class ColorError:
    def __init__(self: Self, color_id: int, reason: str) -> None:
        self.color_id = color_id
        self.reason = reason


class ColorException(Exception):
    def __init__(self: Self, *args: object) -> None:
        super().__init__(*args)


class ColorNotFoundException(ColorException):
    def __init__(self: Self, message: str, color_error: ColorError) -> None:
        super().__init__(message)
        self.message = message
        self.color_error = color_error


jsonrpc = JSONRPCBlueprint('objects__python_classes', __name__)


@jsonrpc.errorhandler(ColorNotFoundException)
def handle_color_not_found_exc(exc: ColorNotFoundException) -> ColorError:
    return exc.color_error


@jsonrpc.method('objects.python_classes.createColor')
def create_color(color: NewColor) -> Color:
    return Color(id=1, name=color.name, tag=color.tag)


@jsonrpc.method('objects.python_classes.createManyColor')
def create_many_colors(colors: list[NewColor], color: NewColor | None = None) -> list[Color]:
    new_color = [Color(id=i, name=pet.name, tag=pet.tag) for i, pet in enumerate(colors)]
    if color is not None:
        return new_color + [Color(id=len(colors), name=color.name, tag=color.tag)]
    return new_color


@jsonrpc.method('objects.python_classes.createManyFixColor')
def create_many_fix_colors(colors: dict[str, NewColor]) -> list[Color]:
    return [Color(id=int(color_id), name=color.name, tag=color.tag) for color_id, color in colors.items()]


@jsonrpc.method('objects.python_classes.removeColor')
def remove_color(color: Color | None = None) -> Color | None:
    if color is not None and color.id > 10:
        raise ColorNotFoundException(
            'Color not found',
            ColorError(color_id=color.id, reason='The color with an ID greater than 10 does not exist.'),
        )
    return color
