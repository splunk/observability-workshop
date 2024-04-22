#!/bin/bash
echo "Building: $1";
export ACCESS_TOKEN="wSgTADmdeTvrZBfHy3GPNA"
export REALM="eu0"
export RUM_TOKEN="XVZtGmYfvn2uQe9razgZbg"
export HEC_TOKEN="43808242-7b23-4154-add6-9bd387833151"
export HEC_URL="https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event"
export INSTANCE=$1

orb create -c cloud-init.yaml -a arm64 ubuntu:jammy $INSTANCE
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m $INSTANCE -u splunk ansible-playbook /home/splunk/orbstack-profile.yml
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m $INSTANCE -u splunk ansible-playbook /home/splunk/orbstack-secrets.yml
ssh splunk@$INSTANCE@orb
