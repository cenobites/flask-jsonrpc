.PHONY: all clean test test-deps env26

VIRTUALENV26_EXISTS := $(shell [ -d .venv26 ] && echo 1 || echo 0)

all: clean test
	@python setup.py build

clean:
	@python setup.py clean
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "__pycache__" | xargs rm -rf
	@rm -rf .coverage Flask_JSONRPC.egg-info/ htmlcov/ build/

test: clean test-deps
	@python setup.py test

test-deps:
	@pip install -r requirements_test.pip

env26:
ifeq ($(VIRTUALENV26_EXISTS), 0)
	@virtualenv2.6 --distribute --unzip-setuptools --no-site-packages .venv26
	@.venv26/bin/pip install --upgrade pip --quiet
	@.venv26/bin/pip install --upgrade setuptools --quiet
	@.venv26/bin/pip install -r requirements.pip
endif
