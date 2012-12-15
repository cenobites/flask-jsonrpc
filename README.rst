Flask JSON-RPC
==============

A basic JSON-RPC implementation for your Flask-powered sites based on `django-json-rpc <https://github.com/samuraisam/django-json-rpc>`_.

Adding Flask JSON-RPC to your application
*****************************************

1. Installation

::

    $ pip install Flask-JSONRPC

or

::

    $ git clone git://github.com/cenobites/flask-jsonrpc.git
    $ cd flask-jsonrpc
    $ python setup.py install


2. Getting Started

Create your application and initialize the Flask-JSONRPC.

::

    from flask import Flask
    from flask_jsonrpc import JSONRPC

    app = Flask(__name__)
    jsonrpc = JSONRPC(app, '/api')

Write JSON-RPC methods.

::

    @jsonrpc.method('App.index')
    def index():
        return 'Welcome to Flask JSON-RPC'

All code of Example `run.py <https://github.com/cenobites/flask-jsonrpc/blob/master/run.py>`_.


3. Running

::
    
    $ python run.py
     * Running on http://0.0.0.0:5000/
     

4. Testing

::

    $ curl -i -X POST -d '{"jsonrpc": "2.0", "method": "App.index", "params": {}, "id": "1"}' http://localhost:5000/api
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


Testing your service
********************

::

    >>> from flask_jsonrpc.proxy import ServiceProxy
    >>> server = ServiceProxy('http://localhost:5000/api')
    >>>
    >>> server.App.index()
    {'jsonrpc': '2.0', 'id': '91bce374-462f-11e2-af55-f0bf97588c3b', 'result': 'Welcome to Flask JSON-RPC'}


Dependecies
***********

* Python 2.7 or later (http://www.python.org)
* Flask 0.9 or later (http://flask.pocoo.org)


Project Information
*******************

:Author: Cenobit Technologies, Inc.
:Version: v0.0.1 of 2012/12/14
:License: `New BSD License <http://opensource.org/licenses/BSD-3-Clause>`_
