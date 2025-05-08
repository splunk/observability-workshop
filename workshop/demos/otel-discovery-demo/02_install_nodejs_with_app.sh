#!/bin/bash

echo Installing nodejs

curl -fsSL https://deb.nodesource.com/setup_23.x | sudo -E bash -
sudo apt install -y nodejs

export KAFKA_BROKER=localhost:9092

cd ~/otel-discovery-demo/src/riskservice

echo Installing packages required by Node.js app
npm install

echo Starting the node.js app
nohup node ./consumer.js &

