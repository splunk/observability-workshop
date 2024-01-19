#!/bin/bash

# This setup script will:
# (1) Install the otel collector (for your org)

# General variables
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

# Prompts
echo 'Enter environment (i.e. qep):'
read ENVIRONMENT
echo 'Enter realm (i.e. us1):'
read REALM
echo 'Enter ingest token:'
read INGEST_TOKEN

# (1) Install the otel collector (for your org)
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
--set splunkObservability.accessToken="$INGEST_TOKEN" \
--set clusterName="$ENVIRONMENT" --set splunkObservability.realm="$REALM" \
--set gateway.enabled="false" \
-f $MY_OTEL_VALUES_PATH \
--generate-name splunk-otel-collector-chart/splunk-otel-collector

echo ""
echo ""
echo ""
echo Installed the otel collector for your environment.
