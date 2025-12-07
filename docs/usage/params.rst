Parameters
==========

JSON-RPC supports both positional and named parameters. Flask-JSONRPC maps these
directly to Python function arguments.

----

Positional Parameters
---------------------

Consider:

.. code-block:: python

   @jsonrpc.method("math.pow")
   def power(a: int, b: int) -> int:
       return a ** b

Call using a positional array:

.. code-block:: json

   {"method": "math.pow", "params": [2, 8]}

----

Keyword Parameters
------------------

Keyword arguments require a JSON object:

.. code-block:: python

   @jsonrpc.method("greeting.welcome")
   def welcome(*, name: str) -> str:
       return f"Welcome, {name}!"

Call:

.. code-block:: json

   {"method": "greeting.welcome", "params": {"name": "Alice"}}

----

Defaults
--------

Default parameter values work normally:

.. code-block:: python

   @jsonrpc.method("math.inc")
   def inc(x: int, *, amount: int = 1):
       return x + amount

----

Varargs
-------

You may accept variable positional arguments:

.. code-block:: python

   @jsonrpc.method("math.sum")
   def total(*values: int) -> int:
       return sum(values)
