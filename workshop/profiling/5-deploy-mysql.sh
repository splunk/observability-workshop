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

echo Creating a new table for user data
# Create a new database and table for user data
kubectl run -it --rm --image=mysql:8.3.0 --restart=Never mysql-client -- mysql -h mysql -p"$MYSQL_ROOT_PASSWORD" \
  -e 'CREATE DATABASE IF NOT EXISTS DoorGameDB; USE DoorGameDB;DROP TABLE IF EXISTS Users; CREATE TABLE Users (UserId VARCHAR(20), FirstName VARCHAR(100), LastName VARCHAR(100));'

echo Creating a new table for organization data
# Create a new table for organization data
kubectl run -it --rm --image=mysql:8.3.0 --restart=Never mysql-client -- mysql -h mysql -p"$MYSQL_ROOT_PASSWORD" \
  -e 'USE DoorGameDB;DROP TABLE IF EXISTS Organizations; CREATE TABLE Organizations (OrgId VARCHAR(256), Name VARCHAR(256), Country VARCHAR(256), Founded INT, NumEmployees INT);'

echo Capturing the pod name
export POD_NAME=`kubectl get pod -l app=mysql -o name --no-headers=true`

echo Copying sample data to the pod
# Copy the sample data files to the database pod for import
kubectl cp ./mysql/users.csv ${POD_NAME:4}:/var/lib/mysql-files/users.csv
kubectl cp ./mysql/organizations.csv ${POD_NAME:4}:/var/lib/mysql-files/organizations.csv

echo Loading sample data into MySQL
# Load sample data into the database
kubectl run -it --rm --image=mysql:8.3.0 --restart=Never mysql-client -- mysql -h mysql -p"$MYSQL_ROOT_PASSWORD" \
  -e "LOAD DATA INFILE '/var/lib/mysql-files/users.csv' INTO TABLE DoorGameDB.Users FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"

kubectl run -it --rm --image=mysql:8.3.0 --restart=Never mysql-client -- mysql -h mysql -p"$MYSQL_ROOT_PASSWORD" \
  -e "LOAD DATA INFILE '/var/lib/mysql-files/organizations.csv' INTO TABLE DoorGameDB.Organizations FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"


echo ""
echo Deployed the MySQL database
echo ""