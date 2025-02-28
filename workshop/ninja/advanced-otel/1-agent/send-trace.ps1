# PowerShell equivalent of the Bash script to send spans to OpenTelemetry collector

# Function to generate a random trace ID
function Generate-TraceId {
  return ((1..16 | ForEach-Object { "{0:X}" -f (Get-Random -Maximum 256) }) -join '').ToUpper()
}

# Function to generate a random span ID
function Generate-SpanId {
  return ((1..8 | ForEach-Object { "{0:X}" -f (Get-Random -Maximum 256) }) -join '').ToUpper()
}

# Function to get the current timestamp in nanoseconds
function Get-CurrentTime {
  return [string]([math]::Round((Get-Date -UFormat %s) * 1000000000))
}

# Function to send a base trace
function Send-Trace {
  param(
      [string]$traceId,
      [string]$spanId,
      [string]$startTime,
      [string]$endTime
  )
  
  $spanJson = @"
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
            "traceId": "$traceId",
            "spanId": "$spanId",
            "name": "Initial Login Span",
            "startTimeUnixNano": "$startTime",
            "endTimeUnixNano": "$endTime",
            "kind": 2,
            "status": {
              "code": 1, 
              "message": "Success"
            },
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
"@

  Invoke-RestMethod -Uri "http://localhost:4318/v1/traces" -Method Post -ContentType "application/json" -Body $spanJson
  Write-Output "Base trace sent with traceId: $traceId and spanId: $spanId"
}

# Function to send a health trace
function Send-HealthTrace {
  param(
      [string]$traceId,
      [string]$spanId,
      [string]$startTime,
      [string]$endTime
  )
  
  $healthJson = @"
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
            "traceId": "$traceId",
            "spanId": "$spanId",
            "name": "/_healthz",
            "startTimeUnixNano": "$startTime",
            "endTimeUnixNano": "$endTime",
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
"@

  Invoke-RestMethod -Uri "http://localhost:4318/v1/traces" -Method Post -ContentType "application/json" -Body $healthJson
  Write-Output "Health trace sent with traceId: $traceId and spanId: $spanId"
}

# Parse command-line flags
param(
  [switch]$health,
  [switch]$security
)

Write-Output "Sending traces every 5 seconds. Use Ctrl-C to stop."

while ($true) {
  $traceId = Generate-TraceId
  $spanId = Generate-SpanId
  $currentTime = Get-CurrentTime
  $endTime = [string]([long]$currentTime + 1000000000)

  Send-Trace -traceId $traceId -spanId $spanId -startTime $currentTime -endTime $endTime

  if ($health) {
      Start-Sleep -Seconds 5
      Send-HealthTrace -traceId $traceId -spanId (Generate-SpanId) -startTime (Get-CurrentTime) -endTime ([string]([long]$currentTime + 1000000000))
  }

  Start-Sleep -Seconds 5
}