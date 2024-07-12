#!/usr/bin/env bash

REGISTRY=docker.io
R_USER=achimstaebler

TAG=${R_USER}/

docker pull ${TAG}credit-check-service:1.0
docker pull ${TAG}credit-check-service:1.1
docker pull ${TAG}credit-processor-service:1.0
docker pull ${TAG}loadgenerator:1.0
