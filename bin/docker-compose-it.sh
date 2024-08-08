#!/bin/bash

DOCKER_COMPOSE_FILE_NAME=docker-compose.it.yml
DOCKER_COMPOSE_FILE_PATH=../${DOCKER_COMPOSE_FILE_NAME}
[ -f ${DOCKER_COMPOSE_FILE_PATH} ] || DOCKER_COMPOSE_FILE_PATH=${DOCKER_COMPOSE_FILE_NAME}

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it build --build-arg VERSION=$(date +%s)
docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it up -d

(
    set -e
    docker wait ci-it-sut-1
    docker logs ci-it-sut-1
)
DOCKER_WAIT_FOR_SUT=$?

(
    set -e
    docker wait ci-it-async-sut-1
    docker logs ci-it-async-sut-1
)
DOCKER_WAIT_FOR_ASYNC_SUT=$?

(
    set -e
    docker wait ci-it-mypyc-sut-1
    docker logs ci-it-mypyc-sut-1
)
DOCKER_WAIT_FOR_MYPYC_SUT=$?

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci-it down --remove-orphans

if [ ${DOCKER_WAIT_FOR_SUT} -ne 0 ]; then echo "Integration Tests for sync app failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_ASYNC_SUT} -ne 0 ]; then echo "Integration Tests for async app failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_MYPYC_SUT} -ne 0 ]; then echo "Integration Tests for mypyc sync app failed"; exit 1; fi
