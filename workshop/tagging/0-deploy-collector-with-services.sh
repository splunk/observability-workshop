#!/bin/bash

if [ ! -f /home/splunk/.helmok ]; then
  helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
  helm repo update
  helm install splunk-otel-collector \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-k3s-cluster" \
  --set="environment=tagging-workshop-$INSTANCE" \
  splunk-otel-collector-chart/splunk-otel-collector

  cd /home/splunk/workshop/tagging/
  ./2-deploy-creditcheckservice.sh
  ./3-deploy-creditprocessorservice.sh
  ./4-deploy-load-generator.sh

  echo $INSTANCE > /home/splunk/.helmok
fi