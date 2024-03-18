#!/bin/bash
set -x
cp tf_files/03_updated_title.tf main.tf
terraform apply -auto-approve