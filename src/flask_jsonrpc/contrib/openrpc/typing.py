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
from __future__ import annotations

from enum import Enum
import typing as t

from pydantic import Field, ConfigDict, AliasChoices
from pydantic.main import BaseModel as PydanticModel

OPENRPC_VERSION_DEFAULT: str = '1.3.2'


class BaseModel(PydanticModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True, arbitrary_types_allowed=True)


class OAuth2FlowType(Enum):
    AUTHORIZATION_CODE = 'authorizationCode'
    CLIENT_CREDENTIALS = 'clientCredentials'
    PASSWORD = 'password'  # nosec B105


class OAuth2Flow(BaseModel):
    type: OAuth2FlowType
    authorization_url: str | None = Field(
        default=None,
        serialization_alias='authorizationUrl',
        validation_alias=AliasChoices('authorizationUrl', 'authorizationUrl'),
    )
    refresh_url: str | None = Field(
        default=None, serialization_alias='refreshUrl', validation_alias=AliasChoices('refresh_url', 'refreshUrl')
    )
    token_url: str | None = Field(
        default=None, serialization_alias='tokenUrl', validation_alias=AliasChoices('token_url', 'tokenUrl')
    )
    scopes: dict[str, str] = Field(default_factory=dict)


class OAuth2(BaseModel):
    flows: list[OAuth2Flow]
    type: t.Literal['oauth2'] = Field(default='oauth2')
    description: str | None = None


class BearerAuth(BaseModel):
    in_: str = Field(alias='in')
    type: t.Literal['bearer'] = Field(default='bearer')
    name: str = Field(default='Authorization')
    description: str | None = None
    scopes: dict[str, str] = Field(default_factory=dict)


class APIKeyAuth(BaseModel):
    in_: str = Field(alias='in')
    type: t.Literal['apikey'] = Field(default='apikey')
    name: str = Field(default='api_key')
    description: str | None = None
    scopes: dict[str, str] = Field(default_factory=dict)


class ParamStructure(Enum):
    BY_NAME = 'by-name'
    BY_POSITION = 'by-position'
    EITHER = 'either'


class SchemaDataType(Enum):
    NULL = 'null'
    BOOLEAN = 'boolean'
    OBJECT = 'object'
    ARRAY = 'array'
    INTEGER = 'integer'
    STRING = 'string'

    @staticmethod
    def from_rpc_describe_type(st: str) -> SchemaDataType:
        type_name = st.lower()
        if type_name == 'number':
            return SchemaDataType.INTEGER
        return SchemaDataType(type_name)


