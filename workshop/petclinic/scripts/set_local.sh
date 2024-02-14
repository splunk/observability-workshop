#!/bin/bash

# Define the deployment YAML file path
deployment_file="/home/ubuntu/workshop/petclinic/petclinic-deploy.yaml"

# Define the output file path
output_file="/home/ubuntu/workshop/petclinic/petclinic-local.yaml"

# Replace "image: quay.io/phagen" with "# image: quay.io/phagen"
sed 's/image: quay\.io\/phagen/#image: quay.io\/phagen/' "$deployment_file" > "$output_file"

# Replace "#image: localhost:5000/" with "image: localhost:9999/"
sed -i 's/#image: localhost:9999/image: localhost:9999/' "$output_file"

echo "Script execution completed. Modified content saved to $output_file."