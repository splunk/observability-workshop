#!/bin/bash

# This setup script will:
# (1) Uninstall all pods and services from the Kubernetes cluster

kubectl delete -f doorgame/doorgame.yaml
kubectl delete -f mysql/database.yaml
kubectl delete -f mysql/volume.yaml
kubectl delete secret db-user-pass

echo ""
echo ""
echo ""
echo Uninstall complete
