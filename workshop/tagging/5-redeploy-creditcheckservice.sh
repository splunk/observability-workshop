#!/bin/bash

# This setup script will:
# (1) Build the credit-check-service app
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
# (4) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-check-service app
IMPL=${1:-py}
docker build -t credit-check-service:latest "creditcheckservice-${IMPL}"

# (2) Import it into k3d
sudo k3d image import credit-check-service:latest --cluster $INSTANCE-cluster

# (3) Deploy the service in kubernetes
kubectl apply -f "creditcheckservice-${IMPL}/creditcheckservice.yaml"

# (4) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(creditcheckservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditcheckservice pod:"
  kubectl delete po "$POD"
fi

echo ""
echo Redeployed creditcheckservice.
