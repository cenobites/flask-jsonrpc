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

from pydantic.main import BaseModel

from flask_jsonrpc import JSONRPCBlueprint

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


jsonrpc = JSONRPCBlueprint('objects__pydantic_models', __name__)


def handle_pet_not_found_exc(exc: PetNotFoundException) -> PetError:
    return exc.pet_error


jsonrpc.register_error_handler(PetNotFoundException, handle_pet_not_found_exc)


@jsonrpc.method('objects.pydantic_models.createPet')
def create_pet(pet: NewPet) -> Pet:
    return Pet(id=1, name=pet.name, tag=pet.tag)


@jsonrpc.method('objects.pydantic_models.createManyPet')
def create_many_pets(pets: list[NewPet], pet: NewPet | None = None) -> list[Pet]:
    new_pets = [Pet(id=i, name=pet.name, tag=pet.tag) for i, pet in enumerate(pets)]
    if pet is not None:
        return new_pets + [Pet(id=len(pets), name=pet.name, tag=pet.tag)]
    return new_pets


@jsonrpc.method('objects.pydantic_models.createManyFixPet')
def create_many_fix_pets(pets: dict[str, NewPet]) -> list[Pet]:
    return [Pet(id=int(pet_id), name=pet.name, tag=pet.tag) for pet_id, pet in pets.items()]


@jsonrpc.method('objects.pydantic_models.removePet')
def remove_pet(pet: Pet | None = None) -> Pet | None:
    if pet is not None and pet.id > 10:
        raise PetNotFoundException(
            'Pet not found', PetError(pet_id=pet.id, reason='The pet with an ID greater than 10 does not exist.')
        )
    return pet
