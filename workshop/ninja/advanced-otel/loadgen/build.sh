#!/bin/bash

# Name of the Go application
APP_NAME="loadgen"

# Output directory for compiled binaries
OUTPUT_DIR="build"

# List of target operating systems and architectures
PLATFORMS=(
  "darwin/amd64"
  "darwin/arm64"
  "linux/amd64"
  "linux/arm64"
)

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to compile for a specific platform
compile() {
  local GOOS=$1
  local GOARCH=$2
  local OUTPUT_FILE="$OUTPUT_DIR/$APP_NAME-$GOOS-$GOARCH"

  echo "Compiling for $GOOS/$GOARCH..."
  env GOOS="$GOOS" GOARCH="$GOARCH" go build -o "$OUTPUT_FILE" .
  if [ $? -ne 0 ]; then
    echo "Failed to compile for $GOOS/$GOARCH"
    exit 1
  fi
  echo "Compiled successfully: $OUTPUT_FILE"
}

# Loop through all platforms and compile
for PLATFORM in "${PLATFORMS[@]}"; do
  GOOS=${PLATFORM%/*}
  GOARCH=${PLATFORM#*/}
  compile "$GOOS" "$GOARCH"
done

echo "All builds completed successfully. Output files are in the '$OUTPUT_DIR' directory."
