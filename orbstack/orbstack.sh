#!/bin/bash
export ACCESS_TOKEN="wSgTADmdeTvrZBfHy3GPNA"
export REALM="eu0"
export RUM_TOKEN="XVZtGmYfvn2uQe9razgZbg"
export HEC_TOKEN="***REMOVED***"
export HEC_URL="https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event"

orb create -c orbstack.yaml -a amd64 ubuntu:jammy
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL orb -m ubuntu -u splunk ansible-playbook /home/splunk/orb-setup.yml
ssh splunk@ubuntu@orb
