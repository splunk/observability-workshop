
#!/bin/bash

#######################################################################
# This script will fetch the latest AppDynamics Sun/Oracle Java agent #
# and place it in the current directory under /appdynamics.            #
# This script requires:                                               #
# curl                                                                #
# unzip                                                                #
# jq                                                                  #
#######################################################################

# Function to check if a command is available and install it if not
check_command() {
    if ! command -v "$1" > /dev/null 2>&1; then
        echo "$1 is not installed. Installing..."
        sudo apt-get update
        sudo apt-get install -y "$1"
    else
        echo "$1 is already installed."
    fi
}

# Check and install required commands
check_command curl
check_command unzip
check_command jq

# Create the directory for the agent
INSTALL_DIR="./agent"
mkdir -p "$INSTALL_DIR"

# Download Root URL
DOWNLOAD_PATH="https://download-files.appdynamics.com/"

# Fetch latest Sun Java Agent download path from AppD
FILE_PATH=$(curl -s https://download.appdynamics.com/download/downloadfilelatest/ | jq -r '.[].s3_path' | grep java-jdk8)

# Construct the full URL
DOWNLOAD_PATH=$DOWNLOAD_PATH$FILE_PATH

# Print URL to stdout
echo "Downloading agent from: $DOWNLOAD_PATH"

# Fetch agent and write into working directory
curl -L $DOWNLOAD_PATH -o ./JavaAgent.zip

# Unzip the agent into the installation directory
unzip ./JavaAgent.zip -d "$INSTALL_DIR"

# Pass in the custom interceptors file
# cp ./custom-interceptors.xml "$INSTALL_DIR"/ver*/conf

# Pass in the custom correlation file
# cp ./custom-activity-correlation.xml "$INSTALL_DIR"/ver*/conf

# Pass in custom log4j, log4j2 config file
# cp ./log4j.xml "$INSTALL_DIR"/ver*/conf/logging
# cp ./log4j2.xml "$INSTALL_DIR"/ver*/conf/logging

# Remove the zip
rm -f ./JavaAgent.zip