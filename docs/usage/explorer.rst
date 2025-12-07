Explorer UI
===========

Flask-JSONRPC includes an optional web-based explorer that lists methods and
lets you invoke them interactively.

Enable it:

.. code-block:: python

   JSONRPC(app, "/api", enable_web_browsable_api=True)

Visit:

::

   /api/browse

----

Features
--------

* lists all registered methods
* groups methods by namespace
* shows docstrings and type signatures
* allows executing calls directly from the browser
* displays request and response JSON
* supports introspection methods

----

Disabling the Explorer
----------------------

Useful in production:

.. code-block:: python

   JSONRPC(app, "/api", enable_web_browsable_api=False)

----

Custom Explorer Pages (Advanced)
--------------------------------

You may override the template by placing a file named
``jsonrpc/explorer.html`` inside your template directory.

This allows:

* custom branding
* hiding sensitive methods
* adding authentication
