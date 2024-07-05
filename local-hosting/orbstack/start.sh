#!/bin/bash
echo "Building: $1";

# Change these values below to match your environment and safe this file as start.sh
export ACCESS_TOKEN="hOyyjQ-N0-cA1VyCkEKNYA"
export REALM="eu0"
export API_TOKEN="1mn3wTvNmpbhqIqi-5ylUQ"
export RUM_TOKEN="E_fENjAd3lAjW9QYUTbGRg"
export HEC_TOKEN="***REMOVED***"
export HEC_URL="https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event"
export INSTANCE=$1

orb create -c cloud-init.yaml -a arm64 ubuntu:jammy $INSTANCE
sleep 2
ORBENV=ACCESS_TOKEN:REALM:API_TOKEN:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m $INSTANCE -u splunk ansible-playbook /home/splunk/orbstack.yml
echo "ssh splunk@$INSTANCE@orb"
ssh splunk@$INSTANCE@orb
