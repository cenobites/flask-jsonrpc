modular
=======

A modular application with BluePrints.


Testing your service
********************

1. Running

::

    $ python modular.py
     * Running on http://0.0.0.0:5000/


2. Testing

::

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "Article.index",
        "id": "1"
      }' http://localhost:5000/api/article
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 75
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 13:14:00 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to Article API"
    }


::

    $ curl -i -X POST  -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "User.index",
        "id": "1"
      }' http://localhost:5000/api/user
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 72
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 13:14:17 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to User API"
    }
