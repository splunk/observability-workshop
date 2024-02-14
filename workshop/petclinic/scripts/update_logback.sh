#!/bin/bash

xml_content='<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>
                logback: %d{HH:mm:ss.SSS} [%thread] severity=%-5level %logger{36} - trace_id=%X{trace_id} span_id=%X{span_id} service.name=%property{otel.resource.service.name} trace_flags=%X{trace_flags} - %msg %kvp{DOUBLE}%n
            </pattern>
        </encoder>
    </appender>
    <appender name="OpenTelemetry"
              class="io.opentelemetry.instrumentation.logback.appender.v1_0.OpenTelemetryAppender">
        <captureExperimentalAttributes>true</captureExperimentalAttributes>
        <captureKeyValuePairAttributes>true</captureKeyValuePairAttributes>
    </appender>
    <root level="INFO">
        <appender-ref ref="console"/>
        <appender-ref ref="OpenTelemetry"/>
    </root>
</configuration>'

directory_paths=("admin-server" "api-gateway" "config-server" "customers-service" "discovery-server" "vets-service" "visits-service")

# Loop through each file and overwrite its content
for dir_path in "${directory_paths[@]}"; do
    file_path="/home/splunk/spring-petclinic-microservices/spring-petclinic-$dir_path/src/main/resources/logback-spring.xml"
    echo "$xml_content" > "$file_path"
    echo "Overwritten $file_path with new XML content."
done

echo "Script execution completed."