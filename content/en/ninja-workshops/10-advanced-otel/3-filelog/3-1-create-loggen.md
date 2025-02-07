---
title: 3.1 Create Log-Gen Script
linkTitle: 3.1 Create Log-Gen Script
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

- **Create the `log-gen` script**: In the `3-filelog` directory create the script `log-gen.sh` (macOS/Linux), or `log-gen.ps1` (Windows) using the appropriate script below for your operating system:

{{% tabs %}}
{{% tab title="log-gen.sh (macOS/Linux)" %}}

```sh
#!/bin/bash

# Define the log file
LOG_FILE="quotes.log"

# Define quotes
LOTR_QUOTES=(
    "One does not simply walk into Mordor."
    "Even the smallest person can change the course of the future."
    "All we have to decide is what to do with the time that is given us."
    "There is some good in this world, and it's worth fighting for."
)

STAR_WARS_QUOTES=(
    "Do or do not, there is no try."
    "The Force will be with you. Always."
    "I find your lack of faith disturbing."
    "In my experience, there is no such thing as luck."
)

# Function to get a random quote
get_random_quote() {
    if (( RANDOM % 2 == 0 )); then
        echo "${LOTR_QUOTES[RANDOM % ${#LOTR_QUOTES[@]}]}"
    else
        echo "${STAR_WARS_QUOTES[RANDOM % ${#STAR_WARS_QUOTES[@]}]}"
    fi
}

# Function to get a random log level
get_random_log_level() {
    LOG_LEVELS=("INFO" "WARN" "ERROR" "DEBUG")
    echo "${LOG_LEVELS[RANDOM % ${#LOG_LEVELS[@]}]}"
}

# Function to generate log entry
generate_log_entry() {
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    LEVEL=$(get_random_log_level)
    MESSAGE=$(get_random_quote)
    
    if [ "$JSON_OUTPUT" = true ]; then
        echo "{\"timestamp\": \"$TIMESTAMP\", \"level\": \"$LEVEL\", \"message\": \"$MESSAGE\"}"
    else
        echo "$TIMESTAMP [$LEVEL] - $MESSAGE"
    fi
}

# Parse command line arguments
JSON_OUTPUT=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -json)
            JSON_OUTPUT=true
            ;;
    esac
    shift
done

# Main loop to write logs
echo "Writing logs to $LOG_FILE. Press Ctrl+C to stop."
while true; do
    generate_log_entry >> "$LOG_FILE"
    sleep 1 # Adjust this value for log frequency
done

```

{{% /tab %}}
{{% tab title="log-gen.ps1 (Windows)" %}}

```ps1
# Define the log file
$LOG_FILE = "quotes.log"

# Define quotes
$LOTR_QUOTES = @(
    "One does not simply walk into Mordor."
    "Even the smallest person can change the course of the future."
    "All we have to decide is what to do with the time that is given us."
    "There is some good in this world, and it's worth fighting for."
)

$STAR_WARS_QUOTES = @(
    "Do or do not, there is no try."
    "The Force will be with you. Always."
    "I find your lack of faith disturbing."
    "In my experience, there is no such thing as luck."
)

# Function to get a random quote
function Get-RandomQuote {
    if ((Get-Random -Minimum 0 -Maximum 2) -eq 0) {
        return $LOTR_QUOTES[(Get-Random -Minimum 0 -Maximum $LOTR_QUOTES.Length)]
    } else {
        return $STAR_WARS_QUOTES[(Get-Random -Minimum 0 -Maximum $STAR_WARS_QUOTES.Length)]
    }
}

# Function to get a random log level
function Get-RandomLogLevel {
    $LOG_LEVELS = @("INFO", "WARN", "ERROR", "DEBUG")
    return $LOG_LEVELS[(Get-Random -Minimum 0 -Maximum $LOG_LEVELS.Length)]
}

# Function to generate log entry
function Generate-LogEntry {
    $TIMESTAMP = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LEVEL = Get-RandomLogLevel
    $MESSAGE = Get-RandomQuote
    
    if ($JSON_OUTPUT) {
        $logEntry = @{ timestamp = $TIMESTAMP; level = $LEVEL; message = $MESSAGE } | ConvertTo-Json -Compress
    } else {
        $logEntry = "$TIMESTAMP [$LEVEL] - $MESSAGE"
    }
    return $logEntry
}

# Parse command line arguments
$JSON_OUTPUT = $false
if ($args -contains "-json") {
    $JSON_OUTPUT = $true
}

# Main loop to write logs
Write-Host "Writing logs to $LOG_FILE. Press Ctrl+C to stop."
while ($true) {
    $logEntry = Generate-LogEntry

    # Ensure UTF-8 encoding is used (without BOM) to avoid unwanted characters
    $logEntry | Out-File -Append -FilePath $LOG_FILE -Encoding utf8

    Start-Sleep -Seconds 1  # Adjust log frequency
}

```

{{% /tab %}}
{{% /tabs %}}

{{% tabs %}}
{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
│   ├── agent.yaml          # Agent Collector configuration file
│   ├── gateway.yaml        # Gateway Collector configuration file
│   ├── log-gen.(sh or ps1) # Script to write a file with logs lines 
│   └── trace.json          # Example trace file 
└── otelcol                 # OpenTelemetry Collector binary
```

{{% /tab %}}
{{% /tabs %}}

For **macOS/Linux** make sure the script is executable:

```bash
chmod +x log-gen.sh
```

{{% /notice %}}
