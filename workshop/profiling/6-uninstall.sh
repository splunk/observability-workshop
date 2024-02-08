#!/bin/bash

# This setup script will:
# (1) Uninstall all pods and services from the Kubernetes cluster
# (2) Remove underlying storage used by the MySQL database volume

kubectl delete -f doorgame/doorgame.yaml
kubectl delete -f mysql/database.yaml
kubectl delete -f mysql/volume.yaml
kubectl delete secret db-user-pass

sudo rm -Rf /mnt/data

echo ""
echo ""
echo ""
echo Uninstall complete
