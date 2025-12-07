Step 2: Declaring Methods
=========================

Now that you have a running application, you can begin declaring JSON-RPC
methods. A method is simply a Python function decorated with
``@jsonrpc.method("<name>")``.

In this step, you will:

* define your first method
* call it using a JSON-RPC request
* see how method names form a global namespace

----

Your First Method
-----------------

Open ``app.py`` and add:

.. code-block:: python

   @jsonrpc.method("ping")
   def ping():
       return "pong"

Restart the server:

.. code-block:: bash

   python app.py

Call it using ``curl``:

.. code-block:: bash

   curl -X POST http://127.0.0.1:5000/api \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"ping","id":1}'

You should see:

.. code-block:: text

   {"jsonrpc": "2.0", "result": "pong", "id": 1}

----

Method Names and Grouping
-------------------------

Method names in JSON-RPC form a *flat namespace*. However, Flask-JSONRPC allows
you to emulate structured namespaces:

.. code-block:: python

   @jsonrpc.method("math.add")
   def add(a, b):
       return a + b

   @jsonrpc.method("math.mul")
   def mul(a, b):
       return a * b

These names appear grouped under ``math`` in the explorer.

----

Browse the Explorer
-------------------

Visit:

::

   http://127.0.0.1:5000/api/browse

You will now see:

* ``ping``
* ``math.add``
* ``math.mul``

Click any method to view its description. Later, you will learn to control the
metadata shown in the explorer using docstrings and type hints.
