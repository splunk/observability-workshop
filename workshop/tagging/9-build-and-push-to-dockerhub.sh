#!/bin/bash

# This setup script will:
# (1) Build the creditcheckservice, creditprocessorservice, and loadgenerator images
# (2) Push the images to Docker Hub
#
# In the event that workshop attendees experiences issues building images locally
# they can use the pre-built images from Docker Hub instead. For the credit check
# service, we'll build images both without tags (1.0) and with tags (1.1).

# (1) Build the creditcheckservice, creditprocessorservice, and loadgenerator images
docker build -t derekmitchell399/credit-check-service:1.0 creditcheckservice
docker build -t derekmitchell399/credit-check-service:1.1 creditcheckservice-with-tags
docker build -t derekmitchell399/credit-processor-service:1.0 creditprocessorservice
docker build -t derekmitchell399/loadgenerator:1.0 loadgenerator

echo ""
echo ""
echo ""
echo Built the creditcheckservice, creditprocessorservice, and loadgenerator images successfully

docker push derekmitchell399/credit-check-service:1.0
docker push derekmitchell399/credit-check-service:1.1
docker push derekmitchell399/credit-processor-service:1.0
docker push derekmitchell399/loadgenerator:1.0

echo ""
echo ""
echo ""
echo Pushed the images to Docker Hub successfully
