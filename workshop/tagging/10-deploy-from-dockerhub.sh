#!/bin/bash

# This setup script will:
# (1) Deploy the services in kubernetes using images from Docker Hub
# (2) Find and delete existing pods (to force redeployment)
#
# (1) Deploy the services in kubernetes using images from Docker Hub
kubectl apply -f creditcheckservice/creditcheckservice-dockerhub.yaml
kubectl apply -f creditprocessorservice/creditprocessorservice-dockerhub.yaml
kubectl apply -f loadgenerator/loadgenerator-dockerhub.yaml

# (2) Find and delete existing pods (to force redeployment)
podlist=$(kubectl get pods)
re="(creditcheckservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditcheckservice pod:"
  kubectl delete po $POD
fi

re="(creditprocessorservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditprocessorservice pod:"
  kubectl delete po $POD
fi

re="(loadgenerator[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting loadgenerator pod:"
  kubectl delete po $POD
fi

echo ""
echo Deployed the creditcheckservice, creditprocessorservice, and loadgenerator from Docker Hub images
