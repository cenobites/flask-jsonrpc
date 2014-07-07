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

    $ curl -i -X POST  -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "App.index", "params": {"username": "flask", "password": "JSON-RPC"}, "id": "1"}' http://localhost:5000/api
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

    $ curl -i -X POST  -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "App.index", "params": {}, "id": "1"}' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 502
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:50:14 GMT

    {
      "error": {
        "code": -32600,
        "data": null,
        "executable": "/usr/bin/python2",
        "message": "InvalidRequestError: Expecting ':' delimiter: line 1 column 59 (char 58)",
        "name": "InvalidRequestError",
        "stack": "Traceback (most recent call last):\n  File \"/home/nycholas/project/src/o_lalertom/flask/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 281, in dispatch\n    raise InvalidRequestError(e.message)\nInvalidRequestError\n"
      },
      "id": "1",
      "result": null
    }


::

    $ curl -i -X POST  -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "App.echo", "params": {"usernme": "flask", "password": "JSON-RPC", "name": "Flask"}, "id": "1"}' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 64
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:51:15 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Hello Flask"
    }


::

    $ curl -i -X POST  -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "App.echo", "params": {"username": "flask", "password": "JSON-RPC"}, "id": "1"}' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 680
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:50:38 GMT

    {
      "error": {
        "code": -32602,
        "data": null,
        "executable": "/usr/bin/python2",
        "message": "InvalidParamsError: Not eough params provided for App.echo(String, String, name=str) -> str",
        "name": "InvalidParamsError",
        "stack": "Traceback (most recent call last):\n  File \"/home/nycholas/project/src/o_lalertom/flask/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 197, in response_dict\n    validate_params(method, D)\n  File \"/home/nycholas/project/src/o_lalertom/flask/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 95, in validate_params\n    .format(method.json_sig))\nInvalidParamsError\n"
      },
      "id": "1",
      "jsonrpc": "2.0"
    }
