# Copyright (c) 2025-2025, Cenobit Technologies, Inc. http://cenobit.es/
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
import flask_jsonrpc.types.params as tp
import flask_jsonrpc.types.methods as tm

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


jsonrpc = JSONRPCBlueprint('types__python_classes_annotated', __name__)


@jsonrpc.errorhandler(ColorNotFoundException)
def handle_color_not_found_exc(exc: ColorNotFoundException) -> ColorError:
    return exc.color_error


@jsonrpc.method(
    'types.python_classes_annotated.createColor',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create a new color'),
        tm.Description('This method creates a new color object with an auto-generated ID.'),
        tm.Tag(
            name='types',
            summary='Python classes related methods',
            description='Methods that demonstrate Python class objects in JSON-RPC.',
        ),
        tm.Example(
            name='Example of creating a color',
            summary='Create a color with name and tag',
            description='This demonstrates creating a Color object from a NewColor input.',
            params=[
                tm.ExampleField(
                    name='color',
                    value={'name': 'Red', 'tag': 'primary'},
                    description='A NewColor object with name and tag.',
                )
            ],
            returns=tm.ExampleField(
                name='result',
                value={'id': 1, 'name': 'Red', 'tag': 'primary'},
                description='The created Color object with ID.',
            ),
        ),
    ],
)
def create_color(
    color: t.Annotated[
        NewColor,
        tp.Summary('A new color object'),
        tp.Description('The color object to create, containing name and tag.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    Color,
    tp.Summary('The created color object'),
    tp.Description('A Color object with an auto-generated ID, name, and tag.'),
]:
    return Color(id=1, name=color.name, tag=color.tag)


@jsonrpc.method(
    'types.python_classes_annotated.createManyColor',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create many colors'),
        tm.Description('This method creates multiple color objects from a list and an optional single color.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of creating many colors',
            summary='Create multiple colors with optional extra color',
            description='This demonstrates creating multiple Color objects from a list of NewColor objects.',
            params=[
                tm.ExampleField(
                    name='colors',
                    value=[{'name': 'Red', 'tag': 'primary'}, {'name': 'Blue', 'tag': 'primary'}],
                    description='A list of NewColor objects.',
                ),
                tm.ExampleField(
                    name='color',
                    value={'name': 'Green', 'tag': 'secondary'},
                    description='An optional additional NewColor object.',
                ),
            ],
            returns=tm.ExampleField(
                name='result',
                value=[
                    {'id': 0, 'name': 'Red', 'tag': 'primary'},
                    {'id': 1, 'name': 'Blue', 'tag': 'primary'},
                    {'id': 2, 'name': 'Green', 'tag': 'secondary'},
                ],
                description='List of created Color objects with auto-generated IDs.',
            ),
        ),
    ],
)
def create_many_colors(
    colors: t.Annotated[
        list[NewColor],
        tp.Summary('List of new color objects'),
        tp.Description('A list of color objects to create.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
    color: t.Annotated[
        NewColor | None,
        tp.Summary('Optional additional color'),
        tp.Description('An optional additional color to add to the list.'),
        tp.Required(False),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    list[Color],
    tp.Summary('List of created color objects'),
    tp.Description('A list of Color objects with auto-generated IDs.'),
]:
    new_color = [Color(id=i, name=pet.name, tag=pet.tag) for i, pet in enumerate(colors)]
    if color is not None:
        return new_color + [Color(id=len(colors), name=color.name, tag=color.tag)]
    return new_color


@jsonrpc.method(
    'types.python_classes_annotated.createManyFixColor',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create many colors from dictionary'),
        tm.Description('This method creates multiple color objects from a dictionary where keys are color IDs.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of creating colors from dictionary',
            summary='Create colors with predefined IDs',
            description='This demonstrates creating Color objects from a dictionary of NewColor objects.',
            params=[
                tm.ExampleField(
                    name='colors',
                    value={'1': {'name': 'Red', 'tag': 'primary'}, '2': {'name': 'Blue', 'tag': 'primary'}},
                    description='A dictionary with string keys (color IDs) and NewColor values.',
                )
            ],
            returns=tm.ExampleField(
                name='result',
                value=[{'id': 1, 'name': 'Red', 'tag': 'primary'}, {'id': 2, 'name': 'Blue', 'tag': 'primary'}],
                description='List of created Color objects with IDs from dictionary keys.',
            ),
        ),
    ],
)
def create_many_fix_colors(
    colors: t.Annotated[
        dict[str, NewColor],
        tp.Summary('Dictionary of color ID to color object mapping'),
        tp.Description('A dictionary where keys are string color IDs and values are NewColor objects.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    list[Color],
    tp.Summary('List of created color objects'),
    tp.Description('A list of Color objects with IDs parsed from dictionary keys.'),
]:
    return [Color(id=int(color_id), name=color.name, tag=color.tag) for color_id, color in colors.items()]


@jsonrpc.method(
    'types.python_classes_annotated.removeColor',
    annotation=tm.MethodAnnotated[
        tm.Summary('Remove a color'),
        tm.Description('This method removes a color object. Throws an exception if color ID is greater than 10.'),
        tm.Tag('types'),
        tm.Error(code=-32001, message='Color not found', status_code=404),
        tm.Example(
            name='Example of removing a color',
            summary='Remove a color by providing the color object',
            description='This demonstrates removing a Color object. Returns the same object if successful.',
            params=[
                tm.ExampleField(
                    name='color',
                    value={'id': 5, 'name': 'Purple', 'tag': 'secondary'},
                    description='The Color object to remove.',
                )
            ],
            returns=tm.ExampleField(
                name='result',
                value={'id': 5, 'name': 'Purple', 'tag': 'secondary'},
                description='The removed Color object if successful.',
            ),
        ),
    ],
)
def remove_color(
    color: t.Annotated[
        Color | None,
        tp.Summary('Color object to remove'),
        tp.Description('The color object to remove. Can be null to test null handling.'),
        tp.Required(False),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    Color | None,
    tp.Summary('Removed color object'),
    tp.Description('The removed color object, or null if input was null.'),
    tp.Nullable(True),
]:
    if color is not None and color.id > 10:
        raise ColorNotFoundException(
            'Color not found',
            ColorError(color_id=color.id, reason='The color with an ID greater than 10 does not exist.'),
        )
    return color
