#!/bin/bash

sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS MyDB;"
sudo mysql -u root -e "CREATE USER 'MyUser'@'localhost' IDENTIFIED BY 'MyPassword';"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON MyDB.* TO 'MyUser'@'localhost';"
sudo mysql -u root -e "FLUSH PRIVILEGES;"
sudo mysql -u root -e "USE MyDB; CREATE TABLE Loans (ApplicantId INT, LoanAmount DECIMAL(10,2));"
