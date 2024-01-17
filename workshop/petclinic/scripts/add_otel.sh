#!/bin/bash

# Specify the base directory
base_directory="/home/ubuntu/spring-petclinic-microservices/"

# Specify the list of directories to navigate into
directories=("spring-petclinic-admin-server" "spring-petclinic-api-gateway" "spring-petclinic-config-server" "spring-petclinic-discovery-server" "spring-petclinic-customers-service" "spring-petclinic-vets-service" "spring-petclinic-visits-service")

# Specify the new dependencies to be added
new_dependencies="
        <dependency>
            <groupId>io.opentelemetry.instrumentation</groupId>
            <artifactId>opentelemetry-instrumentation-annotations</artifactId>
            <version>1.32.0</version>
        </dependency> 
        <dependency>
            <groupId>io.opentelemetry.instrumentation</groupId>
            <artifactId>opentelemetry-logback-mdc-1.0</artifactId>
            <version>2.0.0-alpha</version>
        </dependency>"

# Loop through the specified directories
for dir in "${directories[@]}"; do
    # Full path to the pom.xml file in the current directory
    pom_file="$base_directory/$dir/pom.xml"

    # Check if the pom.xml file exists
    if [ -e "$pom_file" ]; then
        # Create a backup copy of the original pom.xml file
        cp "$pom_file" "$pom_file.old"

        # Use awk to find the line number of <!--OpenTelemetry-->
        line_number=$(awk '/<!--OpenTelemetry-->/{print NR; exit}' "$pom_file")

        # Check if the line was found
        if [ -n "$line_number" ]; then
            # Split the pom.xml file into two temp files
            awk -v line="$line_number" 'NR <= line {print > "temp1.xml"} NR > line {print > "temp2.xml"}' "$pom_file"

            # Write the new dependencies to a third temp file
            echo "$new_dependencies" > "temp3.xml"

            # Combine the three temp files into the final pom.xml file
            cat "temp1.xml" "temp3.xml" "temp2.xml" > "$pom_file"

            # Check the exit status of the cat command
            if [ $? -eq 0 ]; then
                echo "Dependencies added successfully in $dir"
            else
                echo "Error: Failed to add dependencies in $dir"
            fi

            # Remove temporary files
            rm "temp1.xml" "temp2.xml" "temp3.xml"
        else
            echo "Error: <!--OpenTelemetry--> not found in $dir"
        fi
    else
        echo "Error: $pom_file not found in $dir"
    fi
done

echo "Dependency addition complete!"
