#!/bin/bash

# This setup script will:
# (1) Create a persistent volume and persistent volume claim to be used for a MySQL database
# (2) Deploy a MySQL database pod and service in Kubernetes

# Prompts
echo 'Enter your desired password for MySQL (be sure to make a note of it):'
read MYSQL_ROOT_PASSWORD

kubectl create secret generic db-user-pass \
--from-literal=MYSQL_ROOT_PASSWORD='$MYSQL_ROOT_PASSWORD'

# (1) Create a persistent volume and persistent volume claim to be used for a MySQL database
kubectl apply -f mysql/volume.yaml

# (2) Deploy a MySQL database pod and service in Kubernetes
kubectl apply -f mysql/database.yaml

echo ""
echo ""
echo ""
echo Deployed the MySQL database
echo ""