Flask JSON-RPC
==============

A basic JSON-RPC implementation for your Flask-powered sites based on `django-json-rpc <https://github.com/samuraisam/django-json-rpc>`_.


Running
*******

::
    
    $ pip install Flask
    $ python run_test.py
     * Running on http://0.0.0.0:5000/
     

Testing
*******

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


Dependecies
***********

* Python 2.7 or later (http://www.python.org)
* Flask 0.9 or later (http://www.djangoproject.org)


Project Information
*******************

:Author: Cenobit Technologies, Inc.
:Version: v0.0.1 of 2012/12/14
:License: `New BSD License <http://opensource.org/licenses/BSD-3-Clause>`_
