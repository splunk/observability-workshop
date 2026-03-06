#!/bin/bash

while true
do
    phantomjs --proxy-type=none --cookies-file=session-01.txt appd-sc-session-01.js
    phantomjs --proxy-type=none --cookies-file=session-02.txt appd-sc-session-02.js
    phantomjs --proxy-type=none --cookies-file=session-03.txt appd-sc-session-03.js
    phantomjs --proxy-type=none --cookies-file=session-04.txt appd-sc-session-04.js
    phantomjs --proxy-type=none --cookies-file=session-05.txt appd-sc-session-05.js
    phantomjs --proxy-type=none --cookies-file=session-06.txt appd-sc-session-06.js
    phantomjs --proxy-type=none --cookies-file=session-07.txt appd-sc-session-07.js
    phantomjs --proxy-type=none --cookies-file=session-08.txt appd-sc-session-08.js
    phantomjs --proxy-type=none --cookies-file=session-09.txt appd-sc-session-09.js
    phantomjs --proxy-type=none --cookies-file=session-10.txt appd-sc-session-03.js
    phantomjs --proxy-type=none --cookies-file=session-11.txt appd-sc-session-06.js
    phantomjs --proxy-type=none --cookies-file=session-12.txt appd-sc-session-07.js

    rm -f -v session-13.txt
    rm -f -v session-14.txt
    rm -f -v session-15.txt
    rm -f -v session-16.txt
    rm -f -v session-17.txt
    rm -f -v session-18.txt
    rm -f -v session-19.txt
    rm -f -v session-20.txt
    rm -f -v session-21.txt
    rm -f -v session-22.txt
    rm -f -v session-23.txt
    rm -f -v session-24.txt

    phantomjs --proxy-type=none --cookies-file=session-13.txt appd-sc-session-01.js
    phantomjs --proxy-type=none --cookies-file=session-14.txt appd-sc-session-02.js
    phantomjs --proxy-type=none --cookies-file=session-15.txt appd-sc-session-03.js
    phantomjs --proxy-type=none --cookies-file=session-16.txt appd-sc-session-04.js
    phantomjs --proxy-type=none --cookies-file=session-17.txt appd-sc-session-05.js
    phantomjs --proxy-type=none --cookies-file=session-18.txt appd-sc-session-06.js
    phantomjs --proxy-type=none --cookies-file=session-19.txt appd-sc-session-07.js
    phantomjs --proxy-type=none --cookies-file=session-20.txt appd-sc-session-08.js
    phantomjs --proxy-type=none --cookies-file=session-21.txt appd-sc-session-09.js
    phantomjs --proxy-type=none --cookies-file=session-22.txt appd-sc-session-03.js
    phantomjs --proxy-type=none --cookies-file=session-23.txt appd-sc-session-06.js
    phantomjs --proxy-type=none --cookies-file=session-24.txt appd-sc-session-07.js

    rm -f -v session-01.txt
    rm -f -v session-02.txt
    rm -f -v session-03.txt
    rm -f -v session-04.txt
    rm -f -v session-05.txt
    rm -f -v session-06.txt
    rm -f -v session-07.txt
    rm -f -v session-08.txt
    rm -f -v session-09.txt
    rm -f -v session-10.txt
    rm -f -v session-11.txt
    rm -f -v session-12.txt


done