# cerberus params validator

## Setup

```
  $ python3 -m venv .venv
  $ . .venv/bin/activate
  $ pip install -r Flask cerberus
```

## Example 1

Simple example using Cerberus Validator inside the function explicitly.

### Run

```
  $ python example1.py
```

### Test

```
$ curl -i -X POST  -H "Content-Type: application/json; indent=4"       -d '{
        "jsonrpc": "2.0",
        "method": "App.createUsers",
        "params": {"user": {"name": "Foo", "age": 11}},
        "id": "1"
      }' http://localhost:5000/api
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.10.6
Date: Thu, 15 Sep 2022 14:14:45 GMT
Content-Type: application/json
Content-Length: 75
Connection: close

{
  "id": "1",
  "jsonrpc": "2.0",
  "result": {
    "created": true
  }
}
```

```
$ curl -i -X POST  -H "Content-Type: application/json; indent=4"       -d '{
        "jsonrpc": "2.0",
        "method": "App.createUsers",
        "params": {"user": {"name": "Foo", "age": 9}},
        "id": "1"
      }' http://localhost:5000/api
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/2.2.2 Python/3.10.6
Date: Thu, 15 Sep 2022 14:21:53 GMT
Content-Type: application/json
Content-Length: 1187
Connection: close

{
  "error": {
    "code": -32602,
    "data": {
      "message": {
        "user": [
          {
            "age": [
              "min value is 10"
            ]
          }
        ]
      }
    },
    "message": "Invalid params",
    "name": "InvalidParamsError"
  },
  "id": "1",
  "jsonrpc": "2.0"
}
```


## Example 2

Example using Cerberus Custom Validator to validate from the Python's Dataclasses type inside the function explicitly.

### Run

```
  $ python example2.py
```

### Test

```
$ curl -i -X POST  -H "Content-Type: application/json; indent=4"       -d '{
        "jsonrpc": "2.0",
        "method": "App.createUsers",
        "params": {"user": {"name": "Foo", "age": 11}},
        "id": "1"
      }' http://localhost:5000/api
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.10.6
Date: Thu, 15 Sep 2022 14:14:45 GMT
Content-Type: application/json
Content-Length: 75
Connection: close

{
  "id": "1",
  "jsonrpc": "2.0",
  "result": {
    "created": true
  }
}
```

```
$ curl -i -X POST  -H "Content-Type: application/json; indent=4"       -d '{
        "jsonrpc": "2.0",
        "method": "App.createUsers",
        "params": {"user": {"name": "Foo", "age": 9}},
        "id": "1"
      }' http://localhost:5000/api
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/2.2.2 Python/3.10.6
Date: Thu, 15 Sep 2022 14:21:53 GMT
Content-Type: application/json
Content-Length: 1187
Connection: close

{
  "error": {
    "code": -32602,
    "data": {
      "message": {
        "user": [
          {
            "age": [
              "min value is 10"
            ]
          }
        ]
      }
    },
    "message": "Invalid params",
    "name": "InvalidParamsError"
  },
  "id": "1",
  "jsonrpc": "2.0"
}
```


## Example 3

Example using Cerberus Custom Validator to validate by Python Decorator.

### Run

```
  $ python example3.py
```

### Test

```
$ curl -i -X POST  -H "Content-Type: application/json; indent=4"       -d '{
        "jsonrpc": "2.0",
        "method": "App.createUsers",
        "params": {"user": {"name": "Foo", "age": 11}},
        "id": "1"
      }' http://localhost:5000/api
HTTP/1.1 200 OK
Server: Werkzeug/2.2.2 Python/3.10.6
Date: Thu, 15 Sep 2022 14:14:45 GMT
Content-Type: application/json
Content-Length: 75
Connection: close

{
  "id": "1",
  "jsonrpc": "2.0",
  "result": {
    "created": true
  }
}
```

```
$ curl -i -X POST  -H "Content-Type: application/json; indent=4"       -d '{
        "jsonrpc": "2.0",
        "method": "App.createUsers",
        "params": {"user": {"name": "Foo", "age": 9}},
        "id": "1"
      }' http://localhost:5000/api
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/2.2.2 Python/3.10.6
Date: Thu, 15 Sep 2022 14:21:53 GMT
Content-Type: application/json
Content-Length: 1187
Connection: close

{
  "error": {
    "code": -32602,
    "data": {
      "message": {
        "user": [
          {
            "age": [
              "min value is 10"
            ]
          }
        ]
      }
    },
    "message": "Invalid params",
    "name": "InvalidParamsError"
  },
  "id": "1",
  "jsonrpc": "2.0"
}
```
