Quickstart
==========

This Quickstart shows the minimum steps needed to create a JSON-RPC endpoint and
call it from a client.

If you have not installed Flask-JSONRPC yet, see :doc:`installation`.

----

A Minimal Application
---------------------

Create a file called ``app.py``:

.. code-block:: python

   from flask import Flask
   from flask_jsonrpc import JSONRPC

   app = Flask(__name__)

   # Attach the JSON-RPC endpoint at /api
   jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)

   @jsonrpc.method("ping")
   def ping():
       return "pong"

   if __name__ == "__main__":
       app.run(debug=True)

Run it:

.. code-block:: bash

   python app.py

You now have a JSON-RPC server running at:

::

   http://127.0.0.1:5000/api

----

Calling Your Method
-------------------

Using ``curl``:

.. code-block:: bash

   curl -X POST http://127.0.0.1:5000/api \
       -H "Content-Type: application/json" \
       -d '{"jsonrpc": "2.0", "method": "ping", "id": 1}'

The response:

.. code-block:: json

   {"jsonrpc": "2.0", "result": "pong", "id": 1}

----

Using Parameters
----------------

Define a method with parameters:

.. code-block:: python

   @jsonrpc.method("math.add")
   def add(a: int, b: int) -> int:
       return a + b

Call it:

.. code-block:: bash

   curl -X POST http://127.0.0.1:5000/api \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"math.add","params":[3,4],"id":1}'

----

Keyword Parameters
------------------

JSON-RPC also supports keyword parameters:

.. code-block:: python

   @jsonrpc.method("math.mul")
   def mul(*, a: int, b: int) -> int:
       return a * b

Call it:

.. code-block:: json

   {"jsonrpc":"2.0","method":"math.mul","params":{"a":2,"b":6},"id":2}

----

Using the Built-in Web Explorer
-------------------------------

If you enabled it:

.. code-block:: python

   JSONRPC(app, "/api", enable_web_browsable_api=True)

Visit:

::

   http://127.0.0.1:5000/api/browse

You'll see an interactive view of all registered methods.
