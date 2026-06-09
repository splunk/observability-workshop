#!/usr/bin/env bash
set -euo pipefail

LOCAL_RUNTIME="${LOCAL_RUNTIME:-kind}"

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This helper supports Debian/Ubuntu systems with apt-get. Install Docker, kubectl, Helm, and your local Kubernetes runtime manually for other distributions." >&2
  exit 1
fi

case "$LOCAL_RUNTIME" in
  kind|minikube|microk8s)
    ;;
  *)
    echo "Set LOCAL_RUNTIME to kind, minikube, or microk8s." >&2
    exit 1
    ;;
esac

sudo apt-get update
sudo apt-get install -y ca-certificates curl git gnupg lsb-release

if ! command -v docker >/dev/null 2>&1; then
  sudo apt-get install -y docker.io
  sudo usermod -aG docker "$USER" || true
  echo "Docker installed. You may need to log out and back in before running docker without sudo."
fi

ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64)
    KIND_ARCH=amd64
    MINIKUBE_ARCH=amd64
    KUBECTL_ARCH=amd64
    ;;
  aarch64|arm64)
    KIND_ARCH=arm64
    MINIKUBE_ARCH=arm64
    KUBECTL_ARCH=arm64
    ;;
  *)
    echo "Unsupported architecture: $ARCH" >&2
    exit 1
    ;;
esac

if ! command -v kubectl >/dev/null 2>&1; then
  KUBECTL_VERSION="$(curl -fsSL https://dl.k8s.io/release/stable.txt)"
  curl -fsSL -o /tmp/kubectl "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl"
  curl -fsSL -o /tmp/kubectl.sha256 "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl.sha256"
  echo "$(cat /tmp/kubectl.sha256)  /tmp/kubectl" | sha256sum --check
  sudo install -m 0755 /tmp/kubectl /usr/local/bin/kubectl
fi

if ! command -v helm >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
fi

if [[ "$LOCAL_RUNTIME" == "kind" ]] && ! command -v kind >/dev/null 2>&1; then
  KIND_VERSION="${KIND_VERSION:-v0.29.0}"
  curl -fsSL -o /tmp/kind "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-${KIND_ARCH}"
  sudo install -m 0755 /tmp/kind /usr/local/bin/kind
fi

if [[ "$LOCAL_RUNTIME" == "minikube" ]] && ! command -v minikube >/dev/null 2>&1; then
  curl -fsSL -o /tmp/minikube "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-${MINIKUBE_ARCH}"
  sudo install -m 0755 /tmp/minikube /usr/local/bin/minikube
fi

if [[ "$LOCAL_RUNTIME" == "microk8s" ]] && ! command -v microk8s >/dev/null 2>&1; then
  sudo apt-get install -y snapd
  sudo snap install microk8s --classic
  sudo usermod -aG microk8s "$USER" || true
  mkdir -p "$HOME/.kube"
  sudo chown -R "$USER" "$HOME/.kube" || true
  echo "MicroK8s installed. You may need to log out and back in before running microk8s commands without sudo."
fi

echo ""
echo "Verify tools with:"
echo "  git --version"
echo "  docker version"
echo "  kubectl version --client"
echo "  helm version"
case "$LOCAL_RUNTIME" in
  kind) echo "  kind version" ;;
  minikube) echo "  minikube version" ;;
  microk8s) echo "  microk8s status --wait-ready" ;;
esac
