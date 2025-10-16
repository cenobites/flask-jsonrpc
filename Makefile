.PHONY: all clean style typing test test-release release env

VIRTUALENV_EXISTS := $(shell [ -d .venv ] && echo 1 || echo 0)

all: clean test
	@python -c "print('OK')"

clean:
	@find {src,examples,tests} -regex ".*\.\(so\|pyc\)" | xargs rm -rf
	@find {src,examples,tests} -name "__pycache__" -o -name ".coverage" -o -name "junit" -o -name "coverage.lcov" -o -name "htmlcov" -o -name ".tox"  -o -name ".pytest_cache" -o -name ".ruff_cache"  -o -name ".pkg" -o -name ".tmp" -o -name "*.so" | xargs rm -rf
	@rm -rf .coverage coverage.* .eggs/ .mypy_cache/ .pytype/ .ruff_cache/ .pytest_cache/ .tox/ src/*.egg-info/ htmlcov/ junit/ htmldoc/ build/ dist/ wheelhouse/ __pycache__/

style:
	@uv run ruff check .
	@uv run ruff format .

typing:
	@uv run mypy --install-types --non-interactive src/
	@uv run pyright

test: clean
	@uv run tox run

test-examples: clean
	@find examples/ -name "tox.ini" -print0 | xargs -0 -I {} -P 4 uv run tox run -e py,py-async -c {}

test-release: clean test
	$(shell ./bin/docker-compose-test.sh)
	$(shell ./bin/docker-compose-it.sh)

release: test
	@uv build
	@uv tool run twine check --strict dist/*

env:
ifeq ($(VIRTUALENV_EXISTS), 0)
	@uv venv --clear
endif
	@uv sync --locked
	@echo "To activate the virtualenv, run: source .venv/bin/activate"
