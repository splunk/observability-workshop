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

# Function to send a base trace
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
          { "key": "deployment.environment", "value": { "stringValue": "Production" } }
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
              "name": "Initial Login Span",
              "startTimeUnixNano": "$start_time",
              "endTimeUnixNano": "$end_time",
              "kind": 2,
              "status": {
                "code": 1, 
                "message": "Success"
              },
              "attributes": [
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

    curl -X POST "http://localhost:4318/v1/traces" -H "Content-Type: application/json" -d "$span_json"
    echo -e "\nBase trace sent with traceId: $trace_id and spanId: $span_id"
}

# Function to send a security span
send_security_trace() {
    local trace_id=$1
    local span_id=$2
    local start_time=$3
    local end_time=$4

    local security_json=$(cat <<EOF
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          { "key": "service.name", "value": { "stringValue": "password_check" } },
          { "key": "deployment.environment", "value": { "stringValue": "security_applications" } }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "my.library",
            "version": "1.0.0"
          },
          "spans": [
            {
              "traceId": "$trace_id",
              "spanId": "$span_id",
              "parentSpanId": "$(generate_span_id)",
              "name": "password-validation",
              "startTimeUnixNano": "$start_time",
              "endTimeUnixNano": "$end_time",
              "kind": 2,
              "status": {
                "code": 1, 
                "message": "Success"
              },
              "attributes": [
               {
                  "key": "user.name",
                  "value": {
                    "stringValue": "George Lucas"
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

    curl -X POST "http://localhost:4318/v1/traces" -H "Content-Type: application/json" -d "$security_json"
    echo -e "\nSecurity trace sent with traceId: $trace_id and spanId: $span_id"
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
          { "key": "service.name", "value": { "stringValue": "frontend-service" } },
          { "key": "deployment.environment", "value": { "stringValue": "Advanced-Otel" } }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "healthz",
            "version": "1.0.0"
          },
          "spans": [
            {
              "traceId": "$trace_id",
              "spanId": "$span_id",
              "name": "/_healthz",
              "startTimeUnixNano": "$start_time",
              "endTimeUnixNano": "$end_time",
              "kind": 2,
              "status": {
                "code": 1, 
                "message": "Success"
              } 
            }
          ]
        }
      ]
    }
  ]
}
EOF
    )

    curl -X POST "http://localhost:4318/v1/traces" -H "Content-Type: application/json" -d "$health_json"
    echo -e "\nHealth trace sent with traceId: $trace_id and spanId: $span_id"
}

# Check for flags
SEND_HEALTH=false
SEND_SECURITY=false
while getopts ":hs" opt; do
  case ${opt} in
    h )
      SEND_HEALTH=true
      ;;
    s )
      SEND_SECURITY=true
      ;;
    \? )
      echo "Usage: $0 [-h] [-s] (Use -h for health span, -s for security span)"
      exit 1
      ;;
  esac
done

echo "Sending traces every 5 seconds. Use Ctrl-C to stop."

while true; do
    TRACE_ID=$(generate_trace_id)
    SPAN_ID=$(generate_span_id)
    CURRENT_TIME=$(get_current_time)
    END_TIME=$((CURRENT_TIME + 1000000000))

    send_trace "$TRACE_ID" "$SPAN_ID" "$CURRENT_TIME" "$END_TIME"

    if [ "$SEND_HEALTH" = true ]; then
        sleep 5
        send_health_trace "$TRACE_ID" "$(generate_span_id)" "$(get_current_time)" "$((CURRENT_TIME + 1000000000))"
    fi

    if [ "$SEND_SECURITY" = true ]; then
        sleep 5
        send_security_trace "$TRACE_ID" "$(generate_span_id)" "$(get_current_time)" "$((CURRENT_TIME + 1000000000))"
    fi

    sleep 5
done

