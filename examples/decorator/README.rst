decorator
=========

The basic method decorated dealing any extra parameter and do some thing.


Testing your service
********************

1. Running

::

    $ python decorator.py
     * Running on http://0.0.0.0:5000/


2. Testing

::

    $ curl -i -X POST  -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.index",
        "params": {},
        "id": "1",
        "terminal_id": 1
      }' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 67
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:31:50 GMT

    {
      "id": "1",
      "jsonrpc": "2.0",
      "result": "Terminal ID: 1"
    }


::

    $ curl -i -X POST -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.index",
        "params": {},
        "id": "1",
        "terminal_id": 0
      }' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 750
    Server: Werkzeug/0.8.3 Python/2.7.7
    Date: Mon, 07 Jul 2014 12:36:48 GMT

    {
      "error": {
          "code": -32000,
          "data": {
          "message": "Invalid terminal ID"
          },
          "executable": "/home/nycholas/project/cenobit.es/src/flask-jsonrpc/.venv/bin/python",
          "message": "Server error",
          "name": "ServerError",
          "stack": "Traceback (most recent call last):\n  File \"/home/nycholas/project/cenobit.es/src/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 88, in dispatch_request\n    return self.dispatch(json_data)\n  File \"/home/nycholas/project/cenobit.es/src/flask-jsonrpc/examples/../flask_jsonrpc/site.py\", line 138, in dispatch\n    resp_view = view_func(**params)\n  File \"/home/nycholas/project/cenobit.es/src/flask-jsonrpc/.venv/lib/python3.8/site-packages/typeguard/__init__.py\", line 840, in wrapper\n    retval = func(*args, **kwargs)\n  File \"/home/nycholas/project/cenobit.es/src/flask-jsonrpc/examples/decorator/decorator.py\", line 52, in wrapped\n    raise ValueError('Invalid terminal ID')\nValueError: Invalid terminal ID\n"
      },
      "id": "1",
      "jsonrpc": "2.0"
    }



::
    $ curl -i -X POST  -H "Content-Type: application/json; indent=4" \
      -d '{
        "jsonrpc": "2.0",
        "method": "App.decorators",
        "params": {},
        "id": "1",
        "terminal_id": 1
      }' http://localhost:5000/api
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 231
    X-JSONRPC-Tag: JSONRPC 2.0
    Server: Werkzeug/0.10.4 Python/3.4.3
    Date: Sun, 09 Aug 2015 17:00:16 GMT

    {
        "id": "1",
        "jsonrpc": "2.0",
        "result": {
            "headers": "Host: localhost:5000\r\nUser-Agent: curl/7.70.0\r\nAccept: */*\r\nContent-Type: application/json; indent=4\r\nContent-Length: 137\r\n\r\n",
            "terminal_id": 1
        }
    }
