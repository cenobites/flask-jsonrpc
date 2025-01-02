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
import random
import typing as t

# Added in version 3.11.
from typing_extensions import Self

from flask import Flask

from pydantic import BaseModel

from flask_jsonrpc import JSONRPC
import flask_jsonrpc.types.params as tp
import flask_jsonrpc.types.methods as tm

app = Flask('openrpc')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


class PetBaseException(Exception):
    def __init__(self: Self, message: t.Annotated[str, tp.Summary('Exception reason')]) -> None:
        super().__init__(message)


class PetNotFoundException(PetBaseException):
    def __init__(self: Self, pet_id: t.Annotated[int, tp.Summary('')]) -> None:
        super().__init__(message=f'Pet not found: {pet_id}')


class NewPet(BaseModel):
    name: str
    tag: str


class Pet(NewPet):
    id: int


PETS = [Pet(id=1, name='Bob', tag='dog'), Pet(id=2, name='Eve', tag='cat'), Pet(id=3, name='Alice', tag='bird')]


@jsonrpc.errorhandler(PetNotFoundException)
def handle_pet_not_found_exc(ex: PetNotFoundException) -> dict[str, str]:
    return {'message': str(ex), 'code': '1001'}


@jsonrpc.method(
    'Petstore.get_pets',
    tm.MethodAnnotated[
        tm.Summary('Returns all pets from the system'),
        tm.Description(
            'Returns all pets from the system that the user has access to\n'
            'Nam sed condimentum est. Maecenas tempor sagittis sapien, nec rhoncus sem '
            'sagittis sit amet. Aenean at gravida augue, ac iaculis sem. Curabitur odio '
            'lorem, ornare eget elementum nec, cursus id lectus. Duis mi turpis, pulvinar '
            'ac eros ac, tincidunt varius justo. In hac habitasse platea dictumst. Integer '
            'at adipiscing ante, a sagittis ligula. Aenean pharetra tempor ante molestie '
            'imperdiet. Vivamus id aliquam diam.'
        ),
        tm.Tag('pet'),
        tm.Error(code=-32000, message='ServerError', data={'message': 'Server error'}, status_code=500),
        tm.Example(name='default'),
    ],
)
def get_pets(
    tags: t.Annotated[t.Optional[list[str]], tp.Summary('tags to filter by')] = None,
    limit: t.Annotated[t.Optional[int], tp.Summary('maximum number of results to return'), tp.Minimum(1)] = 25,
) -> t.Annotated[list[Pet], tp.Summary('pet response')]:
    pets = PETS
    if tags is not None:
        pets = [pet for pet in pets if pet.tag in tags]
    if limit is not None:
        pets = pets[:limit]
    return pets


@jsonrpc.method(
    'Petstore.create_pet',
    tm.MethodAnnotated[
        tm.Tag('pet'),
        tm.Error(code=-32000, message='Server error', data={'message': 'Pet not found: <pet_id>'}, status_code=500),
        tm.Example(
            name='default',
            params=[
                tm.ExampleField(name='tags', value='dog', summary='', description=''),
                tm.ExampleField(name='limit', value=25, summary='', description=''),
            ],
        ),
    ],
)
def create_pet(
    new_pet: t.Annotated[
        NewPet,
        tp.Summary('Pet to add to the store'),
        tp.Properties(
            {'name': t.Annotated[str, tp.Summary('name of pet')], 'tag': t.Annotated[str, tp.Summary('tag of pet')]}
        ),
    ],
) -> t.Annotated[Pet, tp.Summary('the newly created pet')]:
    """Creates a new pet in the store.

    Duplicates are allowed"""
    pet = Pet(id=random.randint(4, 100), name=new_pet.name, tag=new_pet.tag)
    PETS.append(pet)
    return pet


@jsonrpc.method(
    'Petstore.get_pet_by_id',
    tm.MethodAnnotated[
        tm.Tag('pet'),
        tm.Example(name='default', params=[tm.ExampleField(name='id', value=1, summary='', description='')]),
    ],
)
def get_pet_by_id(
    id: t.Annotated[int, tp.Summary('ID of pet to fetch'), tp.Minimum(1)],
) -> t.Annotated[t.Optional[Pet], tp.Summary('pet response')]:
    """Returns a user based on a single ID, if the user does not have
    access to the pet
    """
    pet = [pet for pet in PETS if pet.id == id]
    return None if len(pet) == 0 else pet[0]


@jsonrpc.method(
    'Petstore.delete_pet_by_id',
    tm.MethodAnnotated[
        tm.Tag('pet'),
        tm.Error(code=-32000, message='Server error', data={'message': 'Pet not found: <pet_id>'}, status_code=500),
        tm.Example(name='default', params=[tm.ExampleField(name='id', value=1, summary='', description='')]),
    ],
)
def delete_pet_by_id(
    id: t.Annotated[int, tp.Summary('ID of pet to delete'), tp.Minimum(1)],
) -> t.Annotated[Pet, tp.Summary('pet deleted')]:
    """deletes a single pet based on the ID supplied"""
    global PETS
    removed = [pet for pet in PETS if pet.id == id]
    if len(removed) == 0:
        raise PetNotFoundException(id)
    PETS = [pet for pet in PETS if pet.id != id]  # noqa: F823, F841
    return removed[0]
