# minimal-async

A minimal async application.

## Install

```
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -e .
```

## Run

```
$ flask --app src/minimal_async/app.py run
```

Open http://127.0.0.1:5000 in a browser.


## Test

```
$ pip install -e '.[test]'
$ pytest
```
