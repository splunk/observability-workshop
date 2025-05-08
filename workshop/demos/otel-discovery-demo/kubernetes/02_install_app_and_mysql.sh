#!/bin/bash

echo 'Enter a password to use for the MySQL root user:'
read MYSQL_ROOT_PASSWORD

echo Creating a secret for the database password
kubectl create secret generic db-user-pass \
--from-literal=MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD"

echo Cleaning up existing database storage
sudo rm -Rf /mnt/data

echo Creating a secret for the MySQL MyUser password
kubectl create secret generic db-myuser --from-literal=MYSQL_USER_NAME='MyUser' --from-literal=MYSQL_USER_PASSWORD='MyPassword'

echo Creating a persistent volume and persistent volume claim for MySQL
kubectl apply -f ./volume.yaml

echo Deploying the application and MySQL database
kubectl apply -f ./loans.yaml

echo Capturing the pod name
export POD_NAME=`kubectl get pod -l app=mysql -o name --no-headers=true`

echo Copying sample data and scripts to the pod

echo Waiting for the database to be ready
while ! kubectl exec -it ${POD_NAME:4} -- mysqladmin ping -p"$MYSQL_ROOT_PASSWORD" --silent; do
    sleep 5
done

# added extra sleep as issues occur when we attempt
# to connect to the database too quickly
sleep 10

echo Creating tables and application data
kubectl exec -it ${POD_NAME:4} -- mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS MyDB;"
kubectl exec -it ${POD_NAME:4} -- mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE USER 'MyUser'@'%' IDENTIFIED BY 'MyPassword';"
kubectl exec -it ${POD_NAME:4} -- mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "GRANT ALL PRIVILEGES ON MyDB.* TO 'MyUser'@'%';"
kubectl exec -it ${POD_NAME:4} -- mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "FLUSH PRIVILEGES;"
kubectl exec -it ${POD_NAME:4} -- mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "USE MyDB; CREATE TABLE Loans (ApplicantId INT, LoanAmount DECIMAL(10,2));"

