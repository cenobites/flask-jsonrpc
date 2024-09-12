#!/bin/bash
set -e

python3 -m venv --upgrade-deps .venv
. .venv/bin/activate
pip install -r requirements/local.txt
pip install -e .
pre-commit install --install-hooks
