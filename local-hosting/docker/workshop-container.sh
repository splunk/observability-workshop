#!/bin/bash
# Build and start the workshop container. This is a normal Docker container.
# It is privileged because k3d creates the cluster nodes inside it. The host
# Docker socket is not mounted. SWIPE_ID, when set in this shell, is passed
# through and is not written into the image.

set -euo pipefail

cd "$(dirname "$0")"

IMAGE="workshop-k3d"
NAME="workshop-k3d"
VOLUME="workshop-k3d-docker"

if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running." >&2
    exit 1
fi

docker build -t "${IMAGE}" container

if docker container inspect "${NAME}" >/dev/null 2>&1; then
    if [ "$(docker inspect -f '{{.State.Running}}' "${NAME}")" != "true" ]; then
        docker start "${NAME}" >/dev/null
    fi
else
    docker volume create "${VOLUME}" >/dev/null
    docker run -d \
        --name "${NAME}" \
        --privileged \
        --hostname workshop \
        -p 81:81 \
        -p 82:82 \
        -p 9999:9999 \
        -p 443:443 \
        -v "${VOLUME}:/var/lib/docker" \
        -e SWIPE_ID \
        -e WORKSHOP_AGENTS \
        -e WORKSHOP_NODE_MEMORY \
        "${IMAGE}" >/dev/null
fi

echo "Site:  http://localhost:81"
echo "Logs:  docker logs -f ${NAME}"
echo "Shell: docker exec -it -u splunk ${NAME} zsh"
echo
docker logs -f "${NAME}"
