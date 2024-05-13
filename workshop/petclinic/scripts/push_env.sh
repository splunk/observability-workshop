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
  RUM_REALM: '$REALM',
  RUM_AUTH: '$RUM_TOKEN',
  RUM_APP_NAME: '$INSTANCE-store',
  RUM_ENVIRONMENT: '$INSTANCE-workshop'
}
// non critical error so it shows in RUM when the realm is set
if (env.RUM_REALM != "") {
    let showJSErrorObject = false;
    showJSErrorObject.property = 'true';
  }
EOF

    echo "JavaScript file generated at: $JS_FILE"
else
    echo "Error: Repository directory does not exist."
fi