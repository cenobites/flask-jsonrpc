.. _changelog:

Changelog
=========

This document describes changes between each past release.

Version 4.0.0
-------------

Released on December 9, 2025

This is a major release with significant breaking changes. Please see the :doc:`migration guide <howto/migration/4.0.0>` for detailed upgrade instructions.

Breaking Changes
~~~~~~~~~~~~~~~~

**Python Support**

- Dropped support for Python 3.8 and 3.9
- Minimum Python version is now 3.10
- Added support for Python 3.13 and 3.14
- Experimental support for Python 3.14 free threading

**Dependencies**

- Updated ``typeguard`` from 2.13.3 to 4.4.4 (major version change with breaking API changes)
- Added ``pydantic>=1.7.4,!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0`` as required dependency
- Added ``eval-type-backport==0.3.1`` for enhanced type evaluation
- Added ``annotated-types==0.7.0`` for type metadata support
- Updated ``typing-extensions`` requirement

**API Changes**

- **BREAKING**: Renamed ``JSONRPC`` constructor parameter ``service_url`` to ``path``
- **BREAKING**: Added required ``version`` parameter to ``JSONRPC`` constructor (defaults to '1.0.0')
- Changed ``enable_web_browsable_api`` to accept ``bool | None`` (enables in debug mode when None)
- Modified import style from relative to absolute imports
- Added explicit ``__all__`` exports to main module

**Types Module Restructure**

- **BREAKING**: Restructured ``flask_jsonrpc.types`` from single file to package with submodules:

  - ``flask_jsonrpc.types.types`` - Core type definitions (String, Number, Object, Array, Boolean, Null)
  - ``flask_jsonrpc.types.methods`` - Method annotation types
  - ``flask_jsonrpc.types.params`` - Parameter type definitions

- Moved ``JSONRPCNewType`` to ``flask_jsonrpc.types.types``
- Added new method annotation types: ``Summary``, ``Description``, ``Validate``, ``Notification``, ``Deprecated``, ``Tag``, ``Error``, ``Example``, ``ExampleField``

**Exception Handling**

- Modified ``JSONRPCError`` to pass message to base ``Exception.__init__()``
- Changed default value assignment logic from conditional to ``or`` operator
- Added explicit ``__init__`` methods to all built-in exception classes (``ParseError``, ``InvalidRequestError``, ``MethodNotFoundError``, ``InvalidParamsError``, ``InternalError``, ``ServerError``)
- Added ``original_exception`` parameter to ``ServerError`` for better error tracking

**Configuration**

- Added new ``flask_jsonrpc.conf`` module with settings system
- Settings can be overridden via Flask app config with ``FLASK_JSONRPC_`` prefix
- Settings are auto-loaded during ``init_app()``

**Build System**

- Migrated build backend from setuptools to hatchling
- Added support for Mypyc compilation via hatch-mypyc plugin
- Updated cibuildwheel configuration for Python 3.11+ wheels
- Added uv package manager support
- Removed tox in favor of uv-based testing

New Features
~~~~~~~~~~~~

**Method Annotations**

- Added comprehensive type-safe method annotation system using ``Annotated`` types
- Support for method summary, description, tags, examples, and deprecation markers
- Enhanced API documentation generation from annotations

**Enhanced Browse API**

- Complete redesign of the web browsable API interface
- Added support for Markdown/rich text in method documentation with ``marked.js``
- Integrated CodeMirror-based JSON editor for complex object editing
- Added tag-based directory navigation for better API organization
- Implemented auto-fill of default parameter values
- Enhanced interactive method execution with better error display
- Added middleware system for authentication and custom functionality
- Support for custom dashboard templates in Browse portal
- New favicon and improved branding

**OpenRPC Support**

- Added new ``flask_jsonrpc.contrib.openrpc`` module
- Full OpenRPC specification support for API documentation
- Automatic OpenRPC schema generation from method annotations
- Integration with Browse API for OpenRPC-powered documentation

**Pydantic Integration**

