authbackend
===========

A backend method authenticator.


Testing your service
********************

1. Running

::

    $ python authbackend.py
     * Running on http://0.0.0.0:5000/


2. Testing

::

    $ curl -i -X POST  -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "App.index", "params": {"username": "flask", "password": "JSON-RPC"}, "id": "1"}' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 78
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:53:01 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Welcome to Flask JSON-RPC"
    }


::

    $ curl -i -X POST  -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "App.index", "params": {"username": "flask"}, "id": "1"}' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 850
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 13:00:57 GMT

    {
      "error": {
        "code": 500,
        "data": null,
        "executable": "/usr/bin/python2",
        "message": "OtherError: global name 'InvalidParamsError' is not defined",
        "name": "OtherError",
        "stack": "Traceback (most recent call last):\n  File \"/home/nycholas/project/src/o_lalertom/flask/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 208, in response_dict\n    R = apply_version[version](method, D['params'])\n  File \"/home/nycholas/project/src/o_lalertom/flask/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 168, in <lambda>\n    '2.0': lambda f, p: f(**encode_kw(p)) if type(p) is dict else f(*p),\n  File \"authbackend.py\", line 64, in _f\n    raise InvalidParamsError('Authenticated methods require at least '\nNameError: global name 'InvalidParamsError' is not defined\n"
      },
      "id": "1",
      "jsonrpc": "2.0"
    }
