auth
====

A basic method authenticator.


Testing your service
********************

1. Running

::

    $ python auth.py
     * Running on http://0.0.0.0:5000/


2. Testing

::

    $ curl -i -X POST -H "Content-Type: application/json" \
      -H 'X-Username: username' \
      -H 'X-Password: secret' \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.index",
        "id": "1"
      }' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 78
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:49:37 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to Flask JSON-RPC"
    }


::

    $ curl -i -X POST  -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.index",
        "params": {},
        "id": "1"
      }' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 502
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:50:14 GMT

    UnauthorizedError
