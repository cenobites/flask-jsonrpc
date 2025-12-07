Marshaling and Serialization
=============================

Sometimes you need to control how objects are converted to JSON.

----

Returning Custom Objects
------------------------

.. code-block:: python

   class User:
       def __init__(self, name, age):
           self.name = name
           self.age = age

   @jsonrpc.method("user.info")
   def info():
       return User("Alice", 30)

By default, Flask-JSONRPC cannot serialize this. Use a helper:

.. code-block:: python

   from flask_jsonrpc.marshaling import marshal

   @jsonrpc.method("user.info")
   def info():
       user = User("Alice", 30)
       return marshal(user)

----

Integration with Marshmallow
----------------------------

.. code-block:: python

   from marshmallow import Schema, fields

   class UserSchema(Schema):
       name = fields.Str()
       age = fields.Int()

   user_schema = UserSchema()

   @jsonrpc.method("user.info")
   def info():
       user = User("Alice", 30)
       return user_schema.dump(user)
