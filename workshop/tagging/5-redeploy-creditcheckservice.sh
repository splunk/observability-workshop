#!/bin/bash

# This setup script will:
# (1) Build the credit-check-service app
# (2) Push it to the local repository
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
# (4) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-check-service app
IMPL=${1:-py}
docker build -t localhost:9999/credit-check-service:latest "creditcheckservice-${IMPL}"

# (2) Push it to the local repository
docker push localhost:9999/credit-check-service:latest

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
