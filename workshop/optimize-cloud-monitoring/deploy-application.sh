#!/bin/bash

# This setup script will:
# (1) Remove existing helm releases
# (2) Add the required helm repos
# (3) Install the otel collector (for your org)
# Get the width of the terminal window
TERM_WIDTH=$(tput cols)

# Function to truncate text based on terminal width
truncate_text() {
    local text="$1"
    echo -n "${text:0:TERM_WIDTH}"
}

echo -e "\e[1mWelcome to the\e[0m"
echo -e "\e[32m$(truncate_text "                           ___  ____  ______ ____ ___ ___ ____ _____   ___                       ")"
echo -e "\e[32m$(truncate_text "                          /   \|    \|      |    |   |   |    |     | /  _]                      ")"
echo -e "\e[32m$(truncate_text "                         |     |  o  )      ||  || _   _ ||  ||__/  |/  [_                       ")"
echo -e "\e[32m$(truncate_text "                         |  O  |   _/|_|  |_||  ||  \_/  ||  ||   __|    _]                      ")"
echo -e "\e[32m$(truncate_text "                         |     |  |    |  |  |  ||   |   ||  ||  /  |   [_                       ")"
echo -e "\e[32m$(truncate_text "                         |     |  |    |  |  |  ||   |   ||  ||     |     |                      ")"
echo -e "\e[32m$(truncate_text "    __ _      ___  __ __ _\___/|__| ___|__| |____|___|___|____|_____|_____|___  ____ ____   ____ ")"
echo -e "\e[32m$(truncate_text "   /  ] |    /   \|  |  |   \      |   |   |/   \|    \|    |      |/   \|    \|    |    \ /    |")"
echo -e "\e[32m$(truncate_text "  /  /| |   |     |  |  |    \     | _   _ |     |  _  ||  ||      |     |  D  )|  ||  _  |   __|")"
echo -e "\e[32m$(truncate_text " /  / | |___|  O  |  |  |  D  |    |  \_/  |  O  |  |  ||  ||_|  |_|  O  |    / |  ||  |  |  |  |")"
echo -e "\e[32m$(truncate_text "/   \_|     |     |  :  |     |    |   |   |     |  |  ||  |  |  | |     |    \ |  ||  |  |  |_ |")"
echo -e "\e[32m$(truncate_text "\     |     |     |     |     |    |   |   |     |  |  ||  |  |  | |     |  .  \|  ||  |  |     |")"
echo -e "\e[32m$(truncate_text " \____|_____|\___/ \__,_|_____|    |___|___|\___/|__|__|____| |__|  \___/|__|\_|____|__|__|___,_|")"
echo -e "\e[0m"
echo -e "\e[1mWorkshop\e[0m"
echo -e " "
echo -e " "
echo -e " "

# (1) Remove existing helm releases
# Check if there are any existing helm releases
echo -e "\e[36mPerforming pre-checks...\e[0m"
echo -e "Checking for existing helm releases..."
if [ -n "$(helm ls --all --short)" ]; then
    # Remove existing helm releases
    echo -e "Removing existing helm releases..."
    helm ls --all --short | xargs -L1 helm delete
else
    echo -e "No existing helm releases found."
fi

echo -e "Adding the required helm repos..."
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart
echo -e "Updating helm repos..."
helm repo update

# General variables
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

# Prompts
echo -e " "
echo -e " "
echo -e " "
echo -e "\e[36mEnter your favorite city (i.e. Detroit):\e[0m"
read WORKSHOP_CITY

# (2) Install the otel collector (for your org)
OTEL_VALUES_PATH="$SCRIPTPATH/values/values.yaml"
MY_OTEL_VALUES_PATH="$SCRIPTPATH/values/values-mine.yaml"
# Remove if previous exists
if [[ -e $MY_OTEL_VALUES_PATH ]]; then
  rm "$MY_OTEL_VALUES_PATH"
fi
cp $OTEL_VALUES_PATH $MY_OTEL_VALUES_PATH
# Update environment

if [ -z "$WORKSHOP_CITY" ]; then
    echo -e "\e[36mEnter your favorite city (i.e. Detroit):\e[0m"
    read WORKSHOP_CITY
fi

if [ -n "$WORKSHOP_CITY" ]; then
    sed -i "s/Detroit/$WORKSHOP_CITY/" "$MY_OTEL_VALUES_PATH"
else
    echo "Error: Workshop city is empty. Exiting..."
    exit 1
fi

echo -e "\e[1mUpdated Workshop City in $MY_OTEL_VALUES_PATH\e[0m"
echo -e " "

#Install the otel collector.
echo -e "\e[1mInstalling OpenTelemetry Collector\e[0m"
helm install splunk-otel-collector \
--set="operator.enabled=true" \
--set="certmanager.enabled=true" \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkObservability.logsEnabled=false" \
--set="logsEngine=otel" \
--set="splunkObservability.profilingEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
--set="environment=$INSTANCE-workshop" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f $MY_OTEL_VALUES_PATH

if helm ls --all --short | grep -q "splunk-otel-collector"; then
    # Splunk OpenTelemetry Collector is installed
    echo -e " "
    echo -e "\e[32mSplunk OpenTelemetry Collector Successfully Installed\e[0m"
else
    # Splunk OpenTelemetry Collector is not installed
    echo -e " "
    echo -e "\e[31mSomething went wrong. Press ctrl+C to cancel and try again.\e[0m"
fi

# (3) Install the OpenTelemetry Demo application
echo -e " "
echo -e "\e[1mDeploying OpenTelemetry Demo Application\e[0m"

helm install opentelemetry-demo open-telemetry/opentelemetry-demo --values $SCRIPTPATH/values/otel-demo.yaml

if helm ls --all --short | grep -q "opentelemetry-demo"; then
    # Splunk OpenTelemetry Collector is installed
    echo -e " "
    echo -e "\e[32mOpenTelemetry Demo Application Successfully Installed\e[0m"
else
    # Splunk OpenTelemetry Collector is not installed
    echo -e " "
    echo -e "\e[31mSomething went wrong. Press ctrl+C to cancel and try again.\e[0m"
fi

# (3) Install the OpenTelemetry Demo application
echo -e " "
echo -e "\e[1mDeploying Kubernetes Ingress Controller\e[0m"

kubectl apply -f $SCRIPTPATH/manifests/frontend-external.yaml

echo -e "\e[32mKubernetes Ingress Controller Deployed Successfully\e[0m"
echo -e " "
echo -e " "
echo -e " "
echo -e "\e[1mWorkshop Setup Complete\e[0m"
echo -e "\e[1mYour instance name is: \e[36m$INSTANCE\e[0m"
echo -e "\e[1mYour demo application will be available at http://$RUM_FRONTEND_IP:81 shortly\e[0m"