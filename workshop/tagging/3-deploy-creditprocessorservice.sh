#!/bin/bash

# This setup script will:
# (1) Build the credit-processor-service app
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes
#
# We will use 6-redeploy-creditprocessorservice.sh to update the app.
# It adds a step of manually finding and deleting the pod,
# because unless the kubernetes manifest is changed the pod
# won't redeploy with the new container image until it restarts.

# (1) Build the credit-check-service app
docker build -t credit-processor-service:latest creditprocessorservice

# (2) Import it into k3d
sudo k3d image import credit-processor-service:latest --cluster $INSTANCE-cluster

# (3) Deploy the service in kubernetes
kubectl apply -f creditprocessorservice/creditprocessorservice.yaml

echo ""
echo ""
echo ""
echo Deployed the new creditprocessorservice.
echo ""
echo This is the service you will need to configure/code.
echo ""
echo You will use 6-redeploy-creditprocessorservice.sh after making any changes to redeploy the service.