Step 1: Creating the Application
================================

Before you can define any JSON-RPC methods, you need to create a Flask
application. Flask-JSONRPC integrates seamlessly with Flask, so everything starts
in exactly the same way.

In this step, you will:

* create a basic Flask application
* attach a JSON-RPC endpoint
* run your first RPC server

----

Creating the Project
--------------------

Create a project directory:

.. code-block:: bash

   mkdir rpc_tutorial
   cd rpc_tutorial

Create a file named ``app.py``:

.. code-block:: python

   from flask import Flask
   from flask_jsonrpc import JSONRPC

   app = Flask(__name__)

   # Attach the JSON-RPC endpoint at /api
   jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)

   if __name__ == "__main__":
       app.run(debug=True)

At this point you have a working JSON-RPC server — it just has no methods.

You can already start the application:

.. code-block:: bash

   python app.py

You should see output similar to:

.. code-block:: text

   * Serving Flask app 'app'
   * Debug mode: on
   * Running on http://127.0.0.1:5000

----

Opening the Explorer
--------------------

Because you enabled the web-based API explorer, navigate to:

::

   http://127.0.0.1:5000/api/browse

The explorer will show “No methods defined”, which is expected. In the next
step, you will add your first method.
