#!/bin/bash

# Define the path to the repository directory
REPO_DIR="/home/splunk/spring-petclinic-microservices"

# Check if the repository directory exists
if [ -d "$REPO_DIR" ]; then
    echo "Repository directory exists."
    # Define the path to the JavaScript file
    JS_FILE="$REPO_DIR/spring-petclinic-api-gateway/src/main/resources/static/scripts/env.js"

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
else
    echo "Error: Repository directory does not exist."
fi