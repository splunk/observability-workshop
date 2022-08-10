#!/bin/bash
if [ -z ${REALM+x} ]; then echo "REALM is unset. Please export REALM=YOUR_REALM"; fi
if [ -z ${ACCESS_TOKEN+x} ]; then echo "ACCESS_TOKEN is unset. Please export ACCESS_TOKEN=YOUR_ACCESS_TOKEN"; fi
if [ -z ${RUM_TOKEN+x} ]; then echo "RUM_TOKEN is unset. Please export RUM_TOKEN=YOUR_RUM_TOKEN"; fi
if [ -z ${INSTANCE+x} ]; then echo "INSTANCE is unset. Please export RUM_TOKEN=YOUR_INSTANCE_NAME"; fi
envsubst '${REALM},${RUM_TOKEN},${INSTANCE}' < deployment-RUM-org.yaml > deploymentRUM.yaml
#sed -i 's/value: "0.75"/value: "0.99"/'  ./deploymentRUM.yaml

  