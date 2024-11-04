#!/bin/bash

# Specify the constant prefix
pod_prefix="customers-service-"

# Get the current pod name with the specified prefix
pod_name=$(kubectl get pods -o=name | grep "$pod_prefix" | cut -d'/' -f 2)

# Check if a pod with the specified prefix is found
if [ -n "$pod_name" ]; then
    # Continuously tail the logs, print each line, and stop after the specific line is shown
    kubectl logs -f "$pod_name" | awk '{print} /INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active./ {exit}'
else
    echo "Error: No pod found with the specified prefix."
fi