#!/bin/bash

# This setup script will:
# (1) Install helm chart
# (2) Install the otel collector

  # ensure the environment variables are read
  source ~/.profile

  helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
  helm repo update
  helm install splunk-otel-collector --version 0.111.0 \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-k3s-cluster" \
  --set="environment=tagging-workshop-$INSTANCE" \
  splunk-otel-collector-chart/splunk-otel-collector \
  -f otel/values.yaml

echo ""
echo ""
echo ""
echo Installed the otel collector for your environment.
