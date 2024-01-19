#!/bin/bash

# This setup script will:
# (1) Build the credit-processor-service app
# (2) Export the image from docker
# (3) Import it into k3s
#     (Steps 2 and 3 are so we don't need to use a public registry)
# (4) Deploy the service in kubernetes
# (5) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-processor-service app
docker build -t credit-processor-service:latest creditprocessorservice

# (2) Export the image from docker
docker save --output credit-processor-service.tar credit-processor-service:latest

# (3) Import it into k3s
sudo k3s ctr images import credit-processor-service.tar

# (4) Deploy the service in kubernetes
kubectl apply -f creditprocessorservice/creditprocessorservice.yaml

# (5) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(creditprocessorservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditprocessorservice pod:"
  kubectl delete po $POD
fi

echo ""
echo Redeployed creditprocessorservice.
