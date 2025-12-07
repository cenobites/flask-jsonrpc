Testing Flask-JSONRPC Applications
==================================

Testing is critical for JSON-RPC services. Flask-JSONRPC integrates seamlessly
with Flask's built-in test client.

----

Using Flask's Test Client
-------------------------

.. code-block:: python

   import unittest
   from app import create_app

   class RPCAppTestCase(unittest.TestCase):
       def setUp(self):
           self.app = create_app()
           self.client = self.app.test_client()

       def rpc_call(self, method, params=None, id=1):
           data = {
               "jsonrpc": "2.0",
               "method": method,
               "id": id
           }
           if params is not None:
               data["params"] = params
           response = self.client.post("/api", json=data)
           return response.get_json()

       def test_ping(self):
           result = self.rpc_call("ping")
           self.assertEqual(result["result"], "pong")

       def test_add(self):
           result = self.rpc_call("math.add", [3, 4])
           self.assertEqual(result["result"], 7)

   if __name__ == "__main__":
       unittest.main()

----

Batch Requests Testing
----------------------

You can also test batch requests:

.. code-block:: python

   def test_batch(self):
       batch_data = [
           {"jsonrpc": "2.0", "method": "ping", "id": 1},
           {"jsonrpc": "2.0", "method": "math.add", "params": [1, 2], "id": 2}
       ]
       response = self.client.post("/api", json=batch_data)
       results = response.get_json()
       self.assertEqual(results[0]["result"], "pong")
       self.assertEqual(results[1]["result"], 3)

----

Mocking Dependencies
--------------------

Use standard Python mocking techniques to replace dependencies:

.. code-block:: python

   from unittest.mock import patch

   @patch("app.db_query")
   def test_user_query(mock_db):
       mock_db.return_value = {"name": "Alice"}
       result = rpc_call("user.get", {"id": 1})
       assert result["result"]["name"] == "Alice"
