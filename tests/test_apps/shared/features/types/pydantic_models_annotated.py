# Copyright (c) 2025-2025 , Cenobit Technologies, Inc. http://cenobit.es/
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

from pydantic.main import BaseModel

from flask_jsonrpc import JSONRPCBlueprint
import flask_jsonrpc.types.params as tp
import flask_jsonrpc.types.methods as tm

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class NewPet(BaseModel):
    name: str
    tag: str


class Pet(NewPet):
    id: int


class PetError(BaseModel):
    pet_id: int
    reason: str


class PetException(Exception):
    def __init__(self: Self, *args: object) -> None:
        super().__init__(*args)


class PetNotFoundException(PetException):
    def __init__(self: Self, message: str, pet_error: PetError) -> None:
        super().__init__(message)
        self.message = message
        self.pet_error = pet_error


jsonrpc = JSONRPCBlueprint('types__pydantic_models_annotated', __name__)


def handle_pet_not_found_exc(exc: PetNotFoundException) -> PetError:
    return exc.pet_error


jsonrpc.register_error_handler(PetNotFoundException, handle_pet_not_found_exc)


@jsonrpc.method(
    'types.pydantic_models_annotated.createPet',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create a pet'),
        tm.Description('This method creates a pet Pydantic model object from a NewPet object.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of creating a pet',
            summary='Create a pet from NewPet model',
            description='This demonstrates creating a Pet Pydantic model from a NewPet object.',
            params=[
                tm.ExampleField(
                    name='pet', value={'name': 'Fluffy', 'tag': 'cat'}, description='A NewPet Pydantic model object.'
                )
            ],
            returns=tm.ExampleField(
                name='result',
                value={'id': 1, 'name': 'Fluffy', 'tag': 'cat'},
                description='The created Pet Pydantic model object with auto-generated ID.',
            ),
        ),
    ],
)
def create_pet(
    pet: t.Annotated[
        NewPet,
        tp.Summary('New pet Pydantic model'),
        tp.Description('A NewPet Pydantic model object to create.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    Pet, tp.Summary('Created pet Pydantic model'), tp.Description('A Pet Pydantic model object with auto-generated ID.')
]:
    return Pet(id=1, name=pet.name, tag=pet.tag)


@jsonrpc.method(
    'types.pydantic_models_annotated.createManyPet',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create many pets'),
        tm.Description(
            'This method creates multiple pet Pydantic model objects from a list and an optional single pet.'
        ),
        tm.Tag('types'),
        tm.Example(
            name='Example of creating many pets',
            summary='Create multiple pets with optional extra pet',
            description='This demonstrates creating multiple Pet Pydantic models from a list of NewPet objects.',
            params=[
                tm.ExampleField(
                    name='pets',
                    value=[{'name': 'Rex', 'tag': 'dog'}, {'name': 'Whiskers', 'tag': 'cat'}],
                    description='A list of NewPet Pydantic model objects.',
                ),
                tm.ExampleField(
                    name='pet',
                    value={'name': 'Buddy', 'tag': 'dog'},
                    description='An optional additional NewPet Pydantic model object.',
                ),
            ],
            returns=tm.ExampleField(
                name='result',
                value=[
                    {'id': 0, 'name': 'Rex', 'tag': 'dog'},
                    {'id': 1, 'name': 'Whiskers', 'tag': 'cat'},
                    {'id': 2, 'name': 'Buddy', 'tag': 'dog'},
                ],
                description='List of created Pet Pydantic model objects with auto-generated IDs.',
            ),
        ),
    ],
)
def create_many_pets(
    pets: t.Annotated[
        list[NewPet],
        tp.Summary('List of new pet Pydantic models'),
        tp.Description('A list of pet Pydantic model objects to create.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
    pet: t.Annotated[
        NewPet | None,
        tp.Summary('Optional additional pet'),
        tp.Description('An optional additional pet to add to the list.'),
        tp.Required(False),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    list[Pet],
    tp.Summary('List of created pet Pydantic models'),
    tp.Description('A list of Pet Pydantic model objects with auto-generated IDs.'),
]:
    new_pets = [Pet(id=i, name=pet.name, tag=pet.tag) for i, pet in enumerate(pets)]
    if pet is not None:
        return new_pets + [Pet(id=len(pets), name=pet.name, tag=pet.tag)]
    return new_pets


@jsonrpc.method(
    'types.pydantic_models_annotated.createManyFixPet',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create many pets from dictionary'),
        tm.Description(
            'This method creates pet Pydantic model objects from a dictionary of pet IDs to NewPet objects.'
        ),
        tm.Tag('types'),
        tm.Example(
            name='Example of creating many pets from dictionary',
            summary='Create pets from dict mapping',
            description=(
                'This demonstrates creating Pet Pydantic models from a dictionary mapping IDs to NewPet objects.'
            ),
            params=[
                tm.ExampleField(
                    name='pets',
                    value={'1': {'name': 'Max', 'tag': 'dog'}, '2': {'name': 'Luna', 'tag': 'cat'}},
                    description='A dictionary mapping pet IDs to NewPet Pydantic model objects.',
                )
            ],
            returns=tm.ExampleField(
                name='result',
                value=[{'id': 1, 'name': 'Max', 'tag': 'dog'}, {'id': 2, 'name': 'Luna', 'tag': 'cat'}],
                description='List of created Pet Pydantic model objects with IDs from dictionary keys.',
            ),
        ),
    ],
)
def create_many_fix_pets(
    pets: t.Annotated[
        dict[str, NewPet],
        tp.Summary('Dictionary of pet ID to NewPet models'),
        tp.Description('A dictionary mapping pet IDs to NewPet Pydantic model objects.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    list[Pet],
    tp.Summary('List of created pet Pydantic models'),
    tp.Description('A list of Pet Pydantic model objects with IDs from dictionary keys.'),
]:
    return [Pet(id=int(pet_id), name=pet.name, tag=pet.tag) for pet_id, pet in pets.items()]


@jsonrpc.method(
    'types.pydantic_models_annotated.removePet',
    annotation=tm.MethodAnnotated[
        tm.Summary('Remove a pet'),
        tm.Description('This method removes a pet Pydantic model and can raise exceptions for certain conditions.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of removing a pet',
            summary='Remove a pet with error handling',
            description='This demonstrates removing a Pet Pydantic model with exception handling.',
            params=[
                tm.ExampleField(
                    name='pet',
                    value={'id': 5, 'name': 'Charlie', 'tag': 'bird'},
                    description='An optional Pet Pydantic model object to remove.',
                )
            ],
            returns=tm.ExampleField(
                name='result',
                value={'id': 5, 'name': 'Charlie', 'tag': 'bird'},
                description='The removed Pet Pydantic model object, or None if not provided.',
            ),
        ),
    ],
)
def remove_pet(
    pet: t.Annotated[
        Pet | None,
        tp.Summary('Optional pet to remove'),
        tp.Description('The Pet Pydantic model object to remove.'),
        tp.Required(False),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    Pet | None,
    tp.Summary('Removed pet Pydantic model'),
    tp.Description('The Pet Pydantic model object that was removed, or None if not provided.'),
]:
    if pet is not None and pet.id > 10:
        raise PetNotFoundException(
            'Pet not found', PetError(pet_id=pet.id, reason='The pet with an ID greater than 10 does not exist.')
        )
    return pet
