#!/bin/bash
export ACCESS_TOKEN=
export REALM=
export RUM_TOKEN=
export HEC_TOKEN=
export HEC_URL=

orb create -c orbstack.yaml -a amd64 ubuntu:jammy
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL orb -m ubuntu -u splunk ansible-playbook /home/splunk/orb-setup.yml
ssh splunk@ubuntu@orb
