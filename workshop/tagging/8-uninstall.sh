#!/bin/bash

IMPL=${1:-py}

# This setup script will:
# (1) Uninstall all pods and services from the Kubernetes cluster

# (1) Uninstall all pods and services from the Kubernetes cluster
kubectl delete -f loadgenerator/loadgenerator.yaml
kubectl delete -f creditprocessorservice/creditprocessorservice.yaml
kubectl delete -f "creditcheckservice-${IMPL}/creditcheckservice.yaml"

echo ""
echo ""
echo ""
echo Uninstall complete
