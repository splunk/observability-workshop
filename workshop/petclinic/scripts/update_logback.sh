#!/bin/bash

xml_content='<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/base.xml"/>
    <!-- Required for Loglevel managment into the Spring Petclinic Admin Server-->
    <jmxConfigurator/>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
          <pattern>%d{HH:mm:ss.SSS} trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} %msg%n</pattern>
        </encoder> 
    </appender>

    <!-- Just wrap your logging appender, for example ConsoleAppender, with OpenTelemetryAppender -->
    <appender name="OTEL" class="io.opentelemetry.instrumentation.logback.mdc.v1_0.OpenTelemetryAppender">
      <appender-ref ref="CONSOLE"/>
    </appender>

     <!-- Use the wrapped "OTEL" appender instead of the original "CONSOLE" one -->
     <root level="INFO">
       <appender-ref ref="OTEL"/>
     </root>
</configuration>'

directory_paths=("admin-server" "api-gateway" "config-server" "customers-service" "discovery-server" "vets-service" "visits-service")

# Loop through each file and overwrite its content
for dir_path in "${directory_paths[@]}"; do
    file_path="/home/ubuntu/spring-petclinic-microservices/spring-petclinic-$dir_path/src/main/resources/logback-spring.xml"
    echo "$xml_content" > "$file_path"
    echo "Overwritten $file_path with new XML content."
done

echo "Script execution completed."