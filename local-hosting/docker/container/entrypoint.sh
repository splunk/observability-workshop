#!/bin/bash
# Start a private Docker engine, build the workshop cluster, then keep the
# engine running. k3d's nodes are containers, so this process has to be root
# inside a privileged container. The engine listens only on a local socket.

set -euo pipefail

export container=docker
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

enable_cgroup_nesting() {
    local attempt
    if [ ! -f /sys/fs/cgroup/cgroup.controllers ]; then
        return 0
    fi
    mkdir -p /sys/fs/cgroup/init
    for attempt in $(seq 1 20); do
        xargs -rn1 < /sys/fs/cgroup/cgroup.procs > /sys/fs/cgroup/init/cgroup.procs || true
        if sed -e 's/ / +/g' -e 's/^/+/' < /sys/fs/cgroup/cgroup.controllers \
            > /sys/fs/cgroup/cgroup.subtree_control; then
            return 0
        fi
        sleep 0.2
    done
    echo "Could not enable cgroup nesting. k3d nodes may fail to start." >&2
}

stop_dockerd() {
    if [ -n "${dockerd_pid:-}" ] && kill -0 "${dockerd_pid}" 2>/dev/null; then
        kill "${dockerd_pid}" 2>/dev/null || true
        wait "${dockerd_pid}" 2>/dev/null || true
    fi
}

if [ -d /sys/kernel/security ] && ! mountpoint -q /sys/kernel/security; then
    mount -t securityfs none /sys/kernel/security || echo "Could not mount securityfs." >&2
fi
enable_cgroup_nesting
mount --make-rshared / 2>/dev/null || echo "Could not make / a shared mount." >&2

rm -f /var/run/docker.pid /run/docker.pid /var/run/docker/containerd/containerd.pid
dockerd --host=unix:///var/run/docker.sock >/var/log/dockerd.log 2>&1 &
dockerd_pid=$!
trap stop_dockerd EXIT
trap 'stop_dockerd; exit 0' INT TERM

for _ in $(seq 1 60); do
    if docker info >/dev/null 2>&1; then
        break
    fi
    if ! kill -0 "${dockerd_pid}" 2>/dev/null; then
        echo "Docker engine exited during startup." >&2
        cat /var/log/dockerd.log >&2 || true
        exit 1
    fi
    sleep 1
done
if ! docker info >/dev/null 2>&1; then
    echo "Docker engine did not become ready." >&2
    cat /var/log/dockerd.log >&2 || true
    exit 1
fi

chgrp docker /var/run/docker.sock
chmod 660 /var/run/docker.sock

echo "Building the workshop cluster."
runuser --preserve-environment -u splunk -- /usr/local/sbin/workshop-up.sh

echo "Shell: docker exec -it -u splunk workshop-k3d zsh"
wait "${dockerd_pid}"
