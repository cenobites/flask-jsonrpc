ARG PYTHON_VERSION="3.13"
ARG PYTHON_DOCKER_IMAGE_TAG="${PYTHON_VERSION}-alpine"
ARG DOCKER_BASE_IMAGE="python:${PYTHON_DOCKER_IMAGE_TAG}"


FROM ${DOCKER_BASE_IMAGE} AS baseimage

ENV TZ="UTC"
ENV USERNAME="kuchulu"
ENV UID="1666"
ENV GROUPNAME="kuchulu"
ENV GID="1666"
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0
ENV HOME_DIR="/home/${USERNAME}"
ENV WHEEL_PACK_DIR="${HOME_DIR}/wheels"
ENV APP_DIR="/app"
ENV PYTHON_VENV_DIR="${APP_DIR}/.venv"
ENV PYTHON_EXEC="${PYTHON_VENV_DIR}/bin/python"

COPY .docker/cleanup.sh /usr/sbin/cleanup.sh
RUN chmod +x /usr/sbin/cleanup.sh \
    && /usr/sbin/cleanup.sh ${USERNAME} ${UID} ${GROUPNAME} ${GID}


FROM baseimage AS builder

ARG DOCKER_BUILD_TARGET=""

RUN set -eux \
    && if command -v apk >/dev/null 2>&1; then \
        apk add --no-cache --update --virtual .build-deps \
            build-base \
            linux-headers \
            ca-certificates \
            gcc \
            musl-dev \
            python3-dev \
            uv \
            git; \
        rm -rf /var/cache/*; \
        mkdir /var/cache/apk; \
        ln -sf /lib/ld-musl-x86_64.so.1 /usr/bin/ldd; \
        ln -s /lib /lib64; \
    elif command -v apt-get >/dev/null 2>&1; then \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            build-essential \
            linux-headers-generic \
            ca-certificates \
            gcc \
            python3-dev \
            curl \
            git; \
        curl -LsSf https://astral.sh/uv/install.sh | sh; \
        cp -rf /root/.local/bin/* /usr/local/bin; \
        rm -rf /var/lib/apt/lists/*; \
    fi

WORKDIR ${APP_DIR}
COPY uv.lock pyproject.toml LICENSE.txt README.md ${APP_DIR}/

RUN set -eux \
    && uv venv --clear \
    && if [ "$DOCKER_BUILD_TARGET" = "" ]; then \
        uv sync --locked --no-dev --no-install-project --no-default-groups; \
    elif [ "$DOCKER_BUILD_TARGET" = "app" ]; then \
        uv sync --locked --no-dev --no-default-groups --extra async; \
    elif [ "$DOCKER_BUILD_TARGET" = "unit-tests" ]; then \
        uv sync --locked --no-dev --no-install-project --no-default-groups --group tests --extra async; \
    elif [ "$DOCKER_BUILD_TARGET" = "integration-tests" ]; then \
        uv sync --locked --no-dev --no-install-project --no-default-groups --group integration-tests --extra async; \
    fi;

ARG VERSION=1
RUN echo "Version: ${VERSION}"
COPY . ${APP_DIR}/

RUN set -eux \
    && if [ "$DOCKER_BUILD_TARGET" = "app" ]; then \
        uv build --wheel --out-dir ${WHEEL_PACK_DIR}; \
        uv pip install ${WHEEL_PACK_DIR}/*.whl; \
    elif [ "$DOCKER_BUILD_TARGET" = "mypyc-app" ]; then \
        uv sync --locked --no-dev --no-default-groups --group cbuild; \
        SETUPTOOLS_BUILD_ENABLE_MYPYC=1 uv run setup.py bdist_wheel --dist-dir ${WHEEL_PACK_DIR}; \
        # TODO: Uncomment the following line to use hatch instead of setup.py
        # HATCH_BUILD_HOOK_ENABLE_MYPYC=1 uv build --wheel --out-dir ${WHEEL_PACK_DIR}; \
        uv pip install ${WHEEL_PACK_DIR}/*.whl; \
    fi \
    && if command -v apk >/dev/null 2>&1; then \
        apk del .build-deps; \
    elif command -v apt-get >/dev/null 2>&1; then \
        apt-get remove --purge -y; \
    fi \
    && /usr/sbin/cleanup.sh ${USERNAME} ${UID} ${GROUPNAME} ${GID}

USER ${USERNAME}
WORKDIR ${HOME_DIR}


FROM baseimage AS app
COPY --from=builder --chown=${USERNAME}:${GROUPNAME} ${APP_DIR} ${APP_DIR}
ENV PATH="${PYTHON_VENV_DIR}/bin:${PATH}"
COPY --chown=${USERNAME}:${GROUPNAME} .docker/* tests/test_apps/ ${APP_DIR}/run/
WORKDIR ${APP_DIR}/run


FROM baseimage AS unit-tests
COPY --from=builder --chown=${USERNAME}:${GROUPNAME} ${APP_DIR} ${APP_DIR}
ENV CI=1 \
    PRAGMA_VERSION=py3.13 \
    PATH="${PYTHON_VENV_DIR}/bin:${PATH}"
WORKDIR ${APP_DIR}


FROM baseimage AS integration-tests
COPY --from=builder --chown=${USERNAME}:${GROUPNAME} ${APP_DIR} ${APP_DIR}
ENV CI=1 \
    PYTEST_CACHE_DIR=".pytest_cache" \
    SITE_DOMAIN="app" \
    SITE_PORT=5000 \
    WEB_URL="http://app:5000" \
    API_URL="http://app:5000/api" \
    BROWSABLE_API_URL="http://app:5000/api/browse" \
    PATH="${PYTHON_VENV_DIR}/bin:${PATH}"
USER root
ADD .docker/certs/Cenobit_Root_CA.pem /usr/local/share/ca-certificates/Cenobit_Root_CA.pem
RUN set -eux \
    && if command -v apk >/dev/null 2>&1; then \
        apk add --no-cache --update \
            bash \
            git \
            ca-certificates \
            openssl \
            nodejs \
            npm; \
        rm -rf /var/cache/apk/*; \
        mkdir /var/cache/apk; \
        ln -sf /lib/ld-musl-x86_64.so.1 /usr/bin/ldd; \
        ln -sf /lib /lib64; \
    elif command -v apt-get >/dev/null 2>&1; then \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            git \
            ca-certificates \
            openssl \
            nodejs \
            npm; \
        rm -rf /var/lib/apt/lists/*; \
    fi \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && openssl x509 -inform PEM -in /usr/local/share/ca-certificates/Cenobit_Root_CA.pem -out /usr/local/share/ca-certificates/Cenobit_Root_CA.crt \
    && chmod 644 /usr/local/share/ca-certificates/Cenobit_Root_CA.crt \
    && update-ca-certificates \
    && npx playwright install --with-deps chromium \
    && playwright install chromium \
    && /usr/sbin/cleanup.sh ${USERNAME} ${UID} ${GROUPNAME} ${GID}
USER ${USERNAME}
WORKDIR ${APP_DIR}/run
COPY --chown=${USERNAME}:${GROUPNAME} .docker/* tests/integration/*.py tests/integration/*.ini ${APP_DIR}/run/
COPY --chown=${USERNAME}:${GROUPNAME} tests/integration/shared/*.py tests/shared/ ${APP_DIR}/run/shared/
CMD ["bash", "-c", "./wait-for-it.sh ${SITE_DOMAIN}:${SITE_PORT} -t 600 -- py.test -n auto -vv --tb=short --junitxml=test-results/junit.xml"]


FROM baseimage
COPY --from=builder --chown=${USERNAME}:${GROUPNAME} ${APP_DIR} ${APP_DIR}
ENV PATH="${PYTHON_VENV_DIR}/bin:${PATH}"
CMD ["flask", "--app", "/app/run", "run"]
