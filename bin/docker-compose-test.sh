#!/bin/bash

DOCKER_COMPOSE_FILE_NAME=docker-compose.test.yml
DOCKER_COMPOSE_FILE_PATH=../${DOCKER_COMPOSE_FILE_NAME}
[ -f ${DOCKER_COMPOSE_FILE_PATH} ] || DOCKER_COMPOSE_FILE_PATH=${DOCKER_COMPOSE_FILE_NAME}

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci build --build-arg VERSION=$(date +%s)
docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci up -d

(
    set -e
    docker wait ci-python3.8-1
    docker logs ci-python3.8-1
)
DOCKER_WAIT_FOR_PY38=$?

(
    set -e
    docker wait ci-python3.9-1
    docker logs ci-python3.9-1
)
DOCKER_WAIT_FOR_PY39=$?

(
    set -e
    docker wait ci-python3.10-1
    docker logs ci-python3.10-1
)
DOCKER_WAIT_FOR_PY310=$?

(
    set -e
    docker wait ci-python3.11-1
    docker logs ci-python3.11-1
)
DOCKER_WAIT_FOR_PY311=$?

(
    set -e
    docker wait ci-python3.12-1
    docker logs ci-python3.12-1
)
DOCKER_WAIT_FOR_PY312=$?

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci down --remove-orphans

if [ ${DOCKER_WAIT_FOR_PY38} -ne 0 ]; then echo "Test to Python 3.8 failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_PY39} -ne 0 ]; then echo "Test to Python 3.9 failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_PY310} -ne 0 ]; then echo "Test to Python 3.10 failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_PY311} -ne 0 ]; then echo "Test to Python 3.11 failed"; exit 1; fi
if [ ${DOCKER_WAIT_FOR_PY312} -ne 0 ]; then echo "Test to Python 3.12 failed"; exit 1; fi
