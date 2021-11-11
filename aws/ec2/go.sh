#!/usr/bin/env bash
set -eo pipefail

_stopnow() {
  test -f stopnow && echo "Stopping!" && rm stopnow && exit 0 || return 0
}

while true
do
    _stopnow
    # Below here, you put in your command you want to run:
     node /home/ubuntu/workshop/apm/microservices-demo/k8s/touchwebsite.js
done