#!/bin/bash

while true
do
	phantomjs --proxy-type=none appd-sc-request-error-01.js
    sleep 3m
    phantomjs --proxy-type=none appd-sc-request-error-01.js
    sleep 1m
    phantomjs --proxy-type=none appd-sc-request-error-01.js
    sleep 1m
    phantomjs --proxy-type=none appd-sc-request-error-01.js
    sleep 10m
    phantomjs --proxy-type=none appd-sc-request-error-01.js
    sleep 5m

done