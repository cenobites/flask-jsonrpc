from enum import Enum
import typing as t

from pydantic import Field, BaseModel, AliasChoices

OPENRPC_VERSION_DEFAULT: str = '1.3.2'


class OAuth2FlowType(Enum):
    AUTHORIZATION_CODE = 'authorizationCode'
    CLIENT_CREDENTIALS = 'clientCredentials'
    PASSWORD = 'password'  # nosec B105


class OAuth2Flow(BaseModel):
    type: OAuth2FlowType
    authorization_url: t.Optional[str] = Field(
        default=None,
        serialization_alias='authorizationUrl',
        validation_alias=AliasChoices('authorizationUrl', 'authorizationUrl'),
    )
    refresh_url: t.Optional[str] = Field(
        default=None, serialization_alias='refreshUrl', validation_alias=AliasChoices('refresh_url', 'refreshUrl')
    )
    token_url: t.Optional[str] = Field(
        default=None, serialization_alias='tokenUrl', validation_alias=AliasChoices('token_url', 'tokenUrl')
    )
    scopes: t.Dict[str, str] = Field(default_factory=dict)


class OAuth2(BaseModel):
    flows: t.List[OAuth2Flow]
    type: t.Literal['oauth2'] = Field(default='oauth2')
    description: t.Optional[str] = None


class BearerAuth(BaseModel):
    in_: str = Field(alias='in')
    type: t.Literal['bearer'] = Field(default='bearer')
    name: str = Field(default='Authorization')
    description: t.Optional[str] = None
    scopes: t.Dict[str, str] = Field(default_factory=dict)


class APIKeyAuth(BaseModel):
    in_: str = Field(alias='in')
    type: t.Literal['apikey'] = Field(default='apikey')
    name: str = Field(default='api_key')
    description: t.Optional[str] = None
    scopes: t.Dict[str, str] = Field(default_factory=dict)


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
    def from_rpc_describe_type(st: str) -> 'SchemaDataType':
        type_name = st.lower()
        if type_name == 'number':
            return SchemaDataType.INTEGER
        return SchemaDataType(type_name)


