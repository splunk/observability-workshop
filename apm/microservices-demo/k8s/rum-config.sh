#!/bin/bash
if [ -z ${RUM_TOKEN+x} ]; then echo "RUM_TOKEN is unset. Please export RUM_TOKEN=YOUR_RUM_TOKEN"; fi
envsubst '${REALM},${RUM_TOKEN},${INSTANCE}' < deployment-host.yaml > deployment.yaml

#temporary add for Cold start RUM
sudo apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs 
npm install -s puppeteer
  