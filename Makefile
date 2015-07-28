.PHONY: all clean test test-deps env env2

VIRTUALENV_EXISTS := $(shell [ -d .venv ] && echo 1 || echo 0)
VIRTUALENV2_EXISTS := $(shell [ -d .venv2 ] && echo 1 || echo 0)

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

env:
ifeq ($(VIRTUALENV_EXISTS), 0)
	@virtualenv --distribute --unzip-setuptools --no-site-packages .venv
	@.venv/bin/pip install --upgrade pip --quiet
	@.venv/bin/pip install --upgrade setuptools --quiet
	@.venv/bin/pip install -r requirements.pip
endif

env2:
ifeq ($(VIRTUALENV2_EXISTS), 0)
	@virtualenv2 --distribute --unzip-setuptools --no-site-packages .venv2
	@.venv2/bin/pip install --upgrade pip --quiet
	@.venv2/bin/pip install --upgrade setuptools --quiet
	@.venv2/bin/pip install -r requirements.pip
endif
