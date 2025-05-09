#!/bin/bash

cd ~/otel-discovery-demo

echo Installing MySQL 
sudo apt install -y mysql-server

echo Starting MySQL 
sudo systemctl start mysql.service

echo Creating database objects
sudo ./src/mysqldb/setup.sh
