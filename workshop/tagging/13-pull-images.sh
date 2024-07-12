#!/usr/bin/env bash

# meant to be executed locally by a facilitator to preload workshop instances with docker images

# REGISTRY=docker.io
R_USER=achimstaebler

#1             2       3       4       5       6           7   8
#adminUsername,sshPass,sshUser,sshHost,sshPort,o11yCloudID,url,adminPassword
SHOW_CSV="${1?Usage: $0 <CSV>}"
TAG=${R_USER}/

< "${SHOW_CSV}" sed -E '1 s/ssh,/sshUser,sshHost,sshPort,/; s/,ssh \-p ([0-9]+) ([a-z]+)@([^,]*)/,\2,\3,\1/' |
    parallel --colsep , --header --will-cite --tty sshpass -p{2} ssh -F none -l {3} -p {5} {4} \
    "cd workshop/tagging &&
    docker pull ${TAG}credit-check-service:1.0 &&
    docker pull ${TAG}credit-check-service:1.1 &&
    docker pull ${TAG}credit-processor-service:1.0 &&
    docker pull ${TAG}loadgenerator:1.0"
