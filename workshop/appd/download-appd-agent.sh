#!/bin/bash

#######################################################################
# Fetch the latest AppDynamics agent (Java or Machine) and extract     #
# it under ./agent or ./machine-agent. Defaults to the Java agent.     #
# Usage:                                                               #
#   ./download-appd-agent.sh           # Java agent (default)          #
#   ./download-appd-agent.sh java      # Java agent                    #
#   ./download-appd-agent.sh machine   # Machine agent (Linux x64)     #
# Requires: curl, unzip, jq                                            #
#######################################################################

check_command() {
    if ! command -v "$1" > /dev/null 2>&1; then
        echo "$1 is not installed. Installing..."
        sudo apt-get update
        sudo apt-get install -y "$1"
    else
        echo "$1 is already installed."
    fi
}

check_command curl
check_command unzip
check_command jq

AGENT_TYPE="${1:-java}"

case "$AGENT_TYPE" in
    java)
        INSTALL_DIR="./agent"
        PATTERN="java-jdk8"
        ZIP_NAME="JavaAgent.zip"
        ;;
    machine)
        INSTALL_DIR="./machine-agent"
        # The trailing [0-9] excludes the aarch64 build (whose name continues with letters).
        PATTERN="machineagent-bundle-64bit-linux-[0-9]"
        ZIP_NAME="MachineAgent.zip"
        ;;
    *)
        echo "Usage: $0 [java|machine]" >&2
        exit 1
        ;;
esac

mkdir -p "$INSTALL_DIR"

DOWNLOAD_ROOT="https://download-files.appdynamics.com/"

FILE_PATH=$(curl -s https://download.appdynamics.com/download/downloadfilelatest/ \
    | jq -r '.[].s3_path' \
    | grep -E "$PATTERN" \
    | head -1)

if [ -z "$FILE_PATH" ]; then
    echo "Could not find a matching $AGENT_TYPE agent download." >&2
    exit 1
fi

DOWNLOAD_PATH="${DOWNLOAD_ROOT}${FILE_PATH}"

echo "Downloading agent from: $DOWNLOAD_PATH"

curl -L "$DOWNLOAD_PATH" -o "./$ZIP_NAME"

unzip -o "./$ZIP_NAME" -d "$INSTALL_DIR"

rm -f "./$ZIP_NAME"
