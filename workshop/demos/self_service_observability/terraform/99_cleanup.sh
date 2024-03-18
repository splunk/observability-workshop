#!/bin/bash
terraform destroy --auto-approve
rm terraform.tfstate
rm terraform.tfstate.backup
rm .terraform.lock.hcl
cp tf_files/01_initial.tf main.tf