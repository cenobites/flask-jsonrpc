#!/bin/bash
set -eux

DOCKER_TARGET_BUILD=${1:-app}
PYTHON_VERSION=${2:-3.13}
DOCKER_COMPOSE_FILE_NAME=compose.yml
DOCKER_COMPOSE_FILE_PATH=../${DOCKER_COMPOSE_FILE_NAME}
[ -f ${DOCKER_COMPOSE_FILE_PATH} ] || DOCKER_COMPOSE_FILE_PATH=${DOCKER_COMPOSE_FILE_NAME}

if [ "${DOCKER_TARGET_BUILD}" = "app" ]; then
    SUT_TARGET="sut"
    APP_TARGET="app"
    NGINX_TARGET="nginx"
elif [ "${DOCKER_TARGET_BUILD}" = "async" ]; then
    SUT_TARGET="async-sut"
    APP_TARGET="async-app"
    NGINX_TARGET="async-nginx"
elif [ "${DOCKER_TARGET_BUILD}" = "mypyc" ]; then
    SUT_TARGET="mypyc-sut"
    APP_TARGET="mypyc-app"
    NGINX_TARGET="mypyc-nginx"
else
    echo "Unknown target build: ${DOCKER_TARGET_BUILD}"
    exit 1
fi

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it build --build-arg PYTHON_DOCKER_IMAGE_TAG=${PYTHON_VERSION}-slim --build-arg VERSION=$(date +%s) ${SUT_TARGET}
docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it build --build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg VERSION=$(date +%s) ${APP_TARGET}
docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it up ${SUT_TARGET} ${APP_TARGET} ${NGINX_TARGET} --abort-on-container-exit

DOCKER_WAIT_FOR_SUT=$?

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it logs ${SUT_TARGET}
docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it down --remove-orphans

if [ ${DOCKER_WAIT_FOR_SUT} -ne 0 ]; then
    echo "Integration Tests for Python ${PYTHON_VERSION} to ${DOCKER_TARGET_BUILD} failed"
    exit 1
fi
echo "Integration Tests for Python ${PYTHON_VERSION} to ${DOCKER_TARGET_BUILD} passed"
