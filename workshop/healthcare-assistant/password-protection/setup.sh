#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USERNAME="${1:-workshop}"
PASSWORD="${2:-}"

if [[ -z "$PASSWORD" ]]; then
  read -s -p "Enter password for user '$USERNAME': " PASSWORD
  echo
fi

# Generate htpasswd string — prefer htpasswd (bcrypt), fall back to openssl (APR1/MD5)
if command -v htpasswd &>/dev/null; then
  HTPASSWD=$(htpasswd -nb -B "$USERNAME" "$PASSWORD")
else
  HASH=$(openssl passwd -apr1 "$PASSWORD")
  HTPASSWD="$USERNAME:$HASH"
fi

# Create or update the credentials Secret
kubectl create secret generic basicauth-credentials \
  --from-literal=users="$HTPASSWD" \
  --dry-run=client -o yaml | kubectl apply -f -

# Apply the Traefik Middleware
kubectl apply -f "$SCRIPT_DIR/auth-middleware.yaml"

# Patch the existing Ingress to reference the middleware
# Format: <namespace>-<middleware-name>@kubernetescrd
kubectl patch ingress healthcare-assistant-ingress \
  -p '{"metadata":{"annotations":{"traefik.ingress.kubernetes.io/router.middlewares":"default-basicauth@kubernetescrd"}}}'

echo ""
echo "Password protection enabled."
echo "  Username: $USERNAME"
echo "  Access the app at http://localhost:81"
