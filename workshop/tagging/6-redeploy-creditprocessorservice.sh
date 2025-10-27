#!/bin/bash

# This setup script will:
# (1) Build the credit-processor-service app
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
# (4) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-processor-service app
docker build -t credit-processor-service:latest creditprocessorservice

# (2) Import it into k3d
sudo k3d image import credit-processor-service:latest --cluster $INSTANCE-cluster

# (3) Deploy the service in kubernetes
kubectl apply -f creditprocessorservice/creditprocessorservice.yaml

# (4) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(creditprocessorservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditprocessorservice pod:"
  kubectl delete po $POD
fi

echo ""
echo Redeployed creditprocessorservice.
