#!/usr/bin/env bash

IMPL="${1:-py}"
docker build -t credit-check-service:1.0 "creditcheckservice-${IMPL}"
docker build -t credit-check-service:1.1 "creditcheckservice-${IMPL}-with-tags"
# docker build -t credit-check-service:1.0 creditcheckservice-py
# docker build -t credit-check-service:1.1 creditcheckservice-py-with-tags
docker build -t credit-processor-service:latest creditprocessorservice
docker build -t loadgenerator:latest loadgenerator
