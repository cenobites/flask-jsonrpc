Errors
======

Flask-JSONRPC implements the JSON-RPC 2.0 error specification and provides
helpers for raising structured errors.

----

Raising Errors
--------------

Use ``JSONRPCError``:

.. code-block:: python

   from flask_jsonrpc.exceptions import JSONRPCError

   @jsonrpc.method("math.safe_div")
   def safe_div(a, b):
       if b == 0:
           raise JSONRPCError(message="Cannot divide by zero")
       return a / b

----

Error Structure
---------------

JSON-RPC errors have these fields:

* ``code`` — integer
* ``message`` — human-readable text
* ``data`` — optional metadata

Example:

.. code-block:: python

   raise JSONRPCError(code=4001, message="Invalid user", data={"user_id": 5})

----

Custom Exception Classes
------------------------

You can subclass ``JSONRPCError``:

.. code-block:: python

   class AuthError(JSONRPCError):
       code = 4010
       message = "Authentication failed"

   @jsonrpc.method("auth.login")
   def login(username, password):
       if not valid(username, password):
           raise AuthError()
