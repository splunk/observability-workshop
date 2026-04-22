#!/bin/bash

# This setup script will:
# (1) Build the credit-check-service app that includes the changes for tagging
# (2) Push it to the local repository
#     (This is so we don't need to use a public registry)
# (4) Deploy the service in kubernetes
# (5) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-check-service app
IMPL=${1:-py}

docker build -t localhost:9999/credit-check-service:latest "creditcheckservice-${IMPL}-with-tags"

# (2) Push it to the local repository
docker push localhost:9999/credit-check-service:latest

# (3) Deploy the service in kubernetes
kubectl apply -f "creditcheckservice-${IMPL}-with-tags/creditcheckservice.yaml"

# (4) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(creditcheckservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditcheckservice pod:"
  kubectl delete po "$POD"
fi

echo ""
echo Redeployed creditcheckservice-with-tags.
