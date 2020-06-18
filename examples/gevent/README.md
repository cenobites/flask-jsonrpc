# gevent

### Setup

```
  $ python3 -m venv .venv
  $ . .venv/bin/activate
  $ pip install -r Flask gevent
```

### Run

```
  $ python run.py
```

### Test

```
  $ curl -i -X POST \
        -H "Content-Type: application/json; indent=4" \
        -d '{
         "jsonrpc": "2.0",
         "method": "App.index",
         "params": {},
         "id": "1"
     }' http://localhost:5000/api
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 64
Date: Wed, 17 Jun 2020 20:38:04 GMT

{"id":"1","jsonrpc":"2.0","result":"Welcome to Flask JSON-RPC"}
```
