Advanced Validation
===================

Flask-JSONRPC supports basic type hints. For complex structures, use JSON
Schema, Pydantic, or Marshmallow.

----

Using JSON Schema
-----------------

.. code-block:: python

   @jsonrpc.method("user.create", schema={
       "type": "object",
       "properties": {
           "name": {"type": "string"},
           "age": {"type": "integer"}
       },
       "required": ["name"]
   })
   def create_user(name: str, age: int = None):
       return {"name": name, "age": age}

----

Using Pydantic Models
---------------------

.. code-block:: python

   from pydantic import BaseModel

   class User(BaseModel):
       name: str
       age: int | None = None

   @jsonrpc.method("user.create")
   def create(user: User):
       return user.dict()
