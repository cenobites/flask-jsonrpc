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
from dataclasses import dataclass

from flask_jsonrpc import JSONRPCBlueprint

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


jsonrpc = JSONRPCBlueprint('objects__python_dataclasses', __name__)


@jsonrpc.errorhandler(CarNotFoundException)
def handle_car_not_found_exc(exc: CarNotFoundException) -> CarError:
    return exc.car_error


@jsonrpc.method('objects.python_dataclasses.createCar')
def create_car(car: NewCar) -> Car:
    return Car(id=1, name=car.name, tag=car.tag)


@jsonrpc.method('objects.python_dataclasses.createManyCar')
def create_many_cars(cars: list[NewCar], car: NewCar | None = None) -> list[Car]:
    new_cars = [Car(id=i, name=car.name, tag=car.tag) for i, car in enumerate(cars)]
    if car is not None:
        return new_cars + [Car(id=len(cars), name=car.name, tag=car.tag)]
    return new_cars


@jsonrpc.method('objects.python_dataclasses.createManyFixCar')
def create_many_fix_cars(cars: dict[str, NewCar]) -> list[Car]:
    return [Car(id=int(car_id), name=car.name, tag=car.tag) for car_id, car in cars.items()]


@jsonrpc.method('objects.python_dataclasses.removeCar')
def remove_car(car: Car | None = None) -> Car | None:
    if car is not None and car.id > 10:
        raise CarNotFoundException(
            'Car not found', CarError(car_id=car.id, reason='The car with an ID greater than 10 does not exist.')
        )
    return car
