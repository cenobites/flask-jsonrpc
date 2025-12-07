Deployment
==========

This section covers deploying Flask-JSONRPC services in production environments.

----

WSGI Servers
------------

Use a WSGI server such as Gunicorn or uWSGI:

.. code-block:: bash

   # Using Gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:create_app()

.. note::

   Replace ``app:create_app()`` with your factory function if using app factories.

----

Reverse Proxy (Nginx Example)
-----------------------------

Example configuration for Nginx forwarding to Gunicorn:

.. code-block:: nginx

   server {
       listen 80;
       server_name example.com;

       location /api {
           proxy_pass http://127.0.0.1:8000/api;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }

----

HTTPS and Security
------------------

* Always enable HTTPS in production.
* Protect sensitive methods with authentication (see :doc:`patterns/auth`).
* Disable the web explorer in public environments:

.. code-block:: python

   JSONRPC(app, "/api", enable_web_browsable_api=False)

----

Scaling and Multiple Instances
------------------------------

Use standard Flask/WSGI scaling:

* Multiple Gunicorn workers
* Load balancer in front (NGINX, HAProxy)
* Optional horizontal scaling across servers

Flask-JSONRPC methods remain stateless by default. Ensure shared state (like
databases) is properly configured.
