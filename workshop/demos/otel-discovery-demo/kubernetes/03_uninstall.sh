#!/bin/bash

kubectl delete secret db-user-pass
kubectl delete secret db-myuser

kubectl delete -f ./loans.yaml --force
kubectl delete -f ./volume.yaml --force

echo Cleaning up existing database storage
sudo rm -Rf /mnt/data

helm uninstall kafka-release
