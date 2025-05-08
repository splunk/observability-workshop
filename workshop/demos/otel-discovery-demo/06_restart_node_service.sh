kill $(ps aux | grep 'consumer.js' | awk 'NR==1{print $2}')

export KAFKA_BROKER=localhost:9092

cd src/riskservice

nohup node ./consumer.js &
