Application Factories
=====================

Flask recommends using **application factories** for flexibility and testability.
Flask-JSONRPC integrates naturally with this pattern.

----

Creating an Application Factory
-------------------------------

.. code-block:: python

   from flask import Flask
   from flask_jsonrpc import JSONRPC

   def create_app(config=None):
       app = Flask(__name__)
       if config:
           app.config.update(config)

       # JSON-RPC endpoint
       jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)

       # Example method
       @jsonrpc.method("ping")
       def ping():
           return "pong"

       return app

----

Benefits
--------

* Easy testing (create multiple app instances)
* Clean separation between app and extensions
* Works with blueprints and modular JSON-RPC endpoints
