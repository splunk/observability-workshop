#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Remove the middleware annotation from the Ingress
kubectl annotate ingress healthcare-assistant-ingress \
  traefik.ingress.kubernetes.io/router.middlewares- 2>/dev/null || true

# Delete the Middleware and credentials Secret
kubectl delete -f "$SCRIPT_DIR/auth-middleware.yaml" --ignore-not-found
kubectl delete secret basicauth-credentials --ignore-not-found

echo "Password protection removed."