class Schema(BaseModel):
    id: t.Optional[str] = Field(default=None, serialization_alias='$id', validation_alias=AliasChoices('id', '$id'))
    title: t.Optional[str] = None
    format: t.Optional[str] = None
    enum: t.Optional[t.List[t.Any]] = None
    type: t.Optional[t.Union[SchemaDataType, t.List[SchemaDataType]]] = None
    all_of: t.Optional[t.List['Schema']] = Field(
        default=None, serialization_alias='allOf', validation_alias=AliasChoices('all_of', 'allOf')
    )
    any_of: t.Optional[t.List['Schema']] = Field(
        default=None, serialization_alias='anyOf', validation_alias=AliasChoices('any_of', 'anyOf')
    )
    one_of: t.Optional[t.List['Schema']] = Field(
        default=None, serialization_alias='oneOf', validation_alias=AliasChoices('one_of', 'oneOf')
    )
    not_: t.Optional['Schema'] = Field(
        default=None, serialization_alias='not', validation_alias=AliasChoices('not_', 'not')
    )
    pattern: t.Optional[str] = None
    minimum: t.Optional[float] = None
    maximum: t.Optional[float] = None
    exclusive_minimum: t.Optional[float] = Field(
        default=None,
        serialization_alias='exclusiveMinimum',
        validation_alias=AliasChoices('exclusive_minimum', 'exclusiveMinimum'),
    )
    exclusive_maximum: t.Optional[float] = Field(
        default=None,
        serialization_alias='exclusiveMaximum',
        validation_alias=AliasChoices('exclusive_maximum', 'exclusiveMaximum'),
    )
    multiple_of: t.Optional[float] = Field(
        default=None, serialization_alias='multipleOf', validation_alias=AliasChoices('multiple_of', 'multipleOf')
    )
    min_length: t.Optional[int] = Field(
        default=None, serialization_alias='minLength', validation_alias=AliasChoices('min_length', 'minLength')
    )
    max_length: t.Optional[int] = Field(
        default=None, serialization_alias='maxLength', validation_alias=AliasChoices('max_length', 'maxLength')
    )
    properties: t.Optional[t.Dict[str, 'Schema']] = None
    pattern_properties: t.Optional[t.Dict[str, 'Schema']] = Field(
        default=None,
        serialization_alias='patternProperties',
        validation_alias=AliasChoices('pattern_properties', 'patternProperties'),
    )
    additional_properties: t.Optional['Schema'] = Field(
        default=None,
        serialization_alias='additionalProperties',
        validation_alias=AliasChoices('additional_properties', 'additionalProperties'),
    )
    property_names: t.Optional['Schema'] = Field(
        default=None,
        serialization_alias='propertyNames',
        validation_alias=AliasChoices('property_names', 'propertyNames'),
    )
    min_properties: t.Optional[int] = Field(
        default=None,
        serialization_alias='minProperties',
        validation_alias=AliasChoices('min_properties', 'minProperties'),
    )
    max_properties: t.Optional[int] = Field(
        default=None,
        serialization_alias='maxProperties',
        validation_alias=AliasChoices('max_properties', 'maxProperties'),
    )
    required: t.Optional[t.List[str]] = None
    defs: t.Optional[t.Dict[str, 'Schema']] = Field(
        default=None, serialization_alias='$defs', validation_alias=AliasChoices('defs', '$defs')
    )
    items: t.Optional['Schema'] = None
    prefix_items: t.Optional[t.List['Schema']] = Field(
        default=None, serialization_alias='prefixItems', validation_alias=AliasChoices('prefix_items', 'prefixItems')
    )
    contains: t.Optional['Schema'] = None
    min_contains: t.Optional[int] = Field(
        default=None, serialization_alias='minContains', validation_alias=AliasChoices('min_contains', 'minContains')
    )
    max_contains: t.Optional[int] = Field(
        default=None, serialization_alias='maxContains', validation_alias=AliasChoices('max_contains', 'maxContains')
    )
    min_items: t.Optional[int] = Field(
        default=None, serialization_alias='minItems', validation_alias=AliasChoices('min_items', 'minItems')
    )
    max_items: t.Optional[int] = Field(
        default=None, serialization_alias='maxItems', validation_alias=AliasChoices('max_items', 'maxItems')
    )
    unique_items: t.Optional[bool] = Field(
        default=None, serialization_alias='uniqueItems', validation_alias=AliasChoices('unique_items', 'uniqueItems')
    )
    ref: t.Optional[str] = Field(default=None, serialization_alias='$ref', validation_alias=AliasChoices('ref', '$ref'))
    description: t.Optional[str] = None
    deprecated: t.Optional[bool] = None
    default: t.Optional[t.Any] = None
    examples: t.Optional[t.List[t.Any]] = None
    read_only: t.Optional[bool] = Field(
        default=None, serialization_alias='readOnly', validation_alias=AliasChoices('read_only', 'readOnly')
    )
    write_only: t.Optional[bool] = Field(
        default=None, serialization_alias='writeOnly', validation_alias=AliasChoices('write_only', 'writeOnly')
    )
    const: t.Optional[t.Any] = None
    dependent_required: t.Optional[t.Dict[str, t.List[str]]] = Field(
        default=None,
        serialization_alias='dependentRequired',
        validation_alias=AliasChoices('dependent_required', 'dependentRequired'),
    )
    dependent_schemas: t.Optional[t.Dict[str, 'Schema']] = Field(
        default=None,
        serialization_alias='dependentSchemas',
        validation_alias=AliasChoices('dependent_schemas', 'dependentSchemas'),
    )
    if_: t.Optional['Schema'] = Field(
        default=None, serialization_alias='if', validation_alias=AliasChoices('if_', 'if')
    )
    then: t.Optional['Schema'] = None
    else_: t.Optional['Schema'] = Field(
        default=None, serialization_alias='else', validation_alias=AliasChoices('else_', 'else')
    )
    schema_: t.Optional[str] = Field(
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
    summary: t.Optional[str] = None
    description: t.Optional[str] = None
    required: t.Optional[bool] = None
    deprecated: t.Optional[bool] = None


class Contact(BaseModel):
    name: t.Optional[str] = None
    url: t.Optional[str] = None
    email: t.Optional[str] = None


class License(BaseModel):
    name: str
    url: t.Optional[str] = None


class Info(BaseModel):
    title: str
    version: str
    description: t.Optional[str] = None
    terms_of_service: t.Optional[str] = Field(
        default=None,
        serialization_alias='termsOfService',
        validation_alias=AliasChoices('terms_of_service', 'termsOfService'),
    )
    contact: t.Optional[Contact] = None
    license_: t.Optional[License] = Field(
        default=None, alias='license', validation_alias=AliasChoices('license_', 'license')
    )


class ServerVariable(BaseModel):
    default: str
    enum: t.Optional[t.List[str]] = None
    description: t.Optional[str] = None


class Server(BaseModel):
    url: str
    name: str = Field(default='default')
    summary: t.Optional[str] = None
    description: t.Optional[str] = None
    variables: t.Optional[t.Dict[str, ServerVariable]] = None


class Example(BaseModel):
    name: str
    value: t.Any
    summary: t.Optional[str] = None
    description: t.Optional[str] = None
    external_value: t.Optional[str] = Field(
        default=None,
        serialization_alias='externalValue',
        validation_alias=AliasChoices('external_value', 'externalValue'),
    )


class ExamplePairing(BaseModel):
    name: t.Optional[str] = None
    params: t.Optional[t.List[Example]] = None
    summary: t.Optional[str] = None
    description: t.Optional[str] = None
    result: t.Optional[Example] = None


class Link(BaseModel):
    name: str
    summary: t.Optional[str] = None
    description: t.Optional[str] = None
    method: t.Optional[str] = None
    params: t.Optional[t.Any] = None
    server: t.Optional[Server] = None


class Error(BaseModel):
    code: int
    message: str
    data: t.Optional[t.Any] = None


class ExternalDocumentation(BaseModel):
    url: str
    description: t.Optional[str] = None


class Tag(BaseModel):
    name: str
    summary: t.Optional[str] = None
    description: t.Optional[str] = None
    external_docs: t.Optional[ExternalDocumentation] = Field(
        default=None, serialization_alias='externalDocs', validation_alias=AliasChoices('external_docs', 'externalDocs')
    )


class Components(BaseModel):
    content_descriptors: t.Optional[t.Dict[str, ContentDescriptor]] = Field(
        default=None,
        serialization_alias='contentDescriptors',
        validation_alias=AliasChoices('content_descriptors', 'contentDescriptors'),
    )
    schemas: t.Optional[t.Dict[str, Schema]] = None
    examples: t.Optional[t.Dict[str, Example]] = None
    links: t.Optional[t.Dict[str, Link]] = None
    errors: t.Optional[t.Dict[str, Error]] = None
    example_pairing_objects: t.Optional[t.Dict[str, ExamplePairing]] = None
    tags: t.Optional[t.Dict[str, Tag]] = None
    x_security_schemes: t.Optional[t.Dict[str, t.Union[OAuth2, BearerAuth, APIKeyAuth]]] = Field(
        default=None,
        serialization_alias='x-security-schemes',
        validation_alias=AliasChoices('x_security_schemes', 'x-security-schemes'),
    )


class Method(BaseModel):
    name: str
    params: t.List[ContentDescriptor]
    result: ContentDescriptor
    tags: t.Optional[t.List[Tag]] = None
    summary: t.Optional[str] = None
    description: t.Optional[str] = None
    external_docs: t.Optional[ExternalDocumentation] = Field(
        default=None, serialization_alias='externalDocs', validation_alias=AliasChoices('external_docs', 'externalDocs')
    )
    deprecated: t.Optional[bool] = None
    servers: t.Optional[t.List[Server]] = None
    errors: t.Optional[t.List[Error]] = None
    links: t.Optional[t.List[Link]] = None
    param_structure: t.Optional[ParamStructure] = Field(
        default=None,
        serialization_alias='paramStructure',
        validation_alias=AliasChoices('param_structure', 'paramStructure'),
    )
    examples: t.Optional[t.List[ExamplePairing]] = None
    x_security: t.Optional[t.Dict[str, t.List[str]]] = Field(
        default=None, serialization_alias='x-security', validation_alias=AliasChoices('x_security', 'x-security')
    )


class OpenRPCSchema(BaseModel):
    info: Info
    openrpc: str = Field(default=OPENRPC_VERSION_DEFAULT)
    methods: t.List[Method] = []
    servers: t.Union[t.List[Server], Server] = Server(name='default', url='localhost')
    components: t.Optional[Components] = None
    external_docs: t.Optional[ExternalDocumentation] = Field(
        default=None, serialization_alias='externalDocs', validation_alias=AliasChoices('external_docs', 'externalDocs')
    )
