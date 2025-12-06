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
import random
from dataclasses import dataclass

# Added in version 3.11.
from typing_extensions import Self

from flask import Flask

from flask_jsonrpc import JSONRPC
from flask_jsonrpc.contrib.openrpc import OpenRPC, typing as st

app = Flask('openrpc')
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)
openrpc = OpenRPC(
    app,
    jsonrpc,
    openrpc_schema=st.OpenRPCSchema(
        openrpc='1.0.0-rc1',
        info=st.Info(
            version='1.0.0',
            title='Petstore Expanded',
            description=(
                'A sample API that uses a petstore as an example to demonstrate features in the OpenRPC specification'
            ),
            terms_of_service='https://open-rpc.org',
            contact=st.Contact(name='OpenRPC Team', email='doesntexist@open-rpc.org', url='https://open-rpc.org'),
            license=st.License(name='Apache 2.0', url='https://www.apache.org/licenses/LICENSE-2.0.html'),
        ),
        servers=[st.Server(url='http://petstore.open-rpc.org')],
        components=st.Components(
            schemas={
                'Pet': st.Schema(
                    all_of=[
                        st.Schema(ref='#/components/schemas/NewPet'),
                        st.Schema(required=['id'], properties={'id': st.Schema(type=st.SchemaDataType.INTEGER)}),
                    ]
                ),
                'NewPet': st.Schema(
                    type=st.SchemaDataType.OBJECT,
                    required=['name'],
                    properties={
                        'name': st.Schema(type=st.SchemaDataType.STRING),
                        'tag': st.Schema(type=st.SchemaDataType.STRING),
                    },
                ),
            }
        ),
        external_docs=st.ExternalDocumentation(
            url='https://github.com/open-rpc/examples/blob/master/service-descriptions/petstore-expanded-openrpc.json'
        ),
    ),
)


class PetBaseException(Exception):
    def __init__(self: Self, message: str) -> None:
        super().__init__(message)


class PetNotFoundException(PetBaseException):
    def __init__(self: Self, pet_id: int) -> None:
        super().__init__(message=f'Pet not found: {pet_id}')


@dataclass
class NewPet:
    name: str
    tag: str


@dataclass
class Pet(NewPet):
    id: int


PETS = [Pet(id=1, name='Bob', tag='dog'), Pet(id=2, name='Eve', tag='cat'), Pet(id=3, name='Alice', tag='bird')]


@jsonrpc.errorhandler(PetNotFoundException)
def handle_pet_not_found_exc(ex: PetNotFoundException) -> dict[str, str]:
    return {'message': str(ex), 'code': '1001'}


@openrpc.extend_schema(
    name='Petstore.get_pets',
    description=(
        'Returns all pets from the system that the user has access to\n'
        'Nam sed condimentum est. Maecenas tempor sagittis sapien, nec rhoncus sem '
        'sagittis sit amet. Aenean at gravida augue, ac iaculis sem. Curabitur odio '
        'lorem, ornare eget elementum nec, cursus id lectus. Duis mi turpis, pulvinar '
        'ac eros ac, tincidunt varius justo. In hac habitasse platea dictumst. Integer '
        'at adipiscing ante, a sagittis ligula. Aenean pharetra tempor ante molestie '
        'imperdiet. Vivamus id aliquam diam.'
    ),
    params=[
        st.ContentDescriptor(
            name='tags',
            description='tags to filter by',
            schema_=st.Schema(type=st.SchemaDataType.ARRAY, items=st.Schema(type=st.SchemaDataType.STRING)),
        ),
        st.ContentDescriptor(
            name='limit',
            description='maximum number of results to return',
            schema_=st.Schema(type=st.SchemaDataType.INTEGER),
        ),
    ],
    result=st.ContentDescriptor(
        name='pet',
        description='pet response',
        schema_=st.Schema(type=st.SchemaDataType.ARRAY, items=st.Schema(ref='#/components/schemas/Pet')),
    ),
)
@jsonrpc.method('Petstore.get_pets')
def get_pets(tags: list[str] | None = None, limit: int | None = None) -> list[Pet]:
    pets = PETS
    if tags is not None:
        pets = [pet for pet in pets if pet.tag in tags]
    if limit is not None:
        pets = pets[:limit]
    return pets


@openrpc.extend_schema(
    name='Petstore.create_pet',
    description='Creates a new pet in the store.  Duplicates are allowed',
    params=[
        st.ContentDescriptor(
            name='newPet', description='Pet to add to the store.', schema_=st.Schema(ref='#/components/schemas/NewPet')
        )
    ],
    result=st.ContentDescriptor(
        name='pet', description='the newly created pet', schema_=st.Schema(ref='#/components/schemas/Pet')
    ),
)
@jsonrpc.method('Petstore.create_pet')
def create_pet(new_pet: NewPet) -> Pet:
    pet = Pet(id=random.randint(4, 100), name=new_pet.name, tag=new_pet.tag)
    PETS.append(pet)
    return pet


@openrpc.extend_schema(
    name='Petstore.get_pet_by_id',
    description='Returns a user based on a single ID, if the user does not have access to the pet',
    params=[
        st.ContentDescriptor(
            name='id',
            description='ID of pet to fetch',
            required=True,
            schema_=st.Schema(type=st.SchemaDataType.INTEGER),
        )
    ],
    result=st.ContentDescriptor(
        name='pet', description='pet response', schema_=st.Schema(ref='#/components/schemas/Pet')
    ),
)
@jsonrpc.method('Petstore.get_pet_by_id')
def get_pet_by_id(id: int) -> Pet | None:
    pet = [pet for pet in PETS if pet.id == id]
    return None if len(pet) == 0 else pet[0]


@openrpc.extend_schema(
    name='Petstore.delete_pet_by_id',
    description='deletes a single pet based on the ID supplied',
    params=[
        st.ContentDescriptor(
            name='id',
            description='ID of pet to delete',
            required=True,
            schema_=st.Schema(type=st.SchemaDataType.INTEGER),
        )
    ],
    result=st.ContentDescriptor(name='pet', description='pet deleted', schema_=st.Schema()),
)
@jsonrpc.method('Petstore.delete_pet_by_id')
def delete_pet_by_id(id: int) -> Pet:
    global PETS
    removed = [pet for pet in PETS if pet.id == id]
    if len(removed) == 0:
        raise PetNotFoundException(id)
    PETS = [pet for pet in PETS if pet.id != id]  # noqa: F823, F841
    return removed[0]
