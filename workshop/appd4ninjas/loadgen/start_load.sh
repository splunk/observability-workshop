#!/bin/bash


echo "Cleaning up artifacts from previous load..."
rm -f -v *.out
sleep 2s
echo "Starting home-init-01"
nohup ./appd-sc-home-init.sh &> home-init-01.out &
sleep 3s
echo "Waiting for additional JVMs to initialize... 1"
sleep 3s
echo "Waiting for additional JVMs to initialize... 2"
sleep 3s
echo "Waiting for additional JVMs to initialize... 3"
sleep 3s
echo "Waiting for additional JVMs to initialize... 4"
sleep 3s
echo "Waiting for additional JVMs to initialize... 5"
sleep 3s
echo "Waiting for additional JVMs to initialize... 6"
sleep 3s
echo "Waiting for additional JVMs to initialize... 7"
sleep 3s
echo "Waiting for additional JVMs to initialize... 8"
sleep 3s
echo "Waiting for additional JVMs to initialize... 9"
sleep 3s
echo "Waiting for additional JVMs to initialize... 10"
sleep 3s
echo "Waiting for additional JVMs to initialize... 11"
sleep 3s
echo "Waiting for additional JVMs to initialize... 12"
sleep 3s
echo "Waiting for additional JVMs to initialize... 13"
sleep 3s
echo "Waiting for additional JVMs to initialize... 14"
sleep 3s
echo "Waiting for additional JVMs to initialize... 15"
sleep 3s
echo "Waiting for additional JVMs to initialize... 16"
sleep 3s
echo "Waiting for additional JVMs to initialize... 17"
sleep 3s
echo "Waiting for additional JVMs to initialize... 18"
sleep 3s
echo "Waiting for additional JVMs to initialize... 19"
sleep 3s
echo "Waiting for additional JVMs to initialize... 20"
sleep 3s
echo "Starting slow-query-01"
nohup ./appd-sc-slow-query-01.sh &> slow-query-01.out &
sleep 2s
echo "Starting slow-query-02"
nohup ./appd-sc-slow-query-01.sh &> slow-query-02.out &
sleep 2s
echo "Starting slow-query-03"
nohup ./appd-sc-slow-query-01.sh &> slow-query-03.out &
sleep 2s
echo "Starting slow-query-04"
nohup ./appd-sc-slow-query-01.sh &> slow-query-04.out &
sleep 2s
echo "Starting sessions-01"
nohup ./appd-sc-sessions-01.sh &> sessions-01.out &
sleep 2s
echo "Starting sessions-02"
nohup ./appd-sc-sessions-01.sh &> sessions-02.out &
sleep 2s
echo "Starting sell-car-01"
nohup ./appd-sc-sell-car-01.sh &> sell-car-01.out &
sleep 3s
echo "Starting sell-car-02"
nohup ./appd-sc-sell-car-01.sh &> sell-car-02.out &
sleep 2s
echo "Starting sessions-03"
nohup ./appd-sc-sessions-01.sh &> sessions-03.out &
sleep 3s
echo "Starting sessions-04"
nohup ./appd-sc-sessions-01.sh &> sessions-04.out &
sleep 3s
echo "Starting search-01"
nohup ./appd-sc-search-01.sh &> search-01.out &
sleep 3s
echo "Starting request-error-01"
nohup ./appd-sc-request-error-01.sh &> request-error-01.out &
sleep 3s
echo "Starting mem-leak-insurance"
nohup ./appd-sc-mem-leak-insurance-start.sh &> mem-leak-insurance.out &
sleep 2s
echo "Finished starting load generator scripts"