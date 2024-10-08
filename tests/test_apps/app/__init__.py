#!/usr/bin/env python
# Copyright (c) 2012-2024, Cenobit Technologies, Inc. http://cenobit.es/
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
import os
import typing as t
import functools
from dataclasses import dataclass

from flask import Flask

# Python 3.11+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

from pydantic import BaseModel

from flask_jsonrpc import JSONRPC


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


class App:
    @staticmethod
    def index(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @staticmethod
    def greeting(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @staticmethod
    def hello(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    @staticmethod
    def echo(string: str, _some: t.Any = None) -> str:  # noqa: ANN401
        return string

    @staticmethod
    def notify(_string: t.Optional[str] = None) -> None:
        pass

    @staticmethod
    def not_allow_notify(_string: t.Optional[str] = None) -> str:
        return 'Now allow notify'

    @staticmethod
    def fails(n: int) -> int:
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')


def jsonrpc_decorator(fn: t.Callable[..., str]) -> t.Callable[..., str]:
    def decorator(string: str) -> str:
        rv = fn(string)
        return f'{rv} from decorator, ;)'

    return decorator


def jsonrpc_decorator_wrapped(fn: t.Callable[..., str]) -> t.Callable[..., str]:
    @functools.wraps(fn)
    def decorator(string: str) -> str:
        rv = fn(string)
        return f'{rv} from decorator, ;)'

    return decorator


def create_app(test_config: t.Optional[t.Dict[str, t.Any]] = None) -> Flask:  # noqa: C901  pylint: disable=W0612
    """Create and configure an instance of the Flask application."""
    flask_app = Flask('apptest', instance_relative_config=True)
    if test_config:
        flask_app.config.update(test_config)

    jsonrpc = JSONRPC(flask_app, '/api', enable_web_browsable_api=True)

    @jsonrpc.errorhandler(ColorNotFoundException)
    def handle_color_not_found_exc(exc: ColorNotFoundException) -> ColorError:
        return exc.color_error

    def handle_pet_not_found_exc(exc: PetNotFoundException) -> PetError:
        return exc.pet_error

    jsonrpc.register_error_handler(PetNotFoundException, handle_pet_not_found_exc)

    @jsonrpc.errorhandler(CarNotFoundException)
    def handle_car_not_found_exc(exc: CarNotFoundException) -> CarError:
        return exc.car_error

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.greeting')
    def greeting(name: str = 'Flask JSON-RPC') -> str:
        return f'Hello {name}'

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.echo')
    def echo(string: str, _some: t.Any = None) -> str:  # noqa: ANN401
        return string

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.notify')
    def notify(_string: t.Optional[str] = None) -> None:
        pass

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.not_allow_notify', notification=False)
    def not_allow_notify(_string: str = 'None') -> str:
        return 'Not allow notify'

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.fails')
    def fails(n: int) -> int:
        if n % 2 == 0:
            return n
        raise ValueError('number is odd')

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.strangeEcho')
    def strange_echo(
        string: str, omg: t.Dict[str, t.Any], wtf: t.List[str], nowai: int, yeswai: str = 'Default'
    ) -> t.List[t.Any]:
        return [string, omg, wtf, nowai, yeswai]

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.sum')
    def sum_(a: t.Union[int, float], b: t.Union[int, float]) -> t.Union[int, float]:
        return a + b

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.decorators')
    @jsonrpc_decorator
    def decorators(string: str) -> str:
        return f'Hello {string}'

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.decoratorsWrapped')
    @jsonrpc_decorator_wrapped
    def decoratorsWrapped(string: str) -> str:
        return f'Hello {string}'

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnStatusCode')
    def return_status_code(s: str) -> t.Tuple[str, int]:
        return f'Status Code {s}', 201

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnHeaders')
    def return_headers(s: str) -> t.Tuple[str, t.Dict[str, t.Any]]:
        return f'Headers {s}', {'X-JSONRPC': '1'}

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.returnStatusCodeAndHeaders')
    def return_status_code_and_headers(s: str) -> t.Tuple[str, int, t.Dict[str, t.Any]]:
        return f'Status Code and Headers {s}', 400, {'X-JSONRPC': '1'}

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.not_validate', validate=False)
    def not_validate(s='Oops!'):  # noqa: ANN001,ANN202
        return f'Not validate: {s}'

    # pylint: disable=W0612
    @jsonrpc.method('jsonrpc.mixin_not_validate', validate=False)
    def mixin_not_validate(s, t: int, u, v: str, x, z):  # noqa: ANN001,ANN202
        return f'Not validate: {s} {t} {u} {v} {x} {z}'

    @jsonrpc.method('jsonrpc.noReturn')
    def no_return(_string: t.Optional[str] = None) -> t.NoReturn:
        raise ValueError('no return')

    @jsonrpc.method('jsonrpc.invalidUnion1')
    def invalid_union_1(color: t.Union[Color, NewColor]) -> t.Union[Color, NewColor]:
        return color

    @jsonrpc.method('jsonrpc.invalidUnion2')
    def invalid_union_2(color: t.Union[Color, NewColor, None] = None) -> t.Union[Color, NewColor, None]:
        return color

    @jsonrpc.method('jsonrpc.literalType')
    def literal_type(x: t.Literal['X']) -> t.Literal['X']:
        return x

    @jsonrpc.method('jsonrpc.createColor')
    def create_color(color: NewColor) -> Color:
        return Color(id=1, name=color.name, tag=color.tag)

    @jsonrpc.method('jsonrpc.createManyColor')
    def create_many_colors(colors: t.List[NewColor], color: t.Optional[NewColor] = None) -> t.List[Color]:
        new_color = [Color(id=i, name=pet.name, tag=pet.tag) for i, pet in enumerate(colors)]
        if color is not None:
            return new_color + [Color(id=len(colors), name=color.name, tag=color.tag)]
        return new_color

    @jsonrpc.method('jsonrpc.createManyFixColor')
    def create_many_fix_colors(colors: t.Dict[str, NewPet]) -> t.List[Color]:
        return [Color(id=int(color_id), name=color.name, tag=color.tag) for color_id, color in colors.items()]

    @jsonrpc.method('jsonrpc.removeColor')
    def remove_color(color: t.Optional[Color] = None) -> t.Optional[Color]:
        if color is not None and color.id > 10:
            raise ColorNotFoundException(
                'Color not found',
                ColorError(color_id=color.id, reason='The color with an ID greater than 10 does not exist.'),
            )
        return color

    @jsonrpc.method('jsonrpc.createPet')
    def create_pet(pet: NewPet) -> Pet:
        return Pet(id=1, name=pet.name, tag=pet.tag)

    @jsonrpc.method('jsonrpc.createManyPet')
    def create_many_pets(pets: t.List[NewPet], pet: t.Optional[NewPet] = None) -> t.List[Pet]:
        new_pets = [Pet(id=i, name=pet.name, tag=pet.tag) for i, pet in enumerate(pets)]
        if pet is not None:
            return new_pets + [Pet(id=len(pets), name=pet.name, tag=pet.tag)]
        return new_pets

    @jsonrpc.method('jsonrpc.createManyFixPet')
    def create_many_fix_pets(pets: t.Dict[str, NewPet]) -> t.List[Pet]:
        return [Pet(id=int(pet_id), name=pet.name, tag=pet.tag) for pet_id, pet in pets.items()]

    @jsonrpc.method('jsonrpc.removePet')
    def remove_pet(pet: t.Optional[Pet] = None) -> t.Optional[Pet]:
        if pet is not None and pet.id > 10:
            raise PetNotFoundException(
                'Pet not found', PetError(pet_id=pet.id, reason='The pet with an ID greater than 10 does not exist.')
            )
        return pet

    @jsonrpc.method('jsonrpc.createCar')
    def create_car(car: NewCar) -> Car:
        return Car(id=1, name=car.name, tag=car.tag)

    @jsonrpc.method('jsonrpc.createManyCar')
    def create_many_cars(cars: t.List[NewCar], car: t.Optional[NewCar] = None) -> t.List[Car]:
        new_cars = [Car(id=i, name=car.name, tag=car.tag) for i, car in enumerate(cars)]
        if car is not None:
            return new_cars + [Car(id=len(cars), name=car.name, tag=car.tag)]
        return new_cars

    @jsonrpc.method('jsonrpc.createManyFixCar')
    def create_many_fix_cars(cars: t.Dict[str, NewCar]) -> t.List[Car]:
        return [Car(id=int(car_id), name=car.name, tag=car.tag) for car_id, car in cars.items()]

    @jsonrpc.method('jsonrpc.removeCar')
    def remove_car(car: t.Optional[Car] = None) -> t.Optional[Car]:
        if car is not None and car.id > 10:
            raise CarNotFoundException(
                'Car not found', CarError(car_id=car.id, reason='The car with an ID greater than 10 does not exist.')
            )
        return car

    class_app = App()
    jsonrpc.register(class_app.index, name='classapp.index')
    jsonrpc.register(class_app.greeting)
    jsonrpc.register(class_app.hello)
    jsonrpc.register(class_app.echo)
    jsonrpc.register(class_app.notify)
    jsonrpc.register(class_app.not_allow_notify, notification=False)
    jsonrpc.register(class_app.fails)

    return flask_app


if __name__ == '__main__':
    app = create_app({'SERVER_NAME': os.getenv('FLASK_SERVER_NAME')})
    app.run(host='0.0.0.0')
