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

echo Capturing the pod name
export POD_NAME=`kubectl get pod -l app=mysql -o name --no-headers=true`

echo Copying sample data and scripts to the pod
# Copy the sample data files to the database pod for import
kubectl cp ./mysql/users.csv ${POD_NAME:4}:/var/lib/mysql-files/users.csv
kubectl cp ./mysql/organizations.csv ${POD_NAME:4}:/var/lib/mysql-files/organizations.csv
kubectl cp ./mysql/populate_db.txt ${POD_NAME:4}:/tmp/populate_db.txt
kubectl cp ./mysql/populate_db.sh ${POD_NAME:4}:/tmp/populate_db.sh

# TODO: ensure the database is fully started
#while [[ $(kubectl exec -it ${POD_NAME:4} -- mysql -p"$MYSQL_ROOT_PASSWORD" -e "Show Databases;")? != 0 ]]; do
#   sleep 1
#done

echo Creating tables and application data
kubectl exec -it ${POD_NAME:4} -- /tmp/populate_db.sh

echo ""
echo Deployed the MySQL database
echo ""
