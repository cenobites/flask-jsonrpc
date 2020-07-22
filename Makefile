.PHONY: all clean test release publish-test publish env

VIRTUALENV_EXISTS := $(shell [ -d .venv ] && echo 1 || echo 0)

all: clean test
	@python setup.py build

clean:
	@python setup.py clean
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name ".coverage" | xargs rm -rf
	@rm -rf .coverage .eggs/ .mypy_cache/ .pytest_cache/ Flask_JSONRPC.egg-info/ htmlcov/ build/ dist/

test: clean
	@python setup.py test

release: clean
	@python setup.py build sdist bdist_wheel

publish-test: clean release
	@twine upload --repository testpypi dist/*

publish: clean release
	@twine upload dist/*

env:
ifeq ($(VIRTUALENV_EXISTS), 0)
	@python -m venv .venv
	@.venv/bin/pip install --upgrade pip setuptools
	@.venv/bin/pip install -r requirements.pip
endif
