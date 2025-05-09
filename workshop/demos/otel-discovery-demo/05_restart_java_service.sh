kill $(ps aux | grep 'loanservice' | awk '{print $2}')

export KAFKA_BROKER=localhost:9092
export DB_URL="jdbc:mysql://localhost/MyDB"

nohup java -jar ~/workshop/demos/otel-discovery-demo/src/loanservice/build/libs/loanservice.jar &
