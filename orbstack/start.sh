#!/bin/bash
echo "Building: $1";
export ACCESS_TOKEN="wSgTADmdeTvrZBfHy3GPNA"
export REALM="eu0"
export RUM_TOKEN="XVZtGmYfvn2uQe9razgZbg"
export HEC_TOKEN="***REMOVED***"
export HEC_URL="https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event"
export INSTANCE=$1

orb create -c cloud-init.yaml -a arm64 ubuntu:jammy $INSTANCE
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m $INSTANCE -u splunk ansible-playbook /home/splunk/orbstack-profile.yml
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m $INSTANCE -u splunk ansible-playbook /home/splunk/orbstack-secrets.yml
echo "ssh plunk@$INSTANCE@orb"
ssh splunk@$INSTANCE@orb
