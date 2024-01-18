![Release Status](https://github.com/cenobites/flask-jsonrpc/actions/workflows/release.yml/badge.svg)
![Tests Status](https://github.com/cenobites/flask-jsonrpc/actions/workflows/tests.yml/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/cenobites/flask-jsonrpc/badge.svg?branch=master)](https://coveralls.io/github/cenobites/flask-jsonrpc?branch=master)
[![Documentation Status](https://readthedocs.org/projects/flask-jsonrpc/badge/?version=latest)](https://flask-jsonrpc.readthedocs.io/en/latest/?badge=latest)
# Flask JSON-RPC

Basic JSON-RPC implementation for your Flask-powered sites.

Some reasons you might want to use:

* Simple, powerful, flexible, and pythonic API.
* Support [JSON-RPC 2.0](https://www.jsonrpc.org/specification "JSON-RPC 2.0") version.
* Support Python 3.8 or later.
* The web browsable API.
* Run-time type checking functions defined with [PEP 484](https://www.python.org/dev/peps/pep-0484/ "PEP 484") argument (and return) type annotations.
* Extensive documentation, and great community support.

There is a live example API for testing purposes, [available here](http://flask-jsonrpc.herokuapp.com/api/browse "Web browsable API").

**Below:** *Screenshot from the browsable API*

![Web browsable API](https://f.cloud.github.com/assets/298350/1575590/203c595a-5150-11e3-99a0-4a6fd9bcbe52.png "Web browsable API")

### Adding Flask JSON-RPC to your application

1. Installation

```console
$ pip install Flask-JSONRPC
```

or

```console
$ git clone git://github.com/cenobites/flask-jsonrpc.git
$ cd flask-jsonrpc
$ python setup.py install
```


2. Getting Started

Create your application and initialize the Flask-JSONRPC.

```python
from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask("application")
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
```

Write JSON-RPC methods.

```python
@jsonrpc.method("App.index")
def index() -> str:
    return "Welcome to Flask JSON-RPC"
```

All code of example [run.py](https://github.com/cenobites/flask-jsonrpc/blob/master/run.py).


3. Running

```console
$ python run.py
 * Running on http://0.0.0.0:5000/
```

4. Testing

```console
$ curl -i -X POST \
   -H "Content-Type: application/json; indent=4" \
   -d '{
    "jsonrpc": "2.0",
    "method": "App.index",
    "params": {},
    "id": "1"
}' http://localhost:5000/api

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 77
Server: Werkzeug/0.8.3 Python/2.7.3
Date: Fri, 14 Dec 2012 19:26:56 GMT

{
  "jsonrpc": "2.0",
  "id": "1",
  "result": "Welcome to Flask JSON-RPC"
}
```


### References

* [http://docs.python.org/](http://docs.python.org/)
* [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* [http://www.jsonrpc.org/](http://www.jsonrpc.org/)
