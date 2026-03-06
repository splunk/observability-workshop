#!/bin/bash

# Function to generate SQL file for a given range and filename
generate_sql_file() {
    local start_id=$1
    local end_id=$2
    local outputFile=$3

    # Write the beginning of the INSERT statement (and replace file if it exists)
    echo "USE Supercars;" > "$outputFile"
    echo "" >> "$outputFile"
    echo "INSERT INTO ENQUIRIES (ENQUIRY_ID, NAME, EMAIL, COMMENT, CAR_ID, DUMMY) VALUES" >> "$outputFile"

    local car_id=$(( (RANDOM % 24) + 1 ))
    for (( i=start_id; i<=end_id; i++ ))
    do
        # Change CAR_ID every 1000 iterations
        if (( (i - start_id) % 1000 == 0 )); then
            car_id=$(( (RANDOM % 24) + 1 ))
        fi

        line="    ($i, 'Tom Smith', 'tomsmith@email.com', 'I would like to come see this car.', $car_id, 0)"
        # Add comma except for the last line
        if [ "$i" -ne "$end_id" ]; then
            line="$line,"
        else
            line="$line;"
        fi
        echo "$line" >> "$outputFile"
    done

    echo "SQL file generation complete: $outputFile"
}

generate_sql_file 1 33333 "mysql-02.sql"
generate_sql_file 33334 66666 "mysql-03.sql"
generate_sql_file 66667 99999 "mysql-04.sql"