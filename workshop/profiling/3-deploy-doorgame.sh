#!/bin/bash

# This setup script will:
# (1) Build the doorgame app
# (2) Export the image from docker
# (3) Import it into k3s
#     (Steps 2 and 3 are so we don't need to use a public registry)
# (4) Deploy the service in kubernetes
#
# We will use 4-redeploy-doorgame.sh to update the app.
# It adds a step of manually finding and deleting the pod,
# because unless the kubernetes manifest is changed the pod
# won't redeploy with the new container image until it restarts.

# (1) Build the doorgame app
docker build -t doorgame:latest doorgame

# (2) Export the image from docker
docker save --output doorgame.tar doorgame:latest

# (3) Import it into k3s
sudo k3s ctr images import doorgame.tar

# (4) Deploy the service in kubernetes
kubectl apply -f doorgame/doorgame.yaml

echo ""
echo ""
echo ""
echo Deployed the new doorgame app.
echo ""
echo This is the service you will need to configure/code.
echo ""
echo You will use 4-redeploy-doorgame.sh after making any changes to redeploy the service.