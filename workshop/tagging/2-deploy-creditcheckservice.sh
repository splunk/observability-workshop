#!/bin/bash

# This setup script will:
# (1) Build the credit-check-service app
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
#
# We will use 5-redeploy-creditcheckservice.sh to update the app.
# It adds a step of manually finding and deleting the pod,
# because unless the kubernetes manifest is changed the pod
# won't redeploy with the new container image until it restarts.

# (1) Build the credit-check-service app
IMPL=${1:-py}

docker build -t credit-check-service:latest "creditcheckservice-${IMPL}"

# (2) Import it into k33
sudo k3d image import credit-check-service:latest --cluster $INSTANCE-cluster

# (3) Deploy the service in kubernetes
kubectl apply -f "creditcheckservice-${IMPL}/creditcheckservice.yaml"

echo ""
echo ""
echo ""
echo Deployed the new creditcheckservice.
echo ""
echo This is the service you will need to configure/code.
echo ""
echo You will use 5-redeploy-creditcheckservice.sh after making any changes to redeploy the service.
