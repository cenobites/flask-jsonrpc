.PHONY: all clean style typing test test-dev test-cov-unit test-examples test-release release env uv-lock

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
	@uv run mypy --install-types --non-interactive run.py src/
	@uv run pyright

test: clean
	@uv run tox run

test-dev:
	@pytest --numprocesses=0 --count=1 --reruns=0 --parallel-threads=0 --iterations=0 --random-order-seed=1 -x

test-cov-unit:
	@REPORT="\nUnit Tests:\n"; \
	ALLOW_ASYNC=$$(python3 -c "import importlib.util; print(1 if importlib.util.find_spec('asgiref') else 0)"); \
	for TEST_FILE in $(shell find tests/unit -name "test_*.py"); do \
        TEST_NAME=$$(basename $${TEST_FILE} .py); \
        PY_MODULE=$$(echo flask_jsonrpc.$${TEST_FILE} | sed 's|/|.|g' | sed 's|.py$$||' | sed 's|test_||' | sed 's|tests.unit.||' | sed 's|.openrpc.app|.openrpc|' | sed 's|.browse.app|.browse|' | sed 's|.async_app|.app|'); \
		if [ $${ALLOW_ASYNC} -eq 0 ] && [[ $${TEST_FILE} == *"async"* ]]; then \
			continue; \
		fi; \
        pytest --count 1 -n 0 --cov-reset --cov=$${PY_MODULE} $${TEST_FILE} -vv; \
        if [ $$? -ne 0 ]; then \
            REPORT+=" + Unit Tests $${TEST_FILE} for $${PY_MODULE} failed (pytest --cov-reset --cov-report=html --cov=$${PY_MODULE} $${TEST_FILE} -vv)\n"; \
		else \
			REPORT+=" + Unit Tests $${TEST_FILE} for $${PY_MODULE} passed\n"; \
        fi; \
    done; \
	echo $${REPORT}


test-examples: clean
	@find examples/ -name "pyproject.toml" -print0 | xargs -0 -I {} -P 4 uv run tox run -e py,py-async -c {}

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

uv-lock:
	@uv lock -U
	@for dir in examples/*/; do \
		echo "Updating lock file for $$dir"; \
		uv lock -U --directory "$$dir"; \
	done
