#!/bin/bash

oc get csv -n nvidia-gpu-operator gpu-operator-certified.v25.3.0 -ojsonpath={.metadata.annotations.alm-examples} | jq .[0] > clusterpolicy.json
oc apply -f clusterpolicy.json

