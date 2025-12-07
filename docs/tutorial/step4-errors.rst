Step 4: Error Handling
======================

Errors are a core part of JSON-RPC 2.0. Flask-JSONRPC provides helpers for
raising errors that follow the specification.

In this step, you will:

* raise simple errors
* customize error messages
* extend error behavior

----

Raising JSON-RPC Errors
-----------------------

Use ``JSONRPCError``:

.. code-block:: python

   from flask_jsonrpc.exceptions import JSONRPCError

   @jsonrpc.method("math.safe_div")
   def safe_div(a: int, b: int) -> float:
       if b == 0:
           raise JSONRPCError(message="Division by zero")
       return a / b

Call with ``b=0``:

.. code-block:: json

   {
     "jsonrpc": "2.0",
     "error": {
       "code": -32000,
       "message": "Division by zero"
     },
     "id": 1
   }

----

Custom Error Codes
------------------

You may supply your own error code:

.. code-block:: python

   raise JSONRPCError(
       code=4001,
       message="Invalid value",
       data={"value": value}
   )

``data`` is optional metadata returned to the client.

----

Unhandled Exceptions
--------------------

If your method raises an unhandled Python exception, Flask-JSONRPC will convert
it into a generic JSON-RPC error. In debug mode, the stack trace is included in
the server logs.

----

What's Next?
------------

You now have enough knowledge to build simple JSON-RPC services. The next
section, **Usage Guides**, explores the framework in depth, including:

* organizing methods
* nesting namespaces
* using blueprints
* batch requests
* advanced validation
* enabling or customizing the web explorer
