#!/bin/bash

while true
do
    phantomjs --proxy-type=none appd-sc-session-01.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-02.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-03.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-04.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-05.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-06.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-07.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-08.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-09.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-03.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-06.js
    sleep 6s
    phantomjs --proxy-type=none appd-sc-session-07.js
    sleep 6s
done