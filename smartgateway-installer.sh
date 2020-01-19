#!/bin/bash
# Version 2.0
TOKEN=$1
REALM=$2
HOSTNAME=$3
CLUSTERNAME=$4

if [ -z "$1" ] ; then
  printf "Token not set, exiting ...\n"
  exit 1
else
  printf "Installing SmartGateway to /usr/local/bin ...\n"
fi

printf "\nDownloading SmartGateway, please hold on...\n"
printf "https://app."$REALM".signalfx.com/v2/smart-gateway/download"
curl -qs -H "X-SF-Token:"$TOKEN"" https://app."$REALM".signalfx.com/v2/smart-gateway/download | gunzip > /usr/local/bin/smart-gateway
chmod 755 /usr/local/bin/smart-gateway

mkdir -p /var/lib/gateway/etc
mkdir -p /var/lib/gateway/logs
mkdir -p /var/lib/gateway/data
chmod -R 777 /var/lib/gateway

cat << EOF > /var/lib/gateway/etc/gateway.conf
{
  "ServerName": "$HOSTNAME",
  "ClusterName": "$CLUSTERNAME",
  "EmitDebugMetrics": true,
  "StatsDelay": "10s",
  "LogDir": "/var/lib/gateway/logs",
  "ListenFrom": [
    {
      "Type": "signalfx",
      "ListenAddr": "0.0.0.0:8080"
    }
  ],
  "ForwardTo": [
    {
      "Type": "signalfx",
      "URL": "https://ingest.$REALM.signalfx.com/v2/datapoint",
      "EventURL": "https://ingest.$REALM.signalfx.com/v2/event",
      "TraceURL": "https://ingest.$REALM.signalfx.com/v1/trace",
      "DefaultAuthToken": "$TOKEN",
      "Name": "smart-gateway",
      "TraceSample": {
        "BackupLocation": "/var/lib/gateway/data"
      }
    }
  ]
}
EOF

printf "\nSmartGateway installation complete\n"
# To start the SmartGateway
# nohup /usr/local/bin/smart-gateway --configfile /var/lib/gateway/etc/gateway.conf &>/dev/null &
