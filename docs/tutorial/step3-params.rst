Step 3: Parameters and Type Checking
====================================

JSON-RPC supports both positional and keyword parameters. Flask-JSONRPC parses
parameters automatically and supports validation using Python type hints.

In this step, you will:

* use positional parameters
* use keyword parameters
* learn how type hints enable validation

----

Positional Parameters
---------------------

Here is a simple method that expects two integers:

.. code-block:: python

   @jsonrpc.method("math.sub")
   def subtract(a: int, b: int) -> int:
       return a - b

Call it using positional parameters:

.. code-block:: bash

   curl -X POST http://127.0.0.1:5000/api \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"math.sub","params":[10,4],"id":1}'

----

Keyword Parameters
------------------

JSON-RPC also supports keyword arguments:

.. code-block:: python

   @jsonrpc.method("greeting.hello")
   def hello(name: str) -> str:
       return f"Hello, {name}!"

Call it with:

.. code-block:: json

   {
     "jsonrpc": "2.0",
     "method": "greeting.hello",
     "params": {"name": "Alice"},
     "id": 2
   }

----

Type Validation
---------------

Because you annotated your method like:

.. code-block:: python

   def subtract(a: int, b: int) -> int:

Flask-JSONRPC will perform basic type validation.

Try sending a string:

.. code-block:: bash

   curl -X POST http://127.0.0.1:5000/api \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"math.sub","params":["foo",4],"id":1}'

You will receive a JSON-RPC error indicating that ``a`` was expected to be an
integer.

Later, in the Patterns section, you will learn to extend this system using
Pydantic for complex validation.
