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

import typing as t
from collections import OrderedDict
from urllib.parse import urlsplit

# Added in version 3.11.
from typing_extensions import Self

from flask_jsonrpc import typing as fjt
from flask_jsonrpc.conf import settings
from flask_jsonrpc.types import params as types_params, methods as types_methods
from flask_jsonrpc.helpers import from_python_type
from flask_jsonrpc.types.types import Object, propertify

if t.TYPE_CHECKING:
    from flask_jsonrpc.site import JSONRPCSite

JSONRPC_DESCRIBE_METHOD_NAME: str = 'rpc.describe'
JSONRPC_DESCRIBE_SERVICE_METHOD_TYPE: str = 'method'


class JSONRPCServiceDescriptor:
    """JSON-RPC Service Descriptor for JSON-RPC 2.0.

    It provides a detailed description of the JSON-RPC service, including its methods,
    parameters, return types, and other metadata.

    Args:
        jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): JSON-RPC site instance.

    Attributes:
        jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): JSON-RPC site instance.
    """

    def __init__(self: Self, jsonrpc_site: JSONRPCSite) -> None:
        self.jsonrpc_site = jsonrpc_site
        self.register(jsonrpc_site)

    def _python_type_name(self: Self, pytype: t.Any) -> str:  # noqa: ANN401
        """Get the JSON-RPC type name for a given Python type.

        Args:
            pytype (typing.Any): Python type.

        Returns:
            str: JSON-RPC type name.
        """
        return str(from_python_type(pytype))

    def _build_field_desc(self: Self, field: fjt.Field, annotations: t.Annotated[t.Any, ...]) -> fjt.Field:  # noqa: ANN401, C901
        """Build a field description from annotations.

        Args:
            field (flask_jsonrpc.typing.Field): Field instance.
            annotations (typing.Annotated[typing.Any, ...]): Annotations for the field.

        Returns:
            flask_jsonrpc.typing.Field: Field instance with updated description.
        """
        for annotation in annotations:
            if isinstance(annotation, types_params.Summary):
                field.summary = annotation.summary
                continue
            if isinstance(annotation, types_params.Description):
                field.description = annotation.description
                continue
            if isinstance(annotation, types_params.Properties):
                field.properties = (
                    self._properties_to_fields(annotation.annotations)
                    if isinstance(annotation.annotations, dict)
                    else None
                )
                continue
            if isinstance(annotation, types_params.Example):
                if field.examples is None:  # pragma: no cover
                    field.examples = []
                field.examples.append(annotation.value)
                continue
            if isinstance(annotation, types_params.Required):
                field.required = annotation.required
                continue
            if isinstance(annotation, types_params.Deprecated):
                field.deprecated = annotation.deprecated
                continue
            if isinstance(annotation, types_params.Nullable):
                field.nullable = annotation.nullable
                continue
            if isinstance(annotation, types_params.Maximum):
                field.maximum = annotation.maximum
                continue
            if isinstance(annotation, types_params.Minimum):
                field.minimum = annotation.minimum
                continue
            if isinstance(annotation, types_params.MultipleOf):
                field.multiple_of = annotation.multiple_of
                continue
            if isinstance(annotation, types_params.MaxLength):
                field.max_length = annotation.max_length
                continue
            if isinstance(annotation, types_params.MinLength):
                field.min_length = annotation.min_length
                continue
            if isinstance(annotation, types_params.Pattern):
                field.pattern = annotation.pattern
                continue
            if isinstance(annotation, types_params.AllowInfNan):
                field.allow_inf_nan = annotation.allow_inf_nan
                continue
            if isinstance(annotation, types_params.MaxDigits):
                field.max_digits = annotation.max_digits
                continue
            if isinstance(annotation, types_params.DecimalPlaces):
                field.decimal_places = annotation.decimal_places
                continue
        return field

    def _properties_to_fields(
        self: Self, annotations: dict[str, t.Annotated[t.Any, ...] | t.Any]
    ) -> dict[str, fjt.Field] | None:
        """Convert properties annotations to field descriptions.

        Args:
            annotations (dict[str, typing.Annotated[typing.Any, ...] | typing.Any]): Annotations for the properties.

        Returns:
            dict[str, flask_jsonrpc.typing.Field] | None: Field descriptions for the properties.
        """
        fields = {}
        for name, annotation in annotations.items():
            if isinstance(annotation, types_params.Properties):
                field_type = Object.name
                properties = (
                    self._properties_to_fields(annotation.annotations)
                    if isinstance(annotation.annotations, dict)
                    else None
                )
                fields[name] = fjt.Field(name=name, type=field_type, properties=properties if properties else None)
                continue
            field = fjt.Field(name=name, type=self._python_type_name(getattr(annotation, '__origin__', type(None))))
            fields[name] = self._build_field_desc(field, getattr(annotation, '__metadata__', ()))
        return fields

    def _build_service_field_desc(self: Self, name: str, obj: t.Any) -> fjt.Field:  # noqa: ANN401, C901
        """Build a service field description from a Python type.

        Args:
            name (str): Field name.
            obj (typing.Any): Python type.

        Returns:
            flask_jsonrpc.typing.Field: Field description.
        """
        annotations = getattr(obj, '__metadata__', ())
        obj_type = getattr(obj, '__origin__', obj) if t.get_origin(obj) is t.Annotated else obj
        field_type = self._python_type_name(obj_type)
        field = fjt.Field(name=name, type=field_type)
        if (
            len([x for x in annotations if isinstance(x, types_params.Properties)]) == 0
            and from_python_type(obj_type, default=None) is None
        ):
            properties = propertify(obj_type)
            annotations = annotations + (properties,)
        return self._build_field_desc(field, annotations)

    def _service_method_params_desc(self: Self, view_func: t.Callable[..., t.Any]) -> list[fjt.Field]:
        """Get the service method parameters description.

        Args:
            view_func (typing.Callable[..., typing.Any]): The view function.

        Returns:
            list[flask_jsonrpc.typing.Field]: List of field descriptions.
        """
        view_func_params = getattr(view_func, 'jsonrpc_method_params', {})
        fields = []
        for param_name, param_type in view_func_params.items():
            fields.append(self._build_service_field_desc(param_name, param_type))
        return fields

    def _service_method_returns_desc(self: Self, view_func: t.Callable[..., t.Any]) -> fjt.Field:
        """Get the service method return description.

        Args:
            view_func (typing.Callable[..., typing.Any]): The view function.

        Returns:
            flask_jsonrpc.typing.Field: Field description.
        """
        view_func_return_type = getattr(view_func, 'jsonrpc_method_return', type(None))
        return self._build_service_field_desc('default', view_func_return_type)

    def _service_methods_desc(self: Self) -> t.OrderedDict[str, fjt.Method]:  # noqa: C901
        """Get the service methods description.

        Returns:
            OrderedDict[str, flask_jsonrpc.typing.Method]: Ordered dictionary of method descriptions.
        """
        methods: t.OrderedDict[str, fjt.Method] = OrderedDict()
        for name, view_func in self.jsonrpc_site.view_funcs.items():
            method_name = getattr(view_func, 'jsonrpc_method_name', name)
            method_annotation: t.Any | types_methods.MethodAnnotatedType = getattr(
                view_func,
                'jsonrpc_method_annotations',
                types_methods.MethodAnnotated[None],  # type: ignore
            )
            method_metadata = getattr(method_annotation, '__metadata__', ())
            method_options = getattr(view_func, 'jsonrpc_options', {})
            method = fjt.Method(
                name=method_name,
                type=JSONRPC_DESCRIBE_SERVICE_METHOD_TYPE,
                validation=method_options.get('validate', settings.DEFAULT_JSONRPC_METHOD_VALIDATE),
                notification=method_options.get('notification', settings.DEFAULT_JSONRPC_METHOD_NOTIFICATION),
                params=self._service_method_params_desc(view_func),
                returns=self._service_method_returns_desc(view_func),
            )
            # mypyc: pydantic optional value
            method.description = getattr(view_func, '__doc__', None)
            for metadata in method_metadata:
                if isinstance(metadata, types_methods.Summary):
                    method.summary = metadata.summary
                    continue
                if isinstance(metadata, types_methods.Description):
                    method.description = metadata.description
                    continue
                if isinstance(metadata, types_methods.Validate):
                    method.validation = metadata.validate
                    continue
                if isinstance(metadata, types_methods.Notification):
                    method.notification = metadata.notification
                    continue
                if isinstance(metadata, types_methods.Deprecated):
                    method.deprecated = metadata.deprecated
                    continue
                if isinstance(metadata, types_methods.Tag):
                    if method.tags is None:  # pragma: no cover
                        method.tags = []
                    method.tags.append(metadata.name)
                    continue
                if isinstance(metadata, types_methods.Error):
                    if method.errors is None:  # pragma: no cover
                        method.errors = []
                    method.errors.append(
                        fjt.Error(
                            code=metadata.code,
                            message=metadata.message,
                            status_code=metadata.status_code,
                            data=metadata.data,
                        )
                    )
                    continue
                if isinstance(metadata, types_methods.Example):
                    if method.examples is None:  # pragma: no cover
                        method.examples = []
                    method.examples.append(
                        fjt.Example(
                            name=metadata.name,
                            summary=metadata.summary,
                            description=metadata.description,
                            params=[
                                fjt.ExampleField(
                                    name=param.name,
                                    value=param.value,
                                    summary=param.summary,
                                    description=param.description,
                                )
                                for param in (metadata.params or [])
                            ],
                            returns=fjt.ExampleField(
                                name=metadata.returns.name,
                                value=metadata.returns.value,
                                summary=metadata.returns.summary,
                                description=metadata.returns.description,
                            )
                            if metadata.returns is not None
                            else None,
                        )
                    )
                    continue

            methods[method_name] = method
        return methods

    def _service_server_url(self: Self) -> str:
        """Get the service server URL.

        Returns:
            str: Service server URL.
        """
        url = urlsplit(self.jsonrpc_site.base_url or self.jsonrpc_site.path or '')
        return (
            f'{url.scheme}://{url.netloc}/{(self.jsonrpc_site.path or "").lstrip("/")}'
            if self.jsonrpc_site.base_url
            else url.path
        )

    def service_describe(self: Self) -> fjt.ServiceDescribe:
        """Get the service description.

        Returns:
            flask_jsonrpc.typing.ServiceDescribe: Service description.
        """
        from flask_jsonrpc.site import JSONRPCSite

        serv_desc = fjt.ServiceDescribe(
            id=f'urn:uuid:{self.jsonrpc_site.uuid}',
            version=self.jsonrpc_site.version,
            name=self.jsonrpc_site.name,
            servers=[fjt.Server(url=self._service_server_url())],
            methods=self._service_methods_desc(),
        )
        # mypyc: pydantic optional value
        serv_desc.description = (
            self.jsonrpc_site.__doc__ if self.jsonrpc_site.__doc__ != getattr(JSONRPCSite, '__doc__', None) else None
        )
        return serv_desc

    def register(self: Self, jsonrpc_site: JSONRPCSite) -> None:
        """Register the service description method.

        The 'rpc.describe' is automatically registered to provide service description.

        Args:
            jsonrpc_site (flask_jsonrpc.site.JSONRPCSite): JSON-RPC site instance.

        Examples:
            >>> from flask import Flask
            >>> from flask_jsonrpc import JSONRPC
            >>>
            >>> app = Flask(__name__)
            >>> jsonrpc = JSONRPC(app, path='/api', version='1.0.0')
            >>> assert 'rpc.describe' in jsonrpc.get_jsonrpc_site().view_funcs
        """

        def describe() -> fjt.ServiceDescribe:
            return self.service_describe()

        describe.__doc__ = 'Service description for JSON-RPC 2.0'

        typing_annotations: types_methods.MethodAnnotatedType = types_methods.MethodAnnotated[
            types_methods.Summary('RPC Describe'),
            types_methods.Description('Service description for JSON-RPC 2.0'),
            types_methods.Validate(False),
            types_methods.Notification(False),
        ]
        fn_annotations = {'return': t.Annotated[fjt.ServiceDescribe, None]}
        setattr(describe, 'jsonrpc_method_name', JSONRPC_DESCRIBE_METHOD_NAME)  # noqa: B010
        setattr(describe, 'jsonrpc_method_sig', fn_annotations.copy())  # noqa: B010
        setattr(describe, 'jsonrpc_method_return', fn_annotations.pop('return'))  # noqa: B010
        setattr(describe, 'jsonrpc_method_params', fn_annotations)  # noqa: B010
        setattr(describe, 'jsonrpc_method_annotations', typing_annotations)  # noqa: B010
        setattr(describe, 'jsonrpc_validate', False)  # noqa: B010
        setattr(describe, 'jsonrpc_notification', False)  # noqa: B010
        setattr(describe, 'jsonrpc_options', {'notification': False, 'validate': False})  # noqa: B010
        jsonrpc_site.register(JSONRPC_DESCRIBE_METHOD_NAME, describe)
        self.describe = describe
