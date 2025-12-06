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
import typing as t
from datetime import datetime, timezone, timedelta

# Added in version 3.11.
from typing_extensions import Self

from flask import Flask, typing as ft, jsonify, request, redirect
from flask.wrappers import Request, Response

from pydantic import BaseModel

from jwt import PyJWTError
import flask_jwt_extended as flask_jwt
from flask_jwt_extended import JWTManager, jwt_required
from flask_jwt_extended.exceptions import JWTExtendedException

from flask_jsonrpc import JSONRPC
import flask_jsonrpc.types.params as tp
import flask_jsonrpc.types.methods as tm
from flask_jsonrpc.contrib.browse import JSONRPCBrowse, register_middleware


@register_middleware('authentication')
def authentication_middleware(
    request: Request,
) -> t.Generator[ft.ResponseReturnValue | bool | None, Response, ft.ResponseReturnValue | None]:
    if (
        request.path == '/api/browse/'
        or request.path.startswith('/api/browse/static')
        or request.path.startswith('/api/browse/login')
        or request.path.startswith('/api/browse/logout')
    ):
        yield False

    try:
        flask_jwt.verify_jwt_in_request()
    except (JWTExtendedException, PyJWTError):
        yield redirect('/api/browse/login')

    response = yield

    jwt = flask_jwt.get_jwt()
    if not jwt:
        yield redirect('/api/browse/login')

    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    exp_timestamp = jwt.get('exp', target_timestamp)
    if target_timestamp > exp_timestamp:
        access_token = flask_jwt.create_access_token(identity=flask_jwt.get_jwt_identity())
        flask_jwt.set_access_cookies(response, access_token)
        yield False
    yield redirect('/api/browse/login')


class CustomJSONRPCBrowse(JSONRPCBrowse):
    def get_browse_title(self: Self) -> str:
        return 'Petstore API'

    def get_browse_subtitle(self: Self) -> str:
        return 'Managing pets'

    def get_browse_description(self: Self) -> str:
        return 'This is the Petstore API which allows you to manage pets'

    def get_browse_fork_me_button_enabled(self: Self) -> bool:
        return False

    def get_browse_media_css(self: Self) -> dict[str, list[str]]:
        return {'all': ['css/petstore.css']}

    def get_browse_media_js(self: Self) -> list[str]:
        return ['js/services.js', 'js/petstore.js']

    def get_browse_dashboard_menu_name(self: Self) -> str:
        return 'Petstore Dashboard'

    def get_browse_dashboard_partial_template(self: Self) -> str:
        return 'browse/partials/dashboard.html'

    def get_browse_login_template(self) -> str:
        return 'browse/login.html'

    def get_browse_logout_template(self) -> str:
        return 'browse/logout.html'


app = Flask('openrpc', template_folder='src/petstore/templates', static_folder='src/petstore/static')
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # 'cookies' is supported but disabled for simplicity
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_ACCESS_CSRF_COOKIE_PATH'] = '/api'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)
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


@app.route('/oauth/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def oauth_token_refresh() -> ft.ResponseReturnValue:
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens.html#explicit-refreshing-with-refresh-tokens
    identity = flask_jwt.get_jwt_identity()
    access_token = flask_jwt.create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@app.route('/login', methods=['POST'])
def login() -> ft.ResponseReturnValue:
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({'msg': 'Bad username or password'}), 401

    access_token = flask_jwt.create_access_token(identity=username)
    refresh_token = flask_jwt.create_refresh_token(identity=username)
    response = jsonify(access_token=access_token, refresh_token=refresh_token)
    # Uncomment to use cookies: app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens.html#implicit-refreshing-with-cookies
    # flask_jwt.set_access_cookies(response, access_token)
    # flask_jwt.set_refresh_cookies(response, refresh_token)
    return response


@app.route('/logout', methods=['POST'])
def logout() -> ft.ResponseReturnValue:
    response = jsonify({'msg': 'logout successful'})
    # Uncomment to use cookies: app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens.html#implicit-refreshing-with-cookies
    # flask_jwt.unset_jwt_cookies(response)
    return response


@jsonrpc.errorhandler(PyJWTError)
def handle_pyjwt_error(e: PyJWTError) -> ft.ResponseReturnValue:
    return {'msg': str(e)}, 401


@jsonrpc.errorhandler(JWTExtendedException)
def handle_jwt_extended_exception(e: JWTExtendedException) -> ft.ResponseReturnValue:
    return {'msg': str(e)}, 401


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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
