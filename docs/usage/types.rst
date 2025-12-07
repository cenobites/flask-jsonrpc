Types and Validation
====================

Flask-JSONRPC understands Python type hints and performs basic validation,
ensuring that parameters match the expected types.

----

Supported Types
---------------

Out of the box, these types are validated:

* ``int``
* ``float``
* ``str``
* ``bool``
* ``list`` and ``dict`` (validated recursively)
* ``Optional[T]``
* ``typing.List[T]``
* ``typing.Dict[Key, Value]``

Complex types (models, objects) require custom handling (see Patterns).

----

Return Type Validation
----------------------

Return types are validated, too:

.. code-block:: python

   @jsonrpc.method("math.average")
   def avg(nums: list[int]) -> float:
       return sum(nums) / len(nums)

If your method returns a value incompatible with the annotation, Flask-JSONRPC
raises a JSON-RPC error.

----

Custom Validation with jsonschema
---------------------------------

You may provide a JSON Schema manually:

.. code-block:: python

   @jsonrpc.method("user.create", schema={
       "type": "object",
       "properties": {
           "name": {"type": "string"},
           "age": {"type": "integer"},
       },
       "required": ["name"]
   })
   def create_user(name: str, age: int = None):
       ...

----

Using Pydantic (Optional Extension)
-----------------------------------

Pydantic models work well for strict typed JSON input:

.. code-block:: python

   from pydantic import BaseModel

   class User(BaseModel):
       name: str
       age: int | None = None

   @jsonrpc.method("user.create")
   def create(user: User) -> dict:
       return user.dict()
