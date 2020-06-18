hrx
===

A minimal application with HRX (Ajax).


Testing your service
********************

1. Running

::

    $ python hrx.py
     * Running on http://0.0.0.0:5000/


2. Testing

::

    $ curl -i -X POST  -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "Hello.index",
        "id": "1"
      }' http://localhost:5000/api/hello
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 74
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 13:03:23 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to Hello API!"
    }
