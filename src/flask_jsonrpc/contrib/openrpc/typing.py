from enum import Enum
import typing as t
from dataclasses import field, dataclass

# Python 3.10+
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

OPENRPC_VERSION_DEFAULT: str = '1.3.2'


class OAuth2FlowType(Enum):
    AUTHORIZATION_CODE = 'authorizationCode'
    CLIENT_CREDENTIALS = 'clientCredentials'
    PASSWORD = 'password'  # nosec B105


@dataclass
class OAuth2Flow:
    type: OAuth2FlowType
    authorization_url: t.Optional[str] = field(default=None, metadata={'field_name': 'authorizationUrl'})
    refresh_url: t.Optional[str] = field(default=None, metadata={'field_name': 'refreshUrl'})
    token_url: t.Optional[str] = field(default=None, metadata={'field_name': 'tokenUrl'})
    scopes: t.Dict[str, str] = field(default_factory=dict)


@dataclass
class OAuth2:
    flows: t.List[OAuth2Flow]
    type: t.Literal['oauth2'] = field(default='oauth2')
    description: t.Optional[str] = field(default=None)


@dataclass
class BearerAuth:
    in_: str = field(metadata={'field_name': 'in'})
    type: t.Literal['bearer'] = field(default='bearer')
    name: str = field(default='Authorization')
    description: t.Optional[str] = field(default=None)
    scopes: t.Dict[str, str] = field(default_factory=dict)


@dataclass
class APIKeyAuth:
    in_: str = field(metadata={'field_name': 'in'})
    type: t.Literal['apikey'] = field(default='apikey')
    name: str = field(default='api_key')
    description: t.Optional[str] = field(default=None)
    scopes: t.Dict[str, str] = field(default_factory=dict)


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
    def of(st: str) -> 'SchemaDataType':
        type_name = st.lower()
        if type_name == 'number':
            return SchemaDataType.INTEGER
        return SchemaDataType(type_name)


@dataclass
class Schema:
    id: t.Optional[str] = field(default=None, metadata={'field_name': '$id'})
    title: t.Optional[str] = field(default=None)
    format: t.Optional[str] = field(default=None)
    enum: t.Optional[t.List[t.Any]] = field(default=None)
    type: t.Optional[t.Union[SchemaDataType, t.List[SchemaDataType]]] = field(
        default=None,
        metadata={'encode': lambda x: getattr(x, 'value', x) if x else x, 'decode': lambda x: x.value if x else x},
    )
    all_of: t.Optional[t.List['Schema']] = field(default=None, metadata={'field_name': 'allOf'})
    any_of: t.Optional[t.List['Schema']] = field(default=None, metadata={'field_name': 'anyOf'})
    one_of: t.Optional[t.List['Schema']] = field(default=None, metadata={'field_name': 'oneOf'})
    not_: t.Optional['Schema'] = field(default=None, metadata={'field_name': 'not'})
    pattern: t.Optional[str] = field(default=None)
    minimum: t.Optional[float] = field(default=None)
    maximum: t.Optional[float] = field(default=None)
    exclusive_minimum: t.Optional[float] = field(default=None, metadata={'field_name': 'exclusiveMinimum'})
    exclusive_maximum: t.Optional[float] = field(default=None, metadata={'field_name': 'exclusiveMaximum'})
    multiple_of: t.Optional[float] = field(default=None, metadata={'field_name': 'multipleOf'})
    min_length: t.Optional[int] = field(default=None, metadata={'field_name': 'minLength'})
    max_length: t.Optional[int] = field(default=None, metadata={'field_name': 'maxLength'})
    properties: t.Optional[t.Dict[str, 'Schema']] = field(default=None)
    pattern_properties: t.Optional[t.Dict[str, 'Schema']] = field(
        default=None, metadata={'field_name': 'patternProperties'}
    )
    additional_properties: t.Optional['Schema'] = field(default=None, metadata={'field_name': 'additionalProperties'})
    property_names: t.Optional['Schema'] = field(default=None, metadata={'field_name': 'propertyNames'})
    min_properties: t.Optional[int] = field(default=None, metadata={'field_name': 'minProperties'})
    max_properties: t.Optional[int] = field(default=None, metadata={'field_name': 'maxProperties'})
    required: t.Optional[t.List[str]] = field(default=None)
    defs: t.Optional[t.Dict[str, 'Schema']] = field(default=None, metadata={'field_name': '$defs'})
    items: t.Optional['Schema'] = field(default=None)
    prefix_items: t.Optional[t.List['Schema']] = field(default=None, metadata={'field_name': 'prefixItems'})
    contains: t.Optional['Schema'] = field(default=None)
    min_contains: t.Optional[int] = field(default=None, metadata={'field_name': 'minContains'})
    max_contains: t.Optional[int] = field(default=None, metadata={'field_name': 'maxContains'})
    min_items: t.Optional[int] = field(default=None, metadata={'field_name': 'minItems'})
    max_items: t.Optional[int] = field(default=None, metadata={'field_name': 'maxItems'})
    unique_items: t.Optional[bool] = field(default=None, metadata={'field_name': 'uniqueItems'})
    ref: t.Optional[str] = field(default=None, metadata={'field_name': '$ref'})
    description: t.Optional[str] = field(default=None)
    deprecated: t.Optional[bool] = field(default=None)
    default: t.Optional[t.Any] = field(default=None)
    examples: t.Optional[t.List[t.Any]] = field(default=None)
    read_only: t.Optional[bool] = field(default=None, metadata={'field_name': 'readOnly'})
    write_only: t.Optional[bool] = field(default=None, metadata={'field_name': 'writeOnly'})
    const: t.Optional[t.Any] = field(default=None)
    dependent_required: t.Optional[t.Dict[str, t.List[str]]] = field(
        default=None, metadata={'field_name': 'dependentRequired'}
    )
    dependent_schemas: t.Optional[t.Dict[str, 'Schema']] = field(
        default=None, metadata={'field_name': 'dependentSchemas'}
    )
    if_: t.Optional['Schema'] = field(default=None, metadata={'field_name': 'if'})
    then: t.Optional['Schema'] = field(default=None)
    else_: t.Optional['Schema'] = field(default=None, metadata={'field_name': 'else'})
    schema_: t.Optional[str] = field(default=None, metadata={'field_name': '$schema'})


