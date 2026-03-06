#!/bin/bash

while true
do
    phantomjs --proxy-type=none appd-sc-slow-query-01.js
    sleep 6s
done