#!/bin/bash

while true; do
# Generate random loan amount between 100 and 1000
loan_amount=$((RANDOM % 901 + 100))

# Generate random sleep time between 100ms and 1000ms
sleep_time=$(awk -v min=0.1 -v max=1.0 'BEGIN{srand(); print min+rand()*(max-min)}')

# Make curl request with random loan amount
curl "http://localhost:8080/loanRequest?applicantId=1234&loanAmount=$loan_amount"

# Sleep for random time
sleep $sleep_time

done
