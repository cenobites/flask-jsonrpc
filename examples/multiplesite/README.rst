multiplesite
============

Multiples sites in same application.


Testing your service
********************

1. Running

::

    $ python multiplesite.py
     * Running on http://0.0.0.0:5000/


2. Testing

::

    $ curl -i -X POST  -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.index",
        "id": "1"
      }' http://localhost:5000/api/v1
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 92
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 13:15:44 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to Flask JSON-RPC Version API 1"
    }


::

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.index",
        "id": "1"
      }' http://localhost:5000/api/v2
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 92
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 13:15:59 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to Flask JSON-RPC Version API 2"
    }
