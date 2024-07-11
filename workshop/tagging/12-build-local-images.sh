#!/usr/bin/env bash

docker build -t credit-check-service:latest creditcheckservice-java
docker build -t credit-check-service:latest creditcheckservice-java-with-tags
docker build -t credit-check-service:latest creditcheckservice-py
docker build -t credit-check-service:latest creditcheckservice-py-with-tags
docker build -t credit-processor-service:latest creditprocessorservice
docker build -t loadgenerator:latest loadgenerator