@dataclass
class Reference:
    ref: str = field(metadata={'field_name': '$ref'})


@dataclass
class ContentDescriptor:
    name: str
    schema: Schema
    summary: t.Optional[str] = field(default=None)
    description: t.Optional[str] = field(default=None)
    required: t.Optional[bool] = field(default=None)
    deprecated: t.Optional[bool] = field(default=None)


@dataclass
class Contact:
    name: t.Optional[str] = field(default=None)
    url: t.Optional[str] = field(default=None)
    email: t.Optional[str] = field(default=None)


@dataclass
class License:
    name: str
    url: t.Optional[str] = field(default=None)


@dataclass
class Info:
    title: str
    version: str
    description: t.Optional[str] = field(default=None)
    terms_of_service: t.Optional[str] = field(default=None, metadata={'field_name': 'termsOfService'})
    contact: t.Optional[Contact] = field(default=None)
    license: t.Optional[License] = field(default=None)


@dataclass
class ServerVariable:
    default: str
    enum: t.Optional[t.List[str]] = field(default=None)
    description: t.Optional[str] = field(default=None)


@dataclass
class Server:
    url: str
    name: str = field(default='default')
    summary: t.Optional[str] = field(default=None)
    description: t.Optional[str] = field(default=None)
    variables: t.Optional[t.Dict[str, ServerVariable]] = field(default=None)


@dataclass
class Example:
    name: str
    value: t.Any
    summary: t.Optional[str] = field(default=None)
    description: t.Optional[str] = field(default=None)
    external_value: t.Optional[str] = field(default=None, metadata={'field_name': 'externalValue'})


@dataclass
class ExamplePairing:
    name: t.Optional[str] = field(default=None)
    params: t.Optional[t.List[Example]] = field(default=None)
    summary: t.Optional[str] = field(default=None)
    description: t.Optional[str] = field(default=None)
    result: t.Optional[Example] = field(default=None)


@dataclass
class Link:
    name: str
    summary: t.Optional[str] = field(default=None)
    description: t.Optional[str] = field(default=None)
    method: t.Optional[str] = field(default=None)
    params: t.Optional[t.Any] = field(default=None)
    server: t.Optional[Server] = field(default=None)


@dataclass
class Error:
    code: int
    message: str
    data: t.Optional[t.Any] = field(default=None)


@dataclass
class ExternalDocumentation:
    url: str
    description: t.Optional[str] = field(default=None)


@dataclass
class Tag:
    name: str
    summary: t.Optional[str] = field(default=None)
    description: t.Optional[str] = field(default=None)
    external_docs: t.Optional[ExternalDocumentation] = field(default=None, metadata={'field_name': 'externalDocs'})


@dataclass
class Components:
    content_descriptors: t.Optional[t.Dict[str, ContentDescriptor]] = field(
        default=None, metadata={'field_name': 'contentDescriptors'}
    )
    schemas: t.Optional[t.Dict[str, Schema]] = field(default=None)
    examples: t.Optional[t.Dict[str, Example]] = field(default=None)
    links: t.Optional[t.Dict[str, Link]] = field(default=None)
    errors: t.Optional[t.Dict[str, Error]] = field(default=None)
    example_pairing_objects: t.Optional[t.Dict[str, ExamplePairing]] = field(default=None)
    tags: t.Optional[t.Dict[str, Tag]] = field(default=None)
    x_security_schemes: t.Optional[t.Dict[str, t.Union[OAuth2, BearerAuth, APIKeyAuth]]] = field(
        default=None, metadata={'field_name': 'x-security-schemes'}
    )


@dataclass
class Method:
    name: str
    params: t.List[ContentDescriptor]
    result: ContentDescriptor
    tags: t.Optional[t.List[Tag]] = field(default=None)
    summary: t.Optional[str] = field(default=None)
    description: t.Optional[str] = field(default=None)
    external_docs: t.Optional[ExternalDocumentation] = field(default=None, metadata={'field_name': 'externalDocs'})
    deprecated: t.Optional[bool] = field(default=None)
    servers: t.Optional[t.List[Server]] = field(default=None)
    errors: t.Optional[t.List[Error]] = field(default=None)
    links: t.Optional[t.List[Link]] = field(default=None)
    param_structure: t.Optional[ParamStructure] = field(default=None, metadata={'field_name': 'paramStructure'})
    examples: t.Optional[t.List[ExamplePairing]] = field(default=None)
    x_security: t.Optional[t.Dict[str, t.List[str]]] = field(default=None, metadata={'field_name': 'x-security'})


@dataclass
class OpenRPCSchema:
    info: Info
    openrpc: str = field(default=OPENRPC_VERSION_DEFAULT)
    methods: t.List[Method] = field(default_factory=list)
    servers: t.Union[t.List[Server], Server] = field(default_factory=list)
    components: t.Optional[Components] = field(default=None)
    external_docs: t.Optional[ExternalDocumentation] = field(default=None, metadata={'field_name': 'externalDocs'})

    def __post_init__(self: Self) -> None:
        if self.servers is None or (isinstance(self.servers, list) and len(self.servers) == 0):
            self.servers = Server(name='default', url='localhost')
