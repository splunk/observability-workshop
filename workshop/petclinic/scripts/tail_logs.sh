#!/bin/bash

# Specify the constant prefix
pod_prefix="petclinic-loadgen-deployment-"

# Get the current pod name with the specified prefix
pod_name=$(kubectl get pods -o=name | grep "$pod_prefix" | cut -d'/' -f 2)

# Check if a pod with the specified prefix is found
if [ -n "$pod_name" ]; then
    # Continuously tail the logs from the specified pod
    kubectl logs -f "$pod_name"
else
    echo "Error: No pod found with the specified prefix."
fi
