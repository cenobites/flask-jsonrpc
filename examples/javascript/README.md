# javascript

A minimal application with HRX (Ajax).

## Install

```
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -e .
```

## Run

```
$ flask --app src/hrx/app.py run
```

Open http://127.0.0.1:5000 in a browser.


## Test

```
$ pip install -e '.[test]'
$ pytest
```
