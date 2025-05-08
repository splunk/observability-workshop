#!/bin/bash

cd ~/otel-discovery-demo

export KAFKA_BROKER=localhost:9092
export DB_URL="jdbc:mysql://localhost/MyDB"

echo Building the Java app
./src/loanservice/gradlew build -p ./src/loanservice
mv ./src/loanservice/build/libs/loanservice-0.0.1-SNAPSHOT.jar ./src/loanservice/build/libs/loanservice.jar

echo Starting the Java app
nohup java -jar ./src/loanservice/build/libs/loanservice.jar &
