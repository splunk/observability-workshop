#!/bin/bash
export ACCESS_TOKEN=
export REALM=
export RUM_TOKEN=
export HEC_TOKEN=
export HEC_URL=
export INSTANCE=

orb create -c orbstack.yaml -a amd64 ubuntu:jammy
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m ubuntu -u splunk ansible-playbook /home/splunk/orb-configure-profile.yml
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m ubuntu -u splunk ansible-playbook /home/splunk/orb-configure-secrets.yml
ssh splunk@ubuntu@orb
