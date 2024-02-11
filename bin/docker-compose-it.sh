#!/bin/bash

DOCKER_COMPOSE_FILE_NAME=docker-compose.it.yml
DOCKER_COMPOSE_FILE_PATH=../${DOCKER_COMPOSE_FILE_NAME}
[ -f ${DOCKER_COMPOSE_FILE_PATH} ] || DOCKER_COMPOSE_FILE_PATH=${DOCKER_COMPOSE_FILE_NAME}

docker-compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci_it build --build-arg VERSION=$(date +%s)
docker-compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci_it --compatibility up -d

(
    set -e
    docker wait ci_it_sut_1
    docker logs ci_it_sut_1
)
DOCKER_WAIT_FOR_SUT=$?

(
    set -e
    docker wait ci_it_async_sut_1
    docker logs ci_it_async_sut_1
)
DOCKER_WAIT_FOR_ASYNC_SUT=$?

(
    set -e
    docker wait ci_it_mypyc_sut_1
    docker logs ci_it_mypyc_sut_1
)
DOCKER_WAIT_FOR_MYPYC_SUT=$?

docker-compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci_it down --remove-orphans

if [ ${DOCKER_WAIT_FOR_SUT} -ne 0 ]; then echo "Integration Tests for sync app failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_ASYNC_SUT} -ne 0 ]; then echo "Integration Tests for async app failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_MYPYC_SUT} -ne 0 ]; then echo "Integration Tests for mypyc sync app failed"; exit 1; fi
