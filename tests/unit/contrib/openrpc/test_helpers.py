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
from flask_jsonrpc.contrib.openrpc import typing as st
from flask_jsonrpc.contrib.openrpc.helpers import openrpc_schema_to_dict


def test_openrpc_schema_to_dict() -> None:
    openrpc_schema = st.OpenRPCSchema(
        info=st.Info(
            version='1.0.0',
            title='Petstore Expanded',
            description=(
                'A sample API that uses a petstore as an example to '
                'demonstrate features in the OpenRPC specification'
            ),
            terms_of_service='https://open-rpc.org',
            contact=st.Contact(name='OpenRPC Team', email='doesntexist@open-rpc.org', url='https://open-rpc.org'),
            license=st.License(name='Apache 2.0', url='https://www.apache.org/licenses/LICENSE-2.0.html'),
        ),
        openrpc='1.0.0-rc1',
        methods=[
            st.Method(
                name='get_pets',
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
                        schema=st.Schema(type=st.SchemaDataType.ARRAY, items=st.Schema(type=st.SchemaDataType.STRING)),
                    ),
                    st.ContentDescriptor(
                        name='limit',
                        description='maximum number of results to return',
                        schema=st.Schema(type=st.SchemaDataType.INTEGER),
                    ),
                ],
                result=st.ContentDescriptor(
                    name='pet',
                    description='pet response',
                    schema=st.Schema(type=st.SchemaDataType.ARRAY, items=st.Schema(ref='#/components/schemas/Pet')),
                ),
            ),
            st.Method(
                name='create_pet',
                description='Creates a new pet in the store.  Duplicates are allowed',
                params=[
                    st.ContentDescriptor(
                        name='newPet',
                        description='Pet to add to the store.',
                        schema=st.Schema(ref='#/components/schemas/NewPet'),
                    )
                ],
                result=st.ContentDescriptor(
                    name='pet', description='the newly created pet', schema=st.Schema(ref='#/components/schemas/Pet')
                ),
            ),
            st.Method(
                name='get_pet_by_id',
                description='Returns a user based on a single ID, if the user does not have access to the pet',
                params=[
                    st.ContentDescriptor(
                        name='id',
                        description='ID of pet to fetch',
                        required=True,
                        schema=st.Schema(type=st.SchemaDataType.INTEGER),
                    )
                ],
                result=st.ContentDescriptor(
                    name='pet', description='pet response', schema=st.Schema(ref='#/components/schemas/Pet')
                ),
            ),
            st.Method(
                name='delete_pet_by_id',
                description='deletes a single pet based on the ID supplied',
                params=[
                    st.ContentDescriptor(
                        name='id',
                        description='ID of pet to delete',
                        required=True,
                        schema=st.Schema(type=st.SchemaDataType.INTEGER),
                    )
                ],
                result=st.ContentDescriptor(name='pet', description='pet deleted', schema=st.Schema()),
            ),
        ],
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
    )

    assert openrpc_schema_to_dict(openrpc_schema) == {
        'openrpc': '1.0.0-rc1',
        'info': {
            'version': '1.0.0',
            'title': 'Petstore Expanded',
            'description': (
                'A sample API that uses a petstore as an example to demonstrate features in '
                'the OpenRPC specification'
            ),
            'termsOfService': 'https://open-rpc.org',
            'contact': {'name': 'OpenRPC Team', 'email': 'doesntexist@open-rpc.org', 'url': 'https://open-rpc.org'},
            'license': {'name': 'Apache 2.0', 'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'},
        },
        'servers': [{'name': 'default', 'url': 'http://petstore.open-rpc.org'}],
        'methods': [
            {
                'name': 'get_pets',
                'description': (
                    'Returns all pets from the system that the user has access to\n'
                    'Nam sed condimentum est. Maecenas tempor sagittis sapien, nec rhoncus sem sagittis '
                    'sit amet. Aenean at gravida augue, ac iaculis sem. Curabitur odio lorem, ornare '
                    'eget elementum nec, cursus id lectus. Duis mi turpis, pulvinar ac eros ac, '
                    'tincidunt varius justo. In hac habitasse platea dictumst. Integer at adipiscing '
                    'ante, a sagittis ligula. Aenean pharetra tempor ante molestie imperdiet. Vivamus '
                    'id aliquam diam.'
                ),
                'params': [
                    {
                        'name': 'tags',
                        'description': 'tags to filter by',
                        'schema': {'type': 'array', 'items': {'type': 'string'}},
                    },
                    {
                        'name': 'limit',
                        'description': 'maximum number of results to return',
                        'schema': {'type': 'integer'},
                    },
                ],
                'result': {
                    'name': 'pet',
                    'description': 'pet response',
                    'schema': {'type': 'array', 'items': {'$ref': '#/components/schemas/Pet'}},
                },
            },
            {
                'name': 'create_pet',
                'description': 'Creates a new pet in the store.  Duplicates are allowed',
                'params': [
                    {
                        'name': 'newPet',
                        'description': 'Pet to add to the store.',
                        'schema': {'$ref': '#/components/schemas/NewPet'},
                    }
                ],
                'result': {
                    'name': 'pet',
                    'description': 'the newly created pet',
                    'schema': {'$ref': '#/components/schemas/Pet'},
                },
            },
            {
                'name': 'get_pet_by_id',
                'description': 'Returns a user based on a single ID, if the user does not have access to the pet',
                'params': [
                    {'name': 'id', 'description': 'ID of pet to fetch', 'required': True, 'schema': {'type': 'integer'}}
                ],
                'result': {
                    'name': 'pet',
                    'description': 'pet response',
                    'schema': {'$ref': '#/components/schemas/Pet'},
                },
            },
            {
                'name': 'delete_pet_by_id',
                'description': 'deletes a single pet based on the ID supplied',
                'params': [
                    {
                        'name': 'id',
                        'description': 'ID of pet to delete',
                        'required': True,
                        'schema': {'type': 'integer'},
                    }
                ],
                'result': {'name': 'pet', 'description': 'pet deleted', 'schema': {}},
            },
        ],
        'components': {
            'schemas': {
                'Pet': {
                    'allOf': [
                        {'$ref': '#/components/schemas/NewPet'},
                        {'required': ['id'], 'properties': {'id': {'type': 'integer'}}},
                    ]
                },
                'NewPet': {
                    'type': 'object',
                    'required': ['name'],
                    'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}},
                },
            }
        },
        'externalDocs': {
            'url': 'https://github.com/open-rpc/examples/blob/master/service-descriptions/petstore-expanded-openrpc.json'
        },
    }