- Native support for Pydantic v1 and v2 models as method parameters and return types
- Automatic validation of Pydantic models
- Enhanced type introspection for Pydantic models
- Support for Pydantic ``BaseModel``, dataclasses, and TypedDict

**Type System Enhancements**

- Added descriptor system for enhanced type inspection (``flask_jsonrpc.descriptor``)
- New function utilities module (``flask_jsonrpc.funcutils``)
- Enhanced encoder support for complex types (``flask_jsonrpc.encoders``)
- Better support for ``Annotated`` types from ``typing_extensions``

**Error Handling**

- Enhanced error handler mechanism with ``@jsonrpc.errorhandler()`` decorator
- Better error propagation and tracking
- Improved error messages and standardization

**Testing & Development**

- Added comprehensive example applications:

  - ``examples/minimal`` - Basic JSON-RPC setup
  - ``examples/minimal-async`` - Async JSON-RPC support
  - ``examples/modular`` - Blueprint-based modular architecture
  - ``examples/multiplesite`` - Multiple JSON-RPC sites
  - ``examples/openrpc`` - OpenRPC integration example
  - ``examples/rpcdescribe`` - RPC Describe portal with authentication
  - ``examples/javascript`` - JavaScript client integration

- Each example now includes:

  - Proper project structure with ``pyproject.toml``
  - Complete test suites
  - ``uv.lock`` for reproducible environments

**Documentation**

- Added comprehensive API documentation with Sphinx
- New tutorial series covering basic to advanced usage
- Pattern guides for authentication, factories, marshaling, and validation
- Usage guides for batch requests, blueprints, errors, methods, parameters, and types
- Deployment guide
- Testing guide
- All documentation now uses Pallets Sphinx theme

**Project Infrastructure**

- Migrated to ``uv`` for dependency management
- Added pre-commit hooks with ``ruff`` for linting
- Configured ``mypy`` and ``pyright`` for type checking
- Added ``bandit`` for security analysis
- Implemented GitHub Actions workflows for CI/CD
- Added CodeQL analysis for security
- Configured Dependabot for automated dependency updates

Improvements
~~~~~~~~~~~~

- Enhanced logging integration with Flask's logging system
- Better JSON-RPC site path and base URL handling
- Improved blueprint registration with better URL prefix handling
- Enhanced async support throughout the codebase
- Better handling of ``None``/``null`` values in responses
- Improved error messages with more context
- Better support for batch requests
- Enhanced notification handling (requests without ``id``)
- Improved type checking and validation performance
- Better support for complex nested types
- Enhanced support for ``Optional`` and ``Union`` types

Bug Fixes
~~~~~~~~~

- Fixed type checker for optional function parameters without default values
- Fixed URN generator for method names
- Fixed relative imports in modular examples
- Fixed integration tests for async applications
- Fixed browse API initial page state for scroll and viewport size
- Fixed continue statements inside try/finally blocks for Mypyc compatibility
- Fixed error message propagation to Exception base class
- Fixed import errors in various submodules

Documentation
~~~~~~~~~~~~~

- Added migration guide from v3.0.1 to v4.0.0
- Updated README with new Python version requirements
- Updated live demo URL to https://flask-jsonrpc.cenobit.es
- Added comprehensive docstrings throughout the codebase
- Enhanced code examples with type annotations
- Updated copyright year to 2025

Deprecations
~~~~~~~~~~~~

- Deprecated ``service_url`` parameter (use ``path`` instead)
- Removed support for Python 3.8 and 3.9
- Removed legacy ``types.py`` single-file module

Internal Changes
~~~~~~~~~~~~~~~~

- Refactored site management system
- Improved view and wrapper classes
- Enhanced globals module for better state management
- Refactored helper functions for better modularity
- Improved test structure with shared test applications
- Added comprehensive unit and integration test coverage (100% coverage target)
- Better separation between sync and async test suites
- Enhanced test fixtures and utilities

Version 3.0.1
-------------

Released on previous date

.. note::
   For changes in version 3.0.1 and earlier, please refer to the git history
   or previous documentation versions.
