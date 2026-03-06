#!/bin/bash

echo "Finding processes for load scripts currently running..."
ps -ef | grep appd-sc-home-init
sleep 1s
ps -ef | grep appd-sc-slow-query
sleep 1s
ps -ef | grep appd-sc-session
sleep 1s
ps -ef | grep appd-sc-sell-car
sleep 1s
ps -ef | grep appd-sc-request-error
sleep 1s
ps -ef | grep appd-sc-search
sleep 1s
ps -ef | grep appd-sc-mem-leak-insurance
sleep 1s
