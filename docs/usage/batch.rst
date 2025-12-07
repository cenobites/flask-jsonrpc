Batch Requests
==============

The JSON-RPC 2.0 specification allows clients to send multiple method calls in a
single request. Flask-JSONRPC supports this fully.

----

Example Batch Request
---------------------

Request:

.. code-block:: json

   [
     {"jsonrpc": "2.0", "method": "ping", "id": 1},
     {"jsonrpc": "2.0", "method": "math.add", "params": [2, 3], "id": 2}
   ]

Response:

.. code-block:: json

   [
     {"jsonrpc": "2.0", "result": "pong", "id": 1},
     {"jsonrpc": "2.0", "result": 5, "id": 2}
   ]

----

Notifications in Batch
----------------------

A "notification" has no ID and produces no response:

.. code-block:: json

   {"jsonrpc": "2.0", "method": "log.write", "params": ["hello"]}

Batch requests may mix notifications and regular calls.
