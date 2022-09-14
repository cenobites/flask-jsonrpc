.PHONY: all clean test test-release release publish-test publish env

VIRTUALENV_EXISTS := $(shell [ -d .venv ] && echo 1 || echo 0)

all: clean test
	@python -c "print('OK')"

clean:
	@python setup.py clean
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name ".coverage" | xargs rm -rf
	@rm -rf .coverage .eggs/ .mypy_cache/ .pytest_cache/ .tox/ src/Flask_JSONRPC.egg-info/ htmlcov/ junit/ htmldoc/ build/ dist/

test: clean
	@python -m tox

test-release: clean test
	@docker-compose -f docker-compose.test.yml build --build-arg VERSION=$(shell date +%s)
	@docker-compose -f docker-compose.test.yml up

release: clean test
	@python -m pip install --upgrade build
	@python -m build

publish-test: clean release
	@python -m pip install --upgrade twine
	@python -m twine upload --repository testpypi dist/*

publish: clean release
	@python -m pip install --upgrade twine
	@python -m twine upload dist/*

env:
ifeq ($(VIRTUALENV_EXISTS), 0)
	@python -m venv .venv
	@.venv/bin/pip install --upgrade pip setuptools
	@.venv/bin/pip install -r requirements/local.txt
endif
