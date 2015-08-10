minimal
=======

A minimal application.


Testing your service
********************

1. Running

::

    $ python minimal.py
     * Running on http://0.0.0.0:5000/


2. Testing

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
    Content-Length: 78
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:40:08 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to Flask JSON-RPC"
    }


::

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.hello",
        "params": ["Flask"],
        "id": "1"
      }' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 64
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:41:08 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Hello Flask"
    }


::

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.notify"
      }' http://localhost:5000/api
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:41:49 GMT


::

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.fails",
        "params": ["Flask"],
        "id": "1"
      }' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 704
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:42:40 GMT

    {
      "error": {
        "code": 500,
        "data": null,
        "executable": "/usr/bin/python2",
        "message": "OtherError: ",
        "name": "OtherError",
        "stack": "Traceback (most recent call last):\n  File \"/home/nycholas/project/src/o_lalertom/flask/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 208, in response_dict\n    R = apply_version[version](method, D['params'])\n  File \"/home/nycholas/project/src/o_lalertom/flask/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 168, in <lambda>\n    '2.0': lambda f, p: f(**encode_kw(p)) if type(p) is dict else f(*p),\n  File \"minimal.py\", line 78, in fails\n    raise ValueError\nValueError\n"
      },
      "id": "1",
      "jsonrpc": "2.0"
    }
