#!/bin/sh
set -eux

TZ=UTC
USERNAME=${1:-kuchulu}
UID=${2:-1666}
GROUPNAME=${3:-kuchulu}
GID=${4:-1666}
HOME_DIR=/home/${USERNAME}
APP_DIR=/app

ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
echo $TZ > /etc/timezone

if command -v apk >/dev/null 2>&1; then
    apk add --no-cache --update
    rm -rf /var/cache/*
    mkdir /var/cache/apk
    ln -sf /lib/ld-musl-x86_64.so.1 /usr/bin/ldd
    ln -sf /lib /lib64

    grep -q -E "^${GROUPNAME}:" /etc/group && echo "group '${GROUPNAME}' exists" || addgroup -g ${GID} -S ${GROUPNAME}
    grep -q -E "^${USERNAME}:" /etc/passwd && echo "user '${USERNAME}' exists" || adduser ${USERNAME} \
        --disabled-password \
        --gecos "Flask-JSONRPC User" \
        --ingroup ${GROUPNAME} \
        --no-create-home \
        --uid ${UID} \
        -s /bin/false \
        ${USERNAME}
elif command -v apt-get >/dev/null 2>&1; then
    apt-get update
    rm -rf /var/lib/apt/lists/*

    grep -q -E "^${GROUPNAME}:" /etc/group && echo "group '${GROUPNAME}' exists" || addgroup --gid ${GID} --system ${GROUPNAME}
    grep -q -E "^${USERNAME}:" /etc/passwd && echo "user '${USERNAME}' exists" || adduser \
        --disabled-password \
        --comment "Flask-JSONRPC User" \
        --ingroup ${GROUPNAME} \
        --no-create-home \
        --uid ${UID} \
        --shell /bin/false \
        ${USERNAME}
fi

mkdir -p /home/${USERNAME}
chown ${USERNAME}:${GROUPNAME} -R /home/${USERNAME}
mkdir -p ${APP_DIR}
chown ${USERNAME}:${GROUPNAME} -R ${APP_DIR}

find / -xdev -perm /6000 -exec echo {} \;
find / -xdev -perm /6000 -exec chmod a-s {} \;
