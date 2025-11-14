#!/bin/bash

echo Installing Kafka using helm

# Note: disable SASL authentication on the client listener, to make it simpler for our demo application to connect
# Reference:  https://github.com/SolDevelo/charts/blob/main/README.md
helm install kafka-release oci://registry-1.docker.io/soldevelo/kafka-chart --set="listeners.client.protocol=PLAINTEXT"
