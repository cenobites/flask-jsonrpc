Methods
=======

A JSON-RPC method in Flask-JSONRPC is a Python function decorated with
``@jsonrpc.method("<name>")``. This page describes everything you need to know
about declaring, organizing, documenting, and structuring methods.

----

Declaring Methods
-----------------

The simplest method looks like this:

.. code-block:: python

   @jsonrpc.method("ping")
   def ping():
       return "pong"

The decorator registers the function with the JSON-RPC endpoint at runtime.

----

Method Naming Conventions
-------------------------

JSON-RPC defines method names as strings. Flask-JSONRPC supports:

* simple names: ``"ping"``
* namespaced dot-notation: ``"math.add"``
* nested namespaces: ``"user.profile.update"``

Dot-notation namespaces are recommended because they:

* help organize large APIs
* are displayed hierarchically by the Explorer UI
* avoid name collisions in big applications

----

Docstrings
----------

Docstrings are shown in the web explorer:

.. code-block:: python

   @jsonrpc.method("auth.login")
   def login(username: str, password: str) -> str:
       """Authenticate a user and return a session token."""
       ...

The first line is displayed as the summary, and the remaining lines as extended
documentation.

----

Returning Values
----------------

A JSON-RPC method may return:

* primitives (int, float, str, bool)
* lists
* dictionaries
* objects that Flask can serialize to JSON

If you need custom serialization, see :doc:`../patterns/marshaling`.

----

Raising Errors
--------------

Use ``JSONRPCError`` (see :doc:`errors`) to raise JSON-RPC–compatible errors.
