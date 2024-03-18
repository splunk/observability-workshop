#!/bin/bash
set -x
cp tf_files/04_add_detector.tf main.tf
terraform apply -auto-approve