#!/bin/bash

# This setup script will:
# (1) Deploy the credit check service with tags in kubernetes using the image from Docker Hub
# (2) Find and delete existing pods (to force redeployment)
#
# (1) Deploy the services in kubernetes using images from Docker Hub
IMPL="${1:-py}"
kubectl apply -f "creditcheckservice-${IMPL}-with-tags/creditcheckservice-dockerhub.yaml"

# (2) Find and delete existing pods (to force redeployment)
podlist=$(kubectl get pods)
re="(creditcheckservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditcheckservice pod:"
  kubectl delete po $POD
fi

echo ""
echo Deployed the creditcheckservice with tags from Docker Hub images
