#!/bin/bash

echo Installing Kafka using helm

# Note: disable SASL authentication on the client listener, to make it simpler for our demo application to connect
# Reference:  https://github.com/bitnami/charts/blob/main/bitnami/kafka/README.md
helm install kafka-release oci://registry-1.docker.io/bitnamicharts/kafka --set="listeners.client.protocol=PLAINTEXT"
