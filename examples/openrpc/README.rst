petstore
=======

A petstore application.


Testing your service
********************

1. Running

::

    $ python petstore.py
     * Running on http://0.0.0.0:5000/

2. Testing

::
    $ curl 'http://localhost:5000/api' -X POST \
        --data-raw '{
            "jsonrpc": "2.0",
            "method": "Petstore.create_pet",
            "params": {
                "name": "Jhon",
                "tag": "cat"
            },
            "id": "1c7fb3b2-7a87-4cf7-8e28-aafc33dae71d"
        }'
    {
        "id": "1c7fb3b2-7a87-4cf7-8e28-aafc33dae71d",
        "jsonrpc": "2.0",
        "result": {
            "id": 32,
            "name": "Jhon",
            "tag": "cat"
        }
    }



::
    $ curl 'http://localhost:5000/api' -X POST \
        --data-raw '{
            "jsonrpc": "2.0",
            "method": "Petstore.get_pets",
            "params": {},
            "id": "16ebeed1-748c-4983-ba19-2848692c873a"
        }'
    {
        "id": "16ebeed1-748c-4983-ba19-2848692c873a",
        "jsonrpc": "2.0",
        "result": [
            {
            "id": 1,
            "name": "Bob",
            "tag": "dog"
            },
            {
            "id": 2,
            "name": "Eve",
            "tag": "cat"
            },
            {
            "id": 3,
            "name": "Alice",
            "tag": "bird"
            },
            {
            "id": 32,
            "name": "Jhon",
            "tag": "cat"
            }
        ]
    }



::
    $ curl 'http://localhost:5000/api' -X POST \
        --data-raw '{
            "jsonrpc": "2.0",
            "method": "Petstore.get_pet_by_id",
            "params": {
                "id": 32
            },
            "id": "5dfbd1c0-6919-4ce2-a05e-0b4a4aa2aeb2"
        }'
    {
        "id": "5dfbd1c0-6919-4ce2-a05e-0b4a4aa2aeb2",
        "jsonrpc": "2.0",
        "result": {
            "id": 32,
            "name": "Jhon",
            "tag": "cat"
        }
    }



::
    $ curl 'http://localhost:5000/api' -X POST -H 'Content-Type: application/json;charset=utf-8' \
        --data-raw '{
            "jsonrpc": "2.0",
            "method": "Petstore.delete_pet_by_id",
            "params": {
                "id": 32
            },
            "id": "706cf9c3-5b5d-4288-8555-a67c8b5de481"
        }'
    {
        "id": "706cf9c3-5b5d-4288-8555-a67c8b5de481",
        "jsonrpc": "2.0",
        "result": null
    }
