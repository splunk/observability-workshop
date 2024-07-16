#!/usr/bin/env bash

docker build -t credit-check-service:1.0 creditcheckservice-java
docker build -t credit-check-service:1.1 creditcheckservice-java-with-tags
docker build -t credit-check-service:1.0 creditcheckservice-py
docker build -t credit-check-service:1.1 creditcheckservice-py-with-tags
docker build -t credit-processor-service:latest creditprocessorservice
docker build -t loadgenerator:latest loadgenerator
