#!/bin/bash

echo "Finding processes for load scripts..."
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
echo "Stopping processes for load scripts..."
sudo pkill -f appd-sc-home-init
sleep 1s
sudo pkill -f appd-sc-slow-query
sleep 1s
sudo pkill -f appd-sc-session
sleep 1s
sudo pkill -f appd-sc-sell-car
sleep 1s
sudo pkill -f appd-sc-request-error
sleep 1s
sudo pkill -f appd-sc-search
sleep 1s
sudo pkill -f appd-sc-mem-leak-insurance
sleep 1s
echo "Checking for processes after stopping load..."
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
