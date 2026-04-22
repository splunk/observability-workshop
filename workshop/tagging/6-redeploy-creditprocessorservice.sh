#!/bin/bash

# This setup script will:
# (1) Build the credit-processor-service app
# (2) Push it to the local repository
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
# (4) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-processor-service app
docker build -t localhost:9999/credit-processor-service:latest creditprocessorservice

# (2) Push it to the local repository
docker push localhost:9999/credit-processor-service:latest

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
