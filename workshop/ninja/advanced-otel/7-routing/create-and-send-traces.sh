#!/bin/bash

# Directory to store trace files
TRACE_DIR="./traces"
SERVICE_ENDPOINT="http://localhost:4318/v1/traces"

# Function to clean up and exit
cleanup() {
  echo "Cleaning up..."
  rm -rf "$TRACE_DIR"
  echo "Cleanup complete. Exiting."
  exit 0
}

# Trap Ctrl+C to invoke cleanup
trap cleanup SIGINT

# Check if trace directory already exists
if [ -d "$TRACE_DIR" ]; then
  echo "Warning: Trace directory '$TRACE_DIR' already exists. Exiting to avoid overwriting."
  exit 1
fi

# Create directory for trace files
mkdir -p "$TRACE_DIR"

# Array of services
SERVICES=("frontend" "database" "restocking" "payment")

# Function to get the timestamp in nanoseconds
get_nanoseconds_timestamp() {
  SECONDS=$(date +%s)
  NANOS=$(date +%N 2>/dev/null || echo "000000000")

  # Check if NANOS is numeric; otherwise, use "000000000"
  if ! [[ $NANOS =~ ^[0-9]+$ ]]; then
    NANOS="000000000"
  fi

  echo "${SECONDS}$(printf "%09d" ${NANOS:0:9})"
}

# Function to generate a trace file
generate_trace() {
  SERVICE=$1
  TRACE_ID=$(uuidgen | tr -d '-')
  SPAN_ID=$(uuidgen | tr -d '-' | head -c 16)
  START_TIME=$(get_nanoseconds_timestamp)
  END_TIME=$((START_TIME + 1000000000)) # Add 1 second in nanoseconds
  SECURITY_VALUE=$2

  cat <<EOF > "$TRACE_DIR/trace_$SERVICE_$(uuidgen).json"
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": { "stringValue": "$SERVICE" }
          }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "$SERVICE.scope",
            "version": "1.0.0"
          },
          "spans": [
            {
              "traceId": "$TRACE_ID",
              "spanId": "$SPAN_ID",
              "name": "$SERVICE-operation",
              "kind": "SPAN_KIND_INTERNAL",
              "startTimeUnixNano": "$START_TIME",
              "endTimeUnixNano": "$END_TIME",
              "attributes": [
                {
                  "key": "security",
                  "value": { "stringValue": "$SECURITY_VALUE" }
                },
                {
                  "key": "operation",
                  "value": { "stringValue": "$SERVICE-operation" }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
EOF
}

# Generate 20 traces
echo "Generating 20 traces..."
for i in {1..20}; do
  SERVICE=${SERVICES[$RANDOM % ${#SERVICES[@]}]}
  # Set security attribute to "unknown" for the first and last trace, "high" otherwise
  if [ "$i" -eq 1 ] || [ "$i" -eq 20 ]; then
    SECURITY_VALUE="unknown"
  else
    SECURITY_VALUE="high"
  fi
  generate_trace "$SERVICE" "$SECURITY_VALUE"
done
echo "Traces generated in $TRACE_DIR"

# Function to send a random trace
send_random_trace() {
  TRACE_FILES=("$TRACE_DIR"/*.json)
  RANDOM_TRACE=${TRACE_FILES[$RANDOM % ${#TRACE_FILES[@]}]}

  echo "Sending trace: $RANDOM_TRACE"
  curl -X POST -i "$SERVICE_ENDPOINT" \
    -H "Content-Type: application/json" \
    -d @"$RANDOM_TRACE"
  
  if [ $? -ne 0 ]; then
    echo "Warning: Failed to send trace $RANDOM_TRACE. Continuing..."
  fi
}

# Keep sending random traces every 5 seconds
echo "Sending random traces every 5 seconds. Press Ctrl+C to stop."
while true; do
  send_random_trace
  sleep 5
done
