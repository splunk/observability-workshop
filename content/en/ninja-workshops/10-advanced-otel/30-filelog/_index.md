---
title: Filelog Receiver
linkTitle: 3. Filelog Receiver
time: 10 minutes
weight: 3
---

The `FileLog` receiver in the OpenTelemetry Collector is used to ingest logs from files. It monitors specified files for new log entries and streams those logs into the Collector for further processing or exporting. It is useful for testing and development purposes.

The Filelog receiver is not recommended for production use, as it is not optimized for performance but can be useful in a pinch. For this part of the workshop, there is script that will generate log lines in a file. The Filelog receiver will read these log lines and send them to the OpenTelemetry Collector.

### Setup

Create a new sub directory called `3-filelog` and copy the content from `2-gateway` across. Delete any `*.out` or `*.old` files.

Copy the script that matches your operating system below and create the appropriate log generation script for your operating system in the new directory (`log-gen.sh` on Mac or Linux or `log-gen.ps1` for Windows). Make sure its executable.

{{% tab title="Directory Structure after script creation" %}}

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

{{%/tab%}}


<!--{{% resources sort="asc" style="splunk" title="Log Generation Scripts" icon="scroll" /%}}-->

{{% tabs %}}
{{% tab title="log-gen.sh (Mac/Linux)" %}}

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

# Write log entries in Log4j format
generate_log_entry() {
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    LEVEL=$(get_random_log_level)
    MESSAGE=$(get_random_quote)
    echo "$TIMESTAMP [$LEVEL] - $MESSAGE"
}

# Main loop to write logsdate
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
$LogFile = "quotes.log"

# Define quotes
$LOTRQuotes = @(
    "One does not simply walk into Mordor."
    "Even the smallest person can change the course of the future."
    "All we have to decide is what to do with the time that is given us."
    "There is some good in this world, and it's worth fighting for."
)

$StarWarsQuotes = @(
    "Do or do not, there is no try."
    "The Force will be with you. Always."
    "I find your lack of faith disturbing."
    "In my experience, there is no such thing as luck."
)

# Function to get a random quote
function Get-RandomQuote {
    if ((Get-Random -Minimum 0 -Maximum 2) -eq 0) {
        $LOTRQuotes | Get-Random
    } else {
        $StarWarsQuotes | Get-Random
    }
}

# Function to generate a log entry
function Generate-LogEntry {
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogLevel = Get-Random -InputObject "INFO", "WARN", "ERROR", "DEBUG"
    $Message = Get-RandomQuote
    return "$Timestamp [$LogLevel] - $Message"
}

# Main loop to write logs
Write-Host "Writing logs to $LogFile. Press Ctrl+C to stop."
while ($true) {
    $LogEntry = Generate-LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
    Start-Sleep -Seconds 1 # Adjust this value for log frequency
}
```

{{% /tab %}}
{{% /tabs %}}

In a new terminal window we are going to use for `log-gen`, navigate to `[WORKSHOP]/3-filelog` folder and start your version of the script. It will start writing lines to a file called `./quotes.log`, and the console output a single line:

 ```txt
 Writing logs to quotes.log. Press Ctrl+C to stop.
 ```

{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
│   ├── agent.yaml          # Agent Collector configuration file
│   ├── gateway.yaml        # Gateway Collector configuration file
│   ├── log-gen.(sh or ps1) # Script to write a file with logs lines 
│   ├── quotes.log          # File containing Random log lines
│   └── trace.json          # Example trace file 
└── otelcol                 # OpenTelemetry Collector binary
```

{{%/tab%}}

Leave it running.
