Blueprints
==========

Large applications often need to group JSON-RPC methods using Flask blueprints.
Flask-JSONRPC works well with them.

----

Basic Blueprint Example
-----------------------

.. code-block:: python

   from flask import Blueprint
   from flask_jsonrpc import JSONRPC

   bp = Blueprint("math", __name__)
   jsonrpc = JSONRPC(bp, "/api/math")

   @jsonrpc.method("add")
   def add(a: int, b: int) -> int:
       return a + b

   def create_app():
       app = Flask(__name__)
       app.register_blueprint(bp)
       return app

This creates methods available under:

::

   /api/math

----

Blueprint Namespaces
--------------------

Blueprints handle URL prefixes; JSON-RPC handles method namespaces.

Example:

* URL: ``/api/math``
* Methods: ``math.add``, ``math.mul``

You can mix or separate them based on preference.

----

Multiple Endpoints
------------------

You can attach multiple JSON-RPC endpoints to the same Flask application:

.. code-block:: python

   JSONRPC(app, "/rpc1")
   JSONRPC(app, "/rpc2")
