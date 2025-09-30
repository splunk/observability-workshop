#!/bin/bash

oc create namespace nvidia-nim-operator

oc create secret -n nvidia-nim-operator docker-registry ngc-secret \
    --docker-server=nvcr.io \
    --docker-username='$oauthtoken' \
    --docker-password=$NGC_API_KEY

operator-sdk run bundle ghcr.io/nvidia/k8s-nim-operator:bundle-latest-main --namespace nvidia-nim-operator

