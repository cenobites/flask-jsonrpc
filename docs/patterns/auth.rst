Authentication Patterns
=======================

Flask-JSONRPC does not include built-in authentication. Use Flask patterns to
secure your endpoints.

----

Token-based Authentication
--------------------------

You can require a token in request headers:

.. code-block:: python

   from flask import request
   from flask_jsonrpc.exceptions import JSONRPCError

   @jsonrpc.method("secret.echo")
   def echo(message: str):
       token = request.headers.get("X-Auth-Token")
       if token != "my-secret":
           raise JSONRPCError(code=401, message="Unauthorized")
       return message

----

JWT Authentication (Optional Extension)
---------------------------------------

.. code-block:: python

   import jwt

   SECRET_KEY = "supersecret"

   @jsonrpc.method("auth.verify")
   def verify(token: str):
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
       except jwt.InvalidTokenError:
           raise JSONRPCError(code=401, message="Invalid token")
       return payload
