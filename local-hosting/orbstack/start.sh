#!/usr/bin/env bash
export TERM=xterm-256color

# Script requires two arguments:
# $1: Instance name - A name for your OrbStack instance (e.g. "splunk-workshop")
# $2: SWiPE ID - A valid Splunk Workshop ID to retrieve configuration

# Check if both arguments are provided
if [ $# -ne 2 ]; then
  echo "Error: This script requires two arguments."
  echo "Usage: $0 <instance_name> <swipe_id>"
  echo ""
  echo "  <instance_name>: Name for your OrbStack instance (e.g. 'splunk-workshop')"
  echo "  <swipe_id>: Valid Splunk Workshop ID to retrieve configuration"
  echo ""
  echo "Example: $0 splunk-workshop abc123"
  exit 1
fi

echo "Building instance '$1' with SWiPE ID '$2'";

JSON_RESPONSE=$(curl -s https://swipe.splunk.show/api?id=$2)
# Change these values below to match your environment and save this file as start.sh

# Check if Workshop ID not found
if [[ "$JSON_RESPONSE" == '{"message":"Workshop ID not found"}' ]]; then
  echo -e "Error: SWiPE ID '$2' not found. Please verify your Workshop ID and try again.\n" && exit 1
fi

# Parse the JSON response and extract values
export ACCESS_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.INGEST')
export API_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.API')
export REALM=$(echo ${JSON_RESPONSE} | jq -r '.REALM')
export RUM_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.RUM')
export HEC_TOKEN=$(echo ${JSON_RESPONSE} | jq -r '.HEC_TOKEN')
export HEC_URL=$(echo ${JSON_RESPONSE} | jq -r '.HEC_URL')
export INSTANCE=$1

echo "Creating instance '$INSTANCE' with configuration from SWiPE ID '$2'..."

# Do not change anything below this line
orb create -c cloud-init.yaml -a arm64 ubuntu:jammy "$INSTANCE"
sleep 2
ORBENV="ACCESS_TOKEN:REALM:API_TOKEN:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE" orb -m "$INSTANCE" -u splunk ansible-playbook /home/splunk/orbstack.yml
echo "Connect to your instance with:"
echo "ssh -t splunk@$INSTANCE@orb ${SHELL} -l"
ssh -t "splunk@$INSTANCE@orb" "${SHELL}" -l