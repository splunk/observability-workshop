#!/bin/bash

# This setup script will:
# (1) Build the doorgame app
# (2) Export the image from docker
# (3) Import it into k3s
#     (Steps 2 and 3 are so we don't need to use a public registry)
# (4) Deploy the service in kubernetes
# (5) Find and delete the pod (so it is redeployed)
#
# (1) Build the doorgame app
docker build -t doorgame:latest doorgame

# (2) Export the image from docker
docker save --output doorgame.tar doorgame:latest

# (3) Import it into k3s
sudo k3s ctr images import doorgame.tar

# (4) Deploy the service in kubernetes
kubectl apply -f doorgame/doorgame.yaml

# (5) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(doorgame[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting doorgame pod:"
  kubectl delete po $POD
fi

echo ""
echo Redeployed doorgame app.