class Schema(BaseModel):
    id: str | None = Field(default=None, serialization_alias='$id', validation_alias=AliasChoices('id', '$id'))
    title: str | None = None
    format: str | None = None
    enum: list[t.Any] | None = None
    type: SchemaDataType | list[SchemaDataType] | None = None
    all_of: list[Schema] | None = Field(
        default=None, serialization_alias='allOf', validation_alias=AliasChoices('all_of', 'allOf')
    )
    any_of: list[Schema] | None = Field(
        default=None, serialization_alias='anyOf', validation_alias=AliasChoices('any_of', 'anyOf')
    )
    one_of: list[Schema] | None = Field(
        default=None, serialization_alias='oneOf', validation_alias=AliasChoices('one_of', 'oneOf')
    )
    not_: Schema | None = Field(default=None, serialization_alias='not', validation_alias=AliasChoices('not_', 'not'))
    pattern: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    exclusive_minimum: float | None = Field(
        default=None,
        serialization_alias='exclusiveMinimum',
        validation_alias=AliasChoices('exclusive_minimum', 'exclusiveMinimum'),
    )
    exclusive_maximum: float | None = Field(
        default=None,
        serialization_alias='exclusiveMaximum',
        validation_alias=AliasChoices('exclusive_maximum', 'exclusiveMaximum'),
    )
    multiple_of: float | None = Field(
        default=None, serialization_alias='multipleOf', validation_alias=AliasChoices('multiple_of', 'multipleOf')
    )
    min_length: int | None = Field(
        default=None, serialization_alias='minLength', validation_alias=AliasChoices('min_length', 'minLength')
    )
    max_length: int | None = Field(
        default=None, serialization_alias='maxLength', validation_alias=AliasChoices('max_length', 'maxLength')
    )
    properties: dict[str, Schema] | None = None
    pattern_properties: dict[str, Schema] | None = Field(
        default=None,
        serialization_alias='patternProperties',
        validation_alias=AliasChoices('pattern_properties', 'patternProperties'),
    )
    additional_properties: Schema | None = Field(
        default=None,
        serialization_alias='additionalProperties',
        validation_alias=AliasChoices('additional_properties', 'additionalProperties'),
    )
    property_names: Schema | None = Field(
        default=None,
        serialization_alias='propertyNames',
        validation_alias=AliasChoices('property_names', 'propertyNames'),
    )
    min_properties: int | None = Field(
        default=None,
        serialization_alias='minProperties',
        validation_alias=AliasChoices('min_properties', 'minProperties'),
    )
    max_properties: int | None = Field(
        default=None,
        serialization_alias='maxProperties',
        validation_alias=AliasChoices('max_properties', 'maxProperties'),
    )
    required: list[str] | None = None
    defs: dict[str, Schema] | None = Field(
        default=None, serialization_alias='$defs', validation_alias=AliasChoices('defs', '$defs')
    )
    items: Schema | None = None
    prefix_items: list[Schema] | None = Field(
        default=None, serialization_alias='prefixItems', validation_alias=AliasChoices('prefix_items', 'prefixItems')
    )
    contains: Schema | None = None
    min_contains: int | None = Field(
        default=None, serialization_alias='minContains', validation_alias=AliasChoices('min_contains', 'minContains')
    )
    max_contains: int | None = Field(
        default=None, serialization_alias='maxContains', validation_alias=AliasChoices('max_contains', 'maxContains')
    )
    min_items: int | None = Field(
        default=None, serialization_alias='minItems', validation_alias=AliasChoices('min_items', 'minItems')
    )
    max_items: int | None = Field(
        default=None, serialization_alias='maxItems', validation_alias=AliasChoices('max_items', 'maxItems')
    )
    unique_items: bool | None = Field(
        default=None, serialization_alias='uniqueItems', validation_alias=AliasChoices('unique_items', 'uniqueItems')
    )
    ref: str | None = Field(default=None, serialization_alias='$ref', validation_alias=AliasChoices('ref', '$ref'))
    description: str | None = None
    deprecated: bool | None = None
    default: t.Any | None = None
    examples: list[t.Any] | None = None
    read_only: bool | None = Field(
        default=None, serialization_alias='readOnly', validation_alias=AliasChoices('read_only', 'readOnly')
    )
    write_only: bool | None = Field(
        default=None, serialization_alias='writeOnly', validation_alias=AliasChoices('write_only', 'writeOnly')
    )
    const: t.Any | None = None
    dependent_required: dict[str, list[str]] | None = Field(
        default=None,
        serialization_alias='dependentRequired',
        validation_alias=AliasChoices('dependent_required', 'dependentRequired'),
    )
    dependent_schemas: dict[str, Schema] | None = Field(
        default=None,
        serialization_alias='dependentSchemas',
        validation_alias=AliasChoices('dependent_schemas', 'dependentSchemas'),
    )
    if_: Schema | None = Field(default=None, serialization_alias='if', validation_alias=AliasChoices('if_', 'if'))
    then: Schema | None = None
    else_: Schema | None = Field(
        default=None, serialization_alias='else', validation_alias=AliasChoices('else_', 'else')
    )
    schema_: str | None = Field(
        default=None,
        alias='schema',
        serialization_alias='$schema',
        validation_alias=AliasChoices('schema_', 'schema', '$schema'),
    )


class Reference(BaseModel):
    ref: str = Field(serialization_alias='$ref', validation_alias=AliasChoices('ref', '$ref'))


class ContentDescriptor(BaseModel):
    name: str
    schema_: Schema = Field(alias='schema', validation_alias=AliasChoices('schema_', 'schema'))
    summary: str | None = None
    description: str | None = None
    required: bool | None = None
    deprecated: bool | None = None


