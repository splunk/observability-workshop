#!/bin/bash

# This setup script will:
# (1) Build the doorgame app
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
#
# We will use 5-redeploy-doorgame.sh to update the app.
# It adds a step of manually finding and deleting the pod,
# because unless the kubernetes manifest is changed the pod
# won't redeploy with the new container image until it restarts.

# (1) Build the doorgame app
docker build -t doorgame:latest doorgame

# (2) Import it into k3d
sudo k3d image import doorgame:latest --cluster $INSTANCE-cluster

# (3) Deploy the service in kubernetes
kubectl apply -f doorgame/doorgame.yaml

echo ""
echo ""
echo ""
echo Deployed the new doorgame app.
echo ""
echo This is the service you will need to configure/code.
echo ""
echo You will use 5-redeploy-doorgame.sh after making any changes to redeploy the service.