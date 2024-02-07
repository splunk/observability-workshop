#!/bin/bash

# List of services to patch
services=("config-server" "discovery-service" "admin-server")

# Loop through each service and apply the kubectl patch command
for service in "${services[@]}"; do
    echo "Patching deployment for $service"
    kubectl patch deployment "$service" -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"default/splunk-otel-collector"}}}} }'
done

echo "Patch applied to all services"
