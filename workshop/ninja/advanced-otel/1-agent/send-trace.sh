#!/bin/bash

# Generate new traceId and spanId
TRACE_ID=$(openssl rand -hex 16 | tr '[:lower:]' '[:upper:]')
SPAN_ID=$(openssl rand -hex 8 | tr '[:lower:]' '[:upper:]')
CURRENT_TIME=$(date +%s%N)  # Current time in nanoseconds
END_TIME=$((CURRENT_TIME + 1000000000))  # Adds 1 second

# Update and send the span JSON
SPAN_JSON=$(cat <<EOF
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          { "key": "service.name", "value": { "stringValue": "my.service" } },
          { "key": "deployment.environment", "value": { "stringValue": "my.environment" } }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "my.library",
            "version": "1.0.0",
            "attributes": [
              { "key": "my.scope.attribute", "value": { "stringValue": "some scope attribute" } }
            ]
          },
          "spans": [
            {
              "traceId": "$TRACE_ID",
              "spanId": "$SPAN_ID",
              "name": "I'm a server span",
              "startTimeUnixNano": "$CURRENT_TIME",
              "endTimeUnixNano": "$END_TIME",
              "kind": 2,
              "attributes": [
                { "key": "user.name", "value": { "stringValue": "George Lucas" } }
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

# Send the updated span JSON via curl
curl -X POST "http://localhost:4318/v1/traces" \
     -H "Content-Type: application/json" \
     -d "$SPAN_JSON"

echo "Trace sent with traceId: $TRACE_ID and spanId: $SPAN_ID"
