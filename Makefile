.PHONY: all clean test test-release release publish-test publish env

VIRTUALENV_EXISTS := $(shell [ -d .venv ] && echo 1 || echo 0)

all: clean test
	@python -c "print('OK')"

clean:
	@python setup.py clean
	@find src/ -name "*.so" | xargs rm -rf
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name ".coverage" | xargs rm -rf
	@rm -rf .coverage coverage.* .eggs/ .mypy_cache/ .pytype/ .ruff_cache/ .pytest_cache/ .tox/ src/Flask_JSONRPC.egg-info/ htmlcov/ junit/ htmldoc/ build/ dist/ wheelhouse/

test: clean
	@python -m pip install --upgrade tox
	@python -m tox

test-release: clean test
	@docker-compose -f docker-compose.test.yml build --build-arg VERSION=$(shell date +%s)
	@docker-compose -f docker-compose.test.yml up

release: clean test
	@python -m pip install --upgrade -r requirements/cbuild.txt
	@python -m build
	@MYPYC_ENABLE=1 python setup.py bdist_wheel

publish-test: clean release
	@python -m pip install --upgrade twine
	@python -m twine upload --repository testpypi dist/*

publish: clean release
	@python -m pip install --upgrade twine
	@python -m twine upload dist/*

env:
ifeq ($(VIRTUALENV_EXISTS), 0)
	@python -m venv --upgrade-deps .venv
	@.venv/bin/pip install -r requirements/local.txt
endif
