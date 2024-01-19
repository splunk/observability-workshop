#!/bin/bash

# This setup script will:
# (1) Build the load generator app
# (2) Export the image from docker
# (3) Import it into k3s
#     (Steps 2 and 3 are so we don't need to use a public registry)
# (4) Deploy the service in kubernetes

# (1) Build the load generator app
docker build -t loadgenerator:latest loadgenerator

# (2) Export the image from docker
docker save --output loadgenerator.tar loadgenerator:latest

# (3) Import it into k3s
sudo k3s ctr images import loadgenerator.tar

# (4) Deploy the service in kubernetes
kubectl apply -f loadgenerator/loadgenerator.yaml

echo ""
echo ""
echo ""
echo Deployed the load generator.
