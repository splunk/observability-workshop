#!/bin/bash

oc create -f ./nfd-namespace.yaml
oc create -f ./nfd-operatorgroup.yaml
oc create -f ./nfd-sub.yaml
oc project openshift-nfd
