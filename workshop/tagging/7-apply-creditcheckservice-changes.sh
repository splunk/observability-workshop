#!/bin/bash

# This setup script will:
# (1) Build the credit-check-service app that includes the changes for tagging
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (4) Deploy the service in kubernetes
# (5) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-check-service app
IMPL=${1:-py}

docker build -t credit-check-service:latest "creditcheckservice-${IMPL}-with-tags"

# (2) Import it into k3d
sudo k3d image import credit-check-service:latest --cluster $INSTANCE-cluster

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
