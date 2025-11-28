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
from dataclasses import dataclass

from flask_jsonrpc import JSONRPCBlueprint
import flask_jsonrpc.types.params as tp
import flask_jsonrpc.types.methods as tm

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self


@dataclass
class NewCar:
    name: str
    tag: str


@dataclass
class Car(NewCar):
    id: int


@dataclass
class CarError:
    car_id: int
    reason: str


class CarException(Exception):
    def __init__(self: Self, *args: object) -> None:
        super().__init__(*args)


class CarNotFoundException(CarException):
    def __init__(self: Self, message: str, car_error: CarError) -> None:
        super().__init__(message)
        self.message = message
        self.car_error = car_error


jsonrpc = JSONRPCBlueprint('types__python_dataclasses_annoated', __name__)


@jsonrpc.errorhandler(CarNotFoundException)
def handle_car_not_found_exc(exc: CarNotFoundException) -> CarError:
    return exc.car_error


@jsonrpc.method(
    'types.python_dataclasses_annotated.createCar',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create a new car'),
        tm.Description('This method creates a new car dataclass object with an auto-generated ID.'),
        tm.Tag(
            name='types',
            summary='Python dataclasses related methods',
            description='Methods that demonstrate Python dataclass objects in JSON-RPC.',
        ),
        tm.Example(
            name='Example of creating a car',
            summary='Create a car with name and tag',
            description='This demonstrates creating a Car dataclass from a NewCar input.',
            params=[
                tm.ExampleField(
                    name='car',
                    value={'name': 'Tesla Model 3', 'tag': 'electric'},
                    description='A NewCar dataclass with name and tag.',
                )
            ],
            returns=tm.ExampleField(
                name='result',
                value={'id': 1, 'name': 'Tesla Model 3', 'tag': 'electric'},
                description='The created Car dataclass with ID.',
            ),
        ),
    ],
)
def create_car(
    car: t.Annotated[
        NewCar,
        tp.Summary('A new car dataclass object'),
        tp.Description('The car dataclass object to create, containing name and tag.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    Car,
    tp.Summary('The created car dataclass object'),
    tp.Description('A Car dataclass with an auto-generated ID, name, and tag.'),
]:
    return Car(id=1, name=car.name, tag=car.tag)


@jsonrpc.method(
    'types.python_dataclasses_annotated.createManyCar',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create many cars'),
        tm.Description('This method creates multiple car dataclass objects from a list and an optional single car.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of creating many cars',
            summary='Create multiple cars with optional extra car',
            description='This demonstrates creating multiple Car dataclasses from a list of NewCar objects.',
            params=[
                tm.ExampleField(
                    name='cars',
                    value=[{'name': 'BMW i3', 'tag': 'electric'}, {'name': 'Toyota Prius', 'tag': 'hybrid'}],
                    description='A list of NewCar dataclass objects.',
                ),
                tm.ExampleField(
                    name='car',
                    value={'name': 'Honda Civic', 'tag': 'gas'},
                    description='An optional additional NewCar dataclass object.',
                ),
            ],
            returns=tm.ExampleField(
                name='result',
                value=[
                    {'id': 0, 'name': 'BMW i3', 'tag': 'electric'},
                    {'id': 1, 'name': 'Toyota Prius', 'tag': 'hybrid'},
                    {'id': 2, 'name': 'Honda Civic', 'tag': 'gas'},
                ],
                description='List of created Car dataclass objects with auto-generated IDs.',
            ),
        ),
    ],
)
def create_many_cars(
    cars: t.Annotated[
        list[NewCar],
        tp.Summary('List of new car dataclass objects'),
        tp.Description('A list of car dataclass objects to create.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
    car: t.Annotated[
        NewCar | None,
        tp.Summary('Optional additional car'),
        tp.Description('An optional additional car to add to the list.'),
        tp.Required(False),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    list[Car],
    tp.Summary('List of created car dataclass objects'),
    tp.Description('A list of Car dataclass objects with auto-generated IDs.'),
]:
    new_cars = [Car(id=i, name=car.name, tag=car.tag) for i, car in enumerate(cars)]
    if car is not None:
        return new_cars + [Car(id=len(cars), name=car.name, tag=car.tag)]
    return new_cars


@jsonrpc.method(
    'types.python_dataclasses_annotated.createManyFixCar',
    annotation=tm.MethodAnnotated[
        tm.Summary('Create many fixed cars'),
        tm.Description('This method creates exactly 4 car dataclass objects with specific names and tags.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of creating many fixed cars',
            summary='Create 4 predefined cars',
            description='This demonstrates creating 4 Car dataclasses with predetermined values.',
            params=[],
            returns=tm.ExampleField(
                name='result',
                value=[
                    {'id': 1, 'name': 'Volkswagen Jetta', 'tag': 'gas'},
                    {'id': 2, 'name': 'Chevrolet Bolt', 'tag': 'electric'},
                    {'id': 3, 'name': 'Lexus NX 300h', 'tag': 'hybrid'},
                    {'id': 4, 'name': 'Buick Regal', 'tag': 'gas'},
                ],
                description='A list of 4 fixed Car dataclass objects with predetermined values.',
            ),
        ),
    ],
)
def create_many_fix_cars(
    cars: t.Annotated[
        dict[str, NewCar],
        tp.Summary('List of new car dataclass objects'),
        tp.Description('A list of car dataclass objects to create.'),
        tp.Required(True),
        tp.Nullable(False),
    ],
) -> t.Annotated[
    list[Car],
    tp.Summary('List of fixed car dataclass objects'),
    tp.Description('A list of 4 predefined Car dataclass objects.'),
]:
    return [Car(id=int(car_id), name=car.name, tag=car.tag) for car_id, car in cars.items()]


@jsonrpc.method(
    'types.python_dataclasses_annotated.removeCar',
    annotation=tm.MethodAnnotated[
        tm.Summary('Remove a car by ID'),
        tm.Description('This method removes a car dataclass by its ID and can optionally be forced.'),
        tm.Tag('types'),
        tm.Example(
            name='Example of removing a car',
            summary='Remove a car by ID',
            description='This demonstrates removing a Car dataclass by providing its ID.',
            params=[
                tm.ExampleField(name='car_id', value=1, description='The ID of the car to remove.'),
                tm.ExampleField(name='force', value=False, description='Whether to force the removal.'),
            ],
            returns=tm.ExampleField(
                name='result',
                value={'id': 1, 'name': 'Removed Car', 'tag': 'removed'},
                description='The removed Car dataclass object.',
            ),
        ),
    ],
)
def remove_car(
    car: t.Annotated[
        Car | None,
        tp.Summary('Optional removed car'),
        tp.Description('An optional removed car to add to the list.'),
        tp.Required(False),
        tp.Nullable(True),
    ] = None,
) -> t.Annotated[
    Car | None, tp.Summary('Removed car dataclass object'), tp.Description('The Car dataclass object that was removed.')
]:
    if car is not None and car.id > 10:
        raise CarNotFoundException(
            'Car not found', CarError(car_id=car.id, reason='The car with an ID greater than 10 does not exist.')
        )
    return car
