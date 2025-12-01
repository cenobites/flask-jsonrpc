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
from flask_jsonrpc.contrib.browse import JSONRPCBrowse

# Added in version 3.11.


class CustomJSONRPCBrowse(JSONRPCBrowse):
    def get_browse_title(self: Self) -> str:
        return 'Petstore API'

    def get_browse_subtitle(self: Self) -> str:
        return 'Managing pets'

    def get_browse_description(self: Self) -> str:
        return 'This is the Petstore API which allows you to manage '

    'pets including creating, retrieving, and deleting pets.'

    def get_browse_fork_me_button_enabled(self: Self) -> bool:
        return False

    def get_browse_media_css(self: Self) -> dict[str, list[str]]:
        return {'all': ['css/petstore.css']}

    def get_browse_media_js(self: Self) -> list[str]:
        return ['js/petstore.js']

    def get_browse_dashboard_menu_name(self: Self) -> str:
        return 'Petstore Dashboard'

    def get_browse_dashboard_template(self: Self) -> str:
        return 'browse/dashboard.html'


app = Flask('openrpc', template_folder='src/petstore/templates', static_folder='src/petstore/static')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=False)
browse = CustomJSONRPCBrowse(app, url_prefix='/api/browse')
browse.register_jsonrpc_site(jsonrpc.get_jsonrpc_site())


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
        tm.Example(
            name='default',
            params=[
                tm.ExampleField(
                    name='tags', value=['dog', 'cat'], summary='Tags to filter by', description='Tags to filter by'
                ),
                tm.ExampleField(
                    name='limit',
                    value=2,
                    summary='Maximum number of results to return',
                    description='Maximum number of results to return',
                ),
            ],
        ),
    ],
)
def get_pets(
    tags: t.Annotated[list[str] | None, tp.Summary('tags to filter by')] = None,
    limit: t.Annotated[int | None, tp.Summary('maximum number of results to return'), tp.Minimum(1)] = 25,
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
                tm.ExampleField(name='tags', value='dog', summary='Tags to filter by', description='Tags to filter by'),
                tm.ExampleField(
                    name='limit',
                    value=25,
                    summary='Maximum number of results to return',
                    description='Maximum number of results to return',
                ),
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
) -> t.Annotated[Pet | None, tp.Summary('pet response')]:
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
        tm.Example(
            name='default',
            params=[
                tm.ExampleField(name='id', value=1, summary='ID of pet to delete', description='ID of pet to delete')
            ],
        ),
    ],
)
def delete_pet_by_id(
    id: t.Annotated[int, tp.Summary('ID of pet to delete'), tp.Minimum(1)],
) -> t.Annotated[Pet, tp.Summary('pet deleted')]:
    """Deletes a single pet based on the ID supplied"""
    global PETS
    removed = [pet for pet in PETS if pet.id == id]
    if len(removed) == 0:
        raise PetNotFoundException(id)
    PETS = [pet for pet in PETS if pet.id != id]  # noqa: F823, F841
    return removed[0]
