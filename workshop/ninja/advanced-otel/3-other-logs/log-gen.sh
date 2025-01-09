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