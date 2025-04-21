#!/bin/bash

# This setup script will:
# (1) Create a persistent volume and persistent volume claim to be used for a MySQL database
# (2) Deploy a MySQL database pod and service in Kubernetes
# (3) Load sample data into the database

# Prompts
echo 'Enter your desired password for MySQL (be sure to make a note of it):'
read MYSQL_ROOT_PASSWORD

echo Creating a secret for the database password
kubectl create secret generic db-user-pass \
--from-literal=MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD"

echo Cleaning up existing database storage
sudo rm -Rf /mnt/data

echo Creating persistent volume and persistent volume claim
# (1) Create a persistent volume and persistent volume claim to be used for a MySQL database
kubectl apply -f mysql/volume.yaml

echo Deploying the MySQL database container
# (2) Deploy a MySQL database pod and service in Kubernetes
kubectl apply -f mysql/database.yaml

echo Waiting for the MySQL pod to be ready
while [[ $(kubectl get pods -l app=mysql -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do
   sleep 1
done

echo Creating a config map for the sample data
kubectl create configmap mysql-data --from-file=./mysql/users.csv --from-file=./mysql/organizations.csv --from-file=./mysql/populate_db.txt

echo ""
echo Deployed the MySQL database
echo ""
