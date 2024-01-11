#!/bin/bash

xml_content='<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<configuration scan="true" scanPeriod="30 seconds">
  <contextListener class="ch.qos.logback.classic.jul.LevelChangePropagator">
      <resetJUL>true</resetJUL>
  </contextListener>
  <logger name="org.springframework.samples.petclinic" level="info"/>
  <appender name="file" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>/tmp/spring-petclinic.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>springLogFile.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>5</maxHistory>
      <totalSizeCap>1GB</totalSizeCap>
    </rollingPolicy>
    <encoder>
      <pattern>
        %d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} %n service.name=%property{otel.resource.service.name}, deployment.environment=%property{otel.resource.deployment.environment}: %m%n
      </pattern>
    </encoder>
  </appender>
  <root level="info">
    <appender-ref ref="file" />
  </root>
</configuration>'

directory_paths=("admin-server" "api-gateway" "config-server" "customers-service" "discovery-server" "vets-service" "visits-service")

# Loop through each file and overwrite its content
for dir_path in "${directory_paths[@]}"; do
    file_path="~/spring-petclinic-microservices/spring-petclinic-$dir_path/src/main/resources/logback-spring.xml"
    echo "$xml_content" > "$file_path"
    echo "Overwritten $file_path with new XML content."
done

echo "Script execution completed."