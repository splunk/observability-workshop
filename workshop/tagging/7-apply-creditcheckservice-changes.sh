#!/bin/bash

# This setup script will:
# (1) Build the credit-check-service app that includes the changes for tagging
# (2) Export the image from docker
# (3) Import it into k3s
#     (Steps 2 and 3 are so we don't need to use a public registry)
# (4) Deploy the service in kubernetes
# (5) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-check-service app
IMPL=${1:-py}

docker build -t credit-check-service:latest "creditcheckservice-${IMPL}-with-tags"

# (2) Export the image from docker
docker save --output credit-check-service.tar credit-check-service:latest

# (3) Import it into k3s
sudo k3s ctr images import credit-check-service.tar

# (4) Deploy the service in kubernetes
kubectl apply -f "creditcheckservice-${IMPL}-with-tags/creditcheckservice.yaml"

# (5) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(creditcheckservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditcheckservice pod:"
  kubectl delete po "$POD"
fi

echo ""
echo Redeployed creditcheckservice-with-tags.
