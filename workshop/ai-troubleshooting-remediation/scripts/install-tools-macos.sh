#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required. Install it from https://brew.sh, then rerun this script." >&2
  exit 1
fi

brew update
brew install git kubectl helm kind minikube

if ! command -v docker >/dev/null 2>&1; then
  brew install --cask docker
  echo "Docker Desktop was installed. Start Docker Desktop from Applications before deploying the lab app."
else
  echo "Docker CLI already found."
fi

echo ""
echo "Verify tools with:"
echo "  git --version"
echo "  docker version"
echo "  kubectl version --client"
echo "  helm version"
echo "  kind version"
echo "  minikube version"

