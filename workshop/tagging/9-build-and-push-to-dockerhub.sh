#!/bin/bash

# This setup script will:
# (1) Build the creditcheckservice, creditprocessorservice, and loadgenerator images
# (2) Push the images to Docker Hub
#
# In the event that workshop attendees experiences issues building images locally
# they can use the pre-built images from Docker Hub instead. For the credit check
# service, we'll build images both without tags (1.0) and with tags (1.1).
#
# Before running this script, you must run docker login and authenticate
# to the desired docker hub account
#

REGISTRY=docker.io
R_USER=achimstaebler

arch=$(uname -m)

case "$arch" in
    "aarch64")
        PLATFORMS="linux/arm64"
        ;;
    "x86_64")
        PLATFORMS="linux/amd64"
        ;;
    "*")
        ;;
esac

TAG=${R_USER}/

# (1) Build the creditcheckservice, creditprocessorservice, and loadgenerator images
docker build --platform "${PLATFORMS}" -t "${TAG}credit-check-service:1.0" creditcheckservice-java
docker build --platform "${PLATFORMS}" -t "${TAG}credit-check-service:1.1" creditcheckservice-java-with-tags
docker build --platform "${PLATFORMS}" -t "${TAG}credit-processor-service:1.0" creditprocessorservice
docker build --platform "${PLATFORMS}" -t "${TAG}loadgenerator:1.0" loadgenerator

echo ""
echo ""
echo ""
echo Built the creditcheckservice, creditprocessorservice, and loadgenerator images successfully

docker login ${REGISTRY} -u ${R_USER}
docker push ${TAG}credit-check-service:1.0
docker push ${TAG}credit-check-service:1.1
docker push ${TAG}credit-processor-service:1.0
docker push ${TAG}loadgenerator:1.0

echo ""
echo ""
echo ""
echo Pushed the images to Docker Hub successfully
