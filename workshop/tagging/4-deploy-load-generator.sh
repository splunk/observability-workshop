#!/bin/bash

# This setup script will:
# (1) Build the load generator app
# (2) Import it into k3d
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes

# (1) Build the load generator app
docker build -t loadgenerator:latest loadgenerator

# (2) Import it into k3d
sudo k3d image import loadgenerator:latest --cluster $INSTANCE-cluster

# (3) Deploy the service in kubernetes
kubectl apply -f loadgenerator/loadgenerator.yaml

echo ""
echo ""
echo ""
echo Deployed the load generator.
