#!/bin/bash

# Function to generate random traceId and spanId
generate_trace_id() {
    echo $(openssl rand -hex 16 | tr '[:lower:]' '[:upper:]')
}

generate_span_id() {
    echo $(openssl rand -hex 8 | tr '[:lower:]' '[:upper:]')
}

# Function to get the current timestamp in nanoseconds
get_current_time() {
    echo $(($(date +%s) * 1000000000))
}

# Function to send a trace
send_trace() {
    local trace_id=$1
    local span_id=$2
    local start_time=$3
    local end_time=$4

    local span_json=$(cat <<EOF
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          { "key": "service.name", "value": { "stringValue": "Validation-service" } },
          { "key": "deployment.environment", "value": { "stringValue": "Advanced-Otel" } }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "fintest.library",
            "version": "1.0.0",
            "attributes": [
              { "key": "fintest.scope.attribute", "value": { "stringValue": "Euro, Dollar, Yen" } }
            ]
          },
          "spans": [
            {
              "traceId": "$trace_id",
              "spanId": "$span_id",
              "name": "/Login Validator",
              "startTimeUnixNano": "$start_time",
              "endTimeUnixNano": "$end_time",
              "kind": 2,
              "attributes":  [
                {
                  "key": "user.name",
                  "value": {
                    "stringValue": "George Lucas"
                  }
                },
                {
                  "key": "user.phone_number",
                  "value": {
                    "stringValue": "+1555-867-5309"
                  }
                },
                {
                  "key": "user.email",
                  "value": {
                    "stringValue": "george@deathstar.email"
                  }
                },
                {
                  "key": "user.account_password",
                  "value": {
                    "stringValue": "LOTR>StarWars1-2-3"
                  }
                },
                {
                  "key": "user.visa",
                  "value": {
                    "stringValue": "4111 1111 1111 1111"
                  }
                },
                {
                  "key": "user.amex",
                  "value": {
                    "stringValue": "3782 822463 10005"
                  }
                },
                {
                  "key": "user.mastercard",
                  "value": {
                    "stringValue": "5555 5555 5555 4444"
                  }
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
    )

    curl -X POST "http://localhost:4318/v1/traces" \
         -H "Content-Type: application/json" \
         -d "$span_json"

    echo -e "\nBase trace sent with traceId: $trace_id and spanId: $span_id"
}

# Function to send a health span
send_health_trace() {
    local trace_id=$1
    local span_id=$2
    local start_time=$3
    local end_time=$4

    local health_json=$(cat <<EOF
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          { "key": "service.name", "value": { "stringValue": "frontend-service" } }
          { "key": "deployment.environment", "value": { "stringValue": "Advanced-Otel" } }      ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "healthz",
            "version": "1.0.0",
            "attributes": [
              { "key": "healthz.scope.attribute", "value": { "stringValue": "Health check" } }
            ]
          },
          "spans": [
            {
              "traceId": "$trace_id",
              "spanId": "$span_id",
              "name": "/_healthz",
              "startTimeUnixNano": "$start_time",
              "endTimeUnixNano": "$end_time",
              "kind": 2,
              "attributes": [
                { "key": "health.status", "value": { "stringValue": "pass" } }
              ]
            }
          ]
        }
      ]
    }
  ]
}
EOF
    )

    curl -X POST "http://localhost:4318/v1/traces" \
         -H "Content-Type: application/json" \
         -d "$health_json"

    echo -e "\nHealth trace sent with traceId: $trace_id and spanId: $span_id"
}

# Check for -h flag
SEND_HEALTH=false
while getopts ":h" opt; do
  case ${opt} in
    h )
      SEND_HEALTH=true
      ;;
    \? )
      echo "Usage: $0 [-h] (Use -h to send a health span in between)"
      exit 1
      ;;
  esac
done

echo "Sending traces every 20 seconds. Use Ctrl-C to stop."

while true; do
    # Generate trace and span IDs for base span
    TRACE_ID=$(generate_trace_id)
    SPAN_ID=$(generate_span_id)
    CURRENT_TIME=$(get_current_time)
    END_TIME=$((CURRENT_TIME + 1000000000)) # Add 1 second

    # Send base trace
    send_trace "$TRACE_ID" "$SPAN_ID" "$CURRENT_TIME" "$END_TIME"

    if [ "$SEND_HEALTH" = true ]; then
        sleep 10  # Wait 10 seconds before sending health span

        # Generate trace and span IDs for health span
        HEALTH_TRACE_ID=$(generate_trace_id)
        HEALTH_SPAN_ID=$(generate_span_id)
        HEALTH_START_TIME=$(get_current_time)
        HEALTH_END_TIME=$((HEALTH_START_TIME + 1000000000))

        # Send health trace
        send_health_trace "$HEALTH_TRACE_ID" "$HEALTH_SPAN_ID" "$HEALTH_START_TIME" "$HEALTH_END_TIME"
    fi

    sleep 10  # Wait remaining 10 seconds before repeating
done