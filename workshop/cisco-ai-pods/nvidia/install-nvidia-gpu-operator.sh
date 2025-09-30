#!/bin/bash

oc create -f nvidia-gpu-operator.yaml
oc create -f nvidia-gpu-operatorgroup.yaml

oc create -f nvidia-gpu-sub.yaml
