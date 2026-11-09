# Workshop toolchain plus the Docker engine k3d uses for its nodes.
# The entrypoint starts dockerd on a local socket, then runs workshop-up.sh
# as splunk. The container has to be started privileged. It does not listen
# for Docker clients on the network.
FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852

ARG TARGETARCH
ARG KUBECTL_VERSION=v1.34.0
ARG HELM_VERSION=v3.22.1
ARG K9S_VERSION=v0.51.0
ARG TERRAFORM_VERSION=1.17.1
ARG K3D_VERSION=v5.9.0
ARG K3S_IMAGE=rancher/k3s:v1.33.4-k3s1
ARG STARSHIP_VERSION=v1.27.0
ARG DOCKER_CE_VERSION=5:29.9.3-1~ubuntu.24.04~noble
ARG DOCKER_CLI_VERSION=5:29.9.3-1~ubuntu.24.04~noble
ARG CONTAINERD_VERSION=2.4.2-3~ubuntu.24.04~noble
ARG BUILDX_VERSION=0.38.1-1~ubuntu.24.04~noble
ARG COMPOSE_VERSION=5.7.0-1~ubuntu.24.04~noble

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ansible \
        ca-certificates \
        cron \
        curl \
        git \
        gnupg \
        jq \
        net-tools \
        procps \
        python3 \
        python3-pip \
        python3-venv \
        rsyslog \
        iptables \
        kmod \
        sudo \
        unzip \
        vim \
        wget \
        whiptail \
        zsh \
    && rm -rf /var/lib/apt/lists/*

# Helm stays on 3. The workshop and the Chaos Mesh installer expect Helm 3.
# Checksums are the published digests for these exact release assets.
RUN <<'EOF'
set -euo pipefail
case "${TARGETARCH}" in
    amd64)
        kubectl_sha=cfda68cba5848bc3b6c6135ae2f20ba2c78de20059f68789c090166d6abc3e2c
        helm_sha=896cf63684a42a723d61c980369d6e588330927deb13676ca0d85006dd6da0ea
        k9s_sha=c3752ad51a5a4015a113819c4eeb6e55a4d0e4b8e652494797532f6fc8161dd7
        terraform_sha=4638628058e71a55212b1c563712eac03b902128f40740f3dc8174df12135061
        k3d_sha=06d8f25bc3a971c4eb29e0ff08429b180402db0f4dec838c9eac427e296800a0
        starship_arch=x86_64
        starship_sha=10c8eb4cb3b761d9bf59ea828444c2dab36c900b7d69a69e08814b286969df89
        ;;
    arm64)
        kubectl_sha=00b182d103a8a73da7a4d11e7526d0543dcf352f06cc63a1fde25ce9243f49a0
        helm_sha=4c29e286b279d170fa048ddfc3e4e83dcd069ca9c52102766ba672d7149e694d
        k9s_sha=3ee05c82e5f9198928a4e86133608ba6a2c10a2244d6a7789e820f78319d640c
        terraform_sha=988e950a1c23058093b0e66ab2d5fb53fc18345ecfbd5871acf51dbac9325edd
        k3d_sha=03cde5cf23e6e8e67de5a039ecf26e5b85aca82fba3e5d13dadf904cd218a250
        starship_arch=aarch64
        starship_sha=341f5cbf24699fa0b27ec88965ad25f862ea09e15d35a543fd6ffdff1d2aa00d
        ;;
    *)
        echo "Unsupported architecture: ${TARGETARCH}" >&2
        exit 1
        ;;
esac

verify() {
    echo "${1}  ${2}" | sha256sum -c -
}

fetch() {
    curl -fsSL --retry 3 --retry-delay 2 -o "$2" "$1"
}

workdir="$(mktemp -d)"
trap 'rm -rf "${workdir}"' EXIT
cd "${workdir}"

fetch "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${TARGETARCH}/kubectl" kubectl
verify "${kubectl_sha}" kubectl
install -m 0755 kubectl /usr/local/bin/kubectl

fetch "https://get.helm.sh/helm-${HELM_VERSION}-linux-${TARGETARCH}.tar.gz" helm.tgz
verify "${helm_sha}" helm.tgz
tar -xzf helm.tgz
install -m 0755 "linux-${TARGETARCH}/helm" /usr/local/bin/helm

fetch "https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TARGETARCH}.tar.gz" k9s.tgz
verify "${k9s_sha}" k9s.tgz
tar -xzf k9s.tgz k9s
install -m 0755 k9s /usr/local/bin/k9s

fetch "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${TARGETARCH}.zip" terraform.zip
verify "${terraform_sha}" terraform.zip
unzip -q terraform.zip
install -m 0755 terraform /usr/local/bin/terraform

fetch "https://github.com/k3d-io/k3d/releases/download/${K3D_VERSION}/k3d-linux-${TARGETARCH}" k3d
verify "${k3d_sha}" k3d
install -m 0755 k3d /usr/local/bin/k3d

fetch "https://github.com/starship/starship/releases/download/${STARSHIP_VERSION}/starship-${starship_arch}-unknown-linux-musl.tar.gz" starship.tgz
verify "${starship_sha}" starship.tgz
tar -xzf starship.tgz starship
install -m 0755 starship /usr/local/bin/starship
EOF

RUN printf '%s\n' \
        'fs.inotify.max_user_watches=524288' \
        'fs.inotify.max_user_instances=8192' \
        > /etc/sysctl.d/99-workshop.conf \
    && touch /var/log/syslog /var/log/auth.log \
    && chown syslog:adm /var/log/syslog /var/log/auth.log \
    && chmod 640 /var/log/syslog /var/log/auth.log \
    && useradd --create-home --shell /bin/zsh --user-group splunk \
    && echo 'splunk ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/splunk \
    && chmod 440 /etc/sudoers.d/splunk

# Accept only the fingerprints published in Docker's apt key.
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /tmp/docker.asc \
    && mapfile -t fingerprints < <(gpg --show-keys --with-colons /tmp/docker.asc | awk -F: '/^fpr:/ { print $10 }') \
    && allowed='9DC858229FC7DD38854AE2D88D81803C0EBFCD88 D3306A018370199E527AE7997EA0A9C3F273FCD8' \
    && test "${#fingerprints[@]}" -gt 0 \
    && for fingerprint in "${fingerprints[@]}"; do \
        case " ${allowed} " in \
            *" ${fingerprint} "*) ;; \
            *) echo "Unexpected Docker apt key ${fingerprint}" >&2; exit 1 ;; \
        esac; \
    done \
    && gpg --dearmor -o /etc/apt/keyrings/docker.gpg /tmp/docker.asc \
    && rm -f /tmp/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=${TARGETARCH} signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        "docker-ce=${DOCKER_CE_VERSION}" \
        "docker-ce-cli=${DOCKER_CLI_VERSION}" \
        "containerd.io=${CONTAINERD_VERSION}" \
        "docker-buildx-plugin=${BUILDX_VERSION}" \
        "docker-compose-plugin=${COMPOSE_VERSION}" \
    && rm -rf /var/lib/apt/lists/* \
    && usermod -aG docker splunk

COPY --chmod=755 workshop-up.sh /usr/local/sbin/workshop-up.sh
COPY --chmod=755 entrypoint.sh /usr/local/sbin/entrypoint.sh

RUN cat > /home/splunk/.zshrc <<'EOF'
autoload -U +X compinit && compinit -u
export TERM="${TERM:-xterm-256color}"
export INSTANCE="${INSTANCE:-workshop}"
export CLUSTER_NAME="${CLUSTER_NAME:-workshop-cluster}"
export KUBECONFIG="${KUBECONFIG:-${HOME}/.kube/config}"
alias kc='kubectl'
alias dc='docker compose'
if [ -f "${HOME}/.workshop-env" ]; then
    source "${HOME}/.workshop-env"
fi
command -v kubectl >/dev/null 2>&1 && source <(kubectl completion zsh)
command -v helm >/dev/null 2>&1 && source <(helm completion zsh)
command -v docker >/dev/null 2>&1 && source <(docker completion zsh)
command -v starship >/dev/null 2>&1 && eval "$(starship init zsh)"
EOF
RUN chown splunk:splunk /home/splunk/.zshrc

ENV INSTANCE=workshop \
    CLUSTER_NAME=workshop-cluster \
    KUBECONFIG=/home/splunk/.kube/config \
    K3S_IMAGE=${K3S_IMAGE}

HEALTHCHECK --interval=30s --timeout=10s --start-period=900s --retries=5 \
    CMD docker info >/dev/null

ENTRYPOINT ["/usr/local/sbin/entrypoint.sh"]
