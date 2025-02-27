# Generate new traceId and spanId
$traceId = -join ((65..70) + (48..57) + (97..102) | Get-Random -Count 32 | % {[char]$_}) 
$spanId = -join ((65..70) + (48..57) + (97..102) | Get-Random -Count 16 | % {[char]$_})

# Get current time in nanoseconds
$startTime = [string]([int64](([datetime]::UtcNow - (Get-Date -Date "1970-01-01T00:00:00Z")).TotalSeconds * 1000000000))
$endTime = [string]([int64]($startTime + 1000000000))  # Adds 1 second

# Construct span JSON
$spanJson = @"
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
              "traceId": "$traceId",
              "spanId": "$spanId",
              "name": "I'm a server span",
              "startTimeUnixNano": "$startTime",
              "endTimeUnixNano": "$endTime",
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
"@

# Save to a temp file
$tempFile = [System.IO.Path]::GetTempFileName()
$spanJson | Out-File -FilePath $tempFile -Encoding utf8

# Send the JSON via curl
$curlCommand = "curl -X POST `"`"http://localhost:4318/v1/traces`"`" -H `"`"Content-Type: application/json`"`" -d @$tempFile"
cmd.exe /c $curlCommand

# Cleanup temp file
Remove-Item -Path $tempFile -Force

Write-Host "Trace sent with traceId: $traceId and spanId: $spanId"