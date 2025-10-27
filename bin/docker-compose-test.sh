#!/bin/bash
set -eux

PYTHON_VERSION=${1:-3.14}
PRAGMA_VERSION=py${PYTHON_VERSION}
DOCKER_COMPOSE_FILE_NAME=compose.yml
DOCKER_COMPOSE_FILE_PATH=../${DOCKER_COMPOSE_FILE_NAME}
[ -f ${DOCKER_COMPOSE_FILE_PATH} ] || DOCKER_COMPOSE_FILE_PATH=${DOCKER_COMPOSE_FILE_NAME}

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci build --build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg VERSION=$(date +%s) unit-tests
docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci up unit-tests --abort-on-container-exit

DOCKER_WAIT_FOR=$?

docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci logs unit-tests
docker compose -f ${DOCKER_COMPOSE_FILE_PATH} -p ci down --remove-orphans

if [ ${DOCKER_WAIT_FOR} -ne 0 ]; then
    echo "Test to Python ${PYTHON_VERSION} failed"
    exit 1
fi
echo "Test to Python ${PYTHON_VERSION} passed"
