#!/bin/bash

# This setup script will:
# (1) Install helm
# (2) Install the otel collector (for your org)

# required for helm to work correctly
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# (1) Install helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
helm repo update

# General variables
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

# Prompts
echo 'Enter environment (i.e. profiling-workshop-yourname):'
read ENVIRONMENT

# (2) Install the otel collector (for your org)
OTEL_VALUES_PATH="$SCRIPTPATH/otel/values.yaml"
MY_OTEL_VALUES_PATH="$SCRIPTPATH/otel/values-mine.yaml"
# Remove if previous exists
if [[ -e $MY_OTEL_VALUES_PATH ]]; then
  rm "$MY_OTEL_VALUES_PATH"
  echo "Removed previous $MY_OTEL_VALUES_PATH"
fi
cp $OTEL_VALUES_PATH $MY_OTEL_VALUES_PATH
# Update environment
sed -i "s/{{environment}}/$ENVIRONMENT/" $MY_OTEL_VALUES_PATH

# Install the otel collector
helm install --set cloudProvider=" " --set distribution=" " \
--set splunkObservability.accessToken="$ACCESS_TOKEN" \
--set clusterName="$ENVIRONMENT" \
--set splunkObservability.realm="$REALM" \
--set gateway.enabled="false" \
--set splunkObservability.profilingEnabled="true" \
-f $MY_OTEL_VALUES_PATH \
--generate-name splunk-otel-collector-chart/splunk-otel-collector

echo ""
echo ""
echo ""
echo Installed the otel collector for your environment.
