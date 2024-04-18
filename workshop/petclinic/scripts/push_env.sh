#!/bin/bash

# Define the path to the JavaScript file
JS_FILE="/home/splunk/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/static/scripts/env.js"

# Create the directory if it doesn't exist
mkdir -p "$(dirname "$JS_FILE")"

# Write the content to the JavaScript file
cat <<EOF > "$JS_FILE"
env = {
  RUM_REALM: '$RUM_REALM',
  RUM_AUTH: '$RUM_AUTH',
  RUM_APP_NAME: '$RUM_APP_NAME',
  RUM_ENVIRONMENT: '$RUM_ENVIRONMENT'
}
EOF

echo "JavaScript file generated at: $JS_FILE"
