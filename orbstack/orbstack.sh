#!/bin/bash
<<<<<<< HEAD
export ACCESS_TOKEN=hOyyjQ-N0-cA1VyCkEKNYA
export REALM=eu0
export RUM_TOKEN=E_fENjAd3lAjW9QYUTbGRg
export HEC_TOKEN=43808242-7b23-4154-add6-9bd387833151
export HEC_URL=https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event
=======
export ACCESS_TOKEN=
export REALM=
export RUM_TOKEN=
export HEC_TOKEN=
export HEC_URL=
export INSTANCE=
>>>>>>> d88cc7d74 (Added instance env var)

orb create -c orbstack.yaml -a amd64 ubuntu:jammy
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m ubuntu -u splunk ansible-playbook /home/splunk/orb-configure-profile.yml
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m ubuntu -u splunk ansible-playbook /home/splunk/orb-configure-secrets.yml
ssh splunk@ubuntu@orb
