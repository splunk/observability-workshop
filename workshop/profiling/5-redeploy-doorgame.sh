#!/bin/bash

# This setup script will:
# (1) Build the doorgame app
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
# (4) Find and delete the pod (so it is redeployed)
#
# (1) Build the doorgame app
docker build -t doorgame:latest doorgame

# (2) Import it into k3d
sudo k3d image import doorgame:latest --cluster $INSTANCE-cluster

# (3) Deploy the service in kubernetes
kubectl apply -f doorgame/doorgame.yaml

# (4) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(doorgame[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting doorgame pod:"
  kubectl delete po $POD
fi

echo ""
echo Redeployed doorgame app.
