#!/bin/bash

echo Updating the package manager
sudo apt update

echo Installing OpenJDK v17
sudo apt install -y openjdk-17-jdk openjdk-17-jre

echo Downloading Kafka
curl -sDL https://dlcdn.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz > ./kafka_2.13-3.8.0.tgz
echo Decompressing Kafka binary
tar -xzf ./kafka_2.13-3.8.0.tgz -C .

echo Starting Zookeeper
nohup ./kafka_2.13-3.8.0/bin/zookeeper-server-start.sh ./kafka_2.13-3.8.0/config/zookeeper.properties &

# update kafka config to ensure we can connect via localhost
sed -i 's$#listeners=PLAINTEXT://:9092$listeners=PLAINTEXT://localhost:9092$g' ./kafka_2.13-3.8.0/config/server.properties

# TODO: validate that Zookeeper started successfully

echo Starting Kafka
nohup ./kafka_2.13-3.8.0/bin/kafka-server-start.sh ./kafka_2.13-3.8.0/config/server.properties &

# TODO: validate that Kafka started successfully

echo Creating a Kafka topic for our application
./kafka_2.13-3.8.0/bin/kafka-topics.sh --create --topic loan-events --bootstrap-server localhost:9092


echo Confirming that the Kafka topic was created successfully
./kafka_2.13-3.8.0/bin/kafka-topics.sh --describe --topic loan-events --bootstrap-server localhost:9092