class Contact(BaseModel):
    name: str | None = None
    url: str | None = None
    email: str | None = None


class License(BaseModel):
    name: str
    url: str | None = None


class Info(BaseModel):
    title: str
    version: str
    description: str | None = None
    terms_of_service: str | None = Field(
        default=None,
        serialization_alias='termsOfService',
        validation_alias=AliasChoices('terms_of_service', 'termsOfService'),
    )
    contact: Contact | None = None
    license_: License | None = Field(
        default=None, alias='license', validation_alias=AliasChoices('license_', 'license')
    )


class ServerVariable(BaseModel):
    default: str
    enum: list[str] | None = None
    description: str | None = None


class Server(BaseModel):
    url: str
    name: str = Field(default='default')
    summary: str | None = None
    description: str | None = None
    variables: dict[str, ServerVariable] | None = None


class Example(BaseModel):
    name: str
    value: t.Any
    summary: str | None = None
    description: str | None = None
    external_value: str | None = Field(
        default=None,
        serialization_alias='externalValue',
        validation_alias=AliasChoices('external_value', 'externalValue'),
    )


class ExamplePairing(BaseModel):
    name: str | None = None
    params: list[Example] | None = None
    summary: str | None = None
    description: str | None = None
    result: Example | None = None


class Link(BaseModel):
    name: str
    summary: str | None = None
    description: str | None = None
    method: str | None = None
    params: t.Any | None = None
    server: Server | None = None


class Error(BaseModel):
    code: int
    message: str
    data: t.Any | None = None


class ExternalDocumentation(BaseModel):
    url: str
    description: str | None = None


class Tag(BaseModel):
    name: str
    summary: str | None = None
    description: str | None = None
    external_docs: ExternalDocumentation | None = Field(
        default=None, serialization_alias='externalDocs', validation_alias=AliasChoices('external_docs', 'externalDocs')
    )


class Components(BaseModel):
    content_descriptors: dict[str, ContentDescriptor] | None = Field(
        default=None,
        serialization_alias='contentDescriptors',
        validation_alias=AliasChoices('content_descriptors', 'contentDescriptors'),
    )
    schemas: dict[str, Schema] | None = None
    examples: dict[str, Example] | None = None
    links: dict[str, Link] | None = None
    errors: dict[str, Error] | None = None
    example_pairing_objects: dict[str, ExamplePairing] | None = None
    tags: dict[str, Tag] | None = None
    x_security_schemes: dict[str, OAuth2 | BearerAuth | APIKeyAuth] | None = Field(
        default=None,
        serialization_alias='x-security-schemes',
        validation_alias=AliasChoices('x_security_schemes', 'x-security-schemes'),
    )


class Method(BaseModel):
    name: str
    params: list[ContentDescriptor]
    result: ContentDescriptor
    tags: list[Tag] | None = None
    summary: str | None = None
    description: str | None = None
    external_docs: ExternalDocumentation | None = Field(
        default=None, serialization_alias='externalDocs', validation_alias=AliasChoices('external_docs', 'externalDocs')
    )
    deprecated: bool | None = None
    servers: list[Server] | None = None
    errors: list[Error] | None = None
    links: list[Link] | None = None
    param_structure: ParamStructure | None = Field(
        default=None,
        serialization_alias='paramStructure',
        validation_alias=AliasChoices('param_structure', 'paramStructure'),
    )
    examples: list[ExamplePairing] | None = None
    x_security: dict[str, list[str]] | None = Field(
        default=None, serialization_alias='x-security', validation_alias=AliasChoices('x_security', 'x-security')
    )


class OpenRPCSchema(BaseModel):
    info: Info
    openrpc: str = Field(default=OPENRPC_VERSION_DEFAULT)
    methods: list[Method] = []
    servers: list[Server] | Server = Server(name='default', url='localhost')
    components: Components | None = None
    external_docs: ExternalDocumentation | None = Field(
        default=None, serialization_alias='externalDocs', validation_alias=AliasChoices('external_docs', 'externalDocs')
    )
