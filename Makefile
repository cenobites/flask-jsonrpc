.PHONY: all clean style typing test test-release release publish-test publish env

VIRTUALENV_EXISTS := $(shell [ -d .venv ] && echo 1 || echo 0)

all: clean test
	@python -c "print('OK')"

clean:
	@find {src,examples,tests} -regex ".*\.\(so\|pyc\)" | xargs rm -rf
	@find {src,examples,tests} -name "__pycache__" -o -name ".coverage" -o -name "junit" -o -name "coverage.lcov" -o -name "htmlcov" -o -name ".tox"  -o -name ".pytest_cache" -o -name ".ruff_cache"  -o -name ".pkg" -o -name ".tmp" | xargs rm -rf
	@rm -rf .coverage coverage.* .eggs/ .mypy_cache/ .pytype/ .ruff_cache/ .pytest_cache/ .tox/ src/*.egg-info/ htmlcov/ junit/ htmldoc/ build/ dist/ wheelhouse/

style:
	@ruff check .
	@ruff format .

typing:
	@mypy --install-types --non-interactive src/

test: clean
	@python -m pip install --upgrade tox
	@python -m tox -p all

test-examples: clean
	@python -m pip install --upgrade tox
	@find examples/ -name "tox.ini" -print0 | xargs -0 -t -I % -P 4 tox -p all -c %

test-release: test
	$(shell ./bin/docker-compose-test.sh)
	$(shell ./bin/docker-compose-it.sh)

release: test
	@python -m pip install --upgrade -r requirements/cbuild.txt
	@python -m build
	@MYPYC_ENABLE=1 python setup.py bdist_wheel
	@cibuildwheel

publish-test: release
	@python -m pip install --upgrade twine
	@python -m twine upload --repository testpypi dist/*

publish: release
	@python -m pip install --upgrade twine
	@python -m twine upload dist/*

env:
ifeq ($(VIRTUALENV_EXISTS), 0)
	@python -m venv --upgrade-deps .venv
	@.venv/bin/pip install -r requirements/local.txt
endif
