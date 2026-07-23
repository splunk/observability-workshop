# Splunk Agent Observability Workshop Setup 

This folder includes scripts that can be used to provision a specific number of users 
for a workshop. The script will create a project for each user, and each user will only 
have access to their project. There's also a script to delete the users once the 
workshop is complete. 

## Configure the Environment

The first step is to make a copy of the `.env.example` file: 

``` bash
cp .env.example .env
```

Then, update the `.env` file to include the Galileo admin email address and password that 
the script will use to create/delete the users, and the password that users will use 
to log in to Splunk Agent Observability. 

> Note: make sure not to add the `.env` file to GitHub as it includes passwords. 

## Populate the users.csv file 


## Initialize the Environment

Run the following command to create a virtual environment with the required packages: 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Create the Users 

Run the following command to execute the user creation script: 

```bash
python batch_create_users.py --input-csv users.csv --output-csv results.csv
```

## Delete the Users

When the workshop is complete, run the following command to execute the user deletion script:

```bash
python batch_delete_users.py --input-csv users.csv --output-csv delete_results.csv
```