#!/bin/bash

# This setup script will:
# (1) Build the load generator app
# (2) Push it to the local repository
#     (This is so we don't need to use a public registry)
# (3) Deploy the service in kubernetes

# (1) Build the load generator app
docker build -t localhost:9999/loadgenerator:latest loadgenerator

# (2) Push it to the local repository
docker push localhost:9999/loadgenerator:latest

# (3) Deploy the service in kubernetes
kubectl apply -f loadgenerator/loadgenerator.yaml

echo ""
echo ""
echo ""
echo Deployed the load generator.
