#!/bin/bash

# '<?xml version="1.0" encoding="UTF-8"?>
# <configuration>
#     <include resource="org/springframework/boot/logging/logback/base.xml"/>
#     <!-- Required for Loglevel managment into the Spring Petclinic Admin Server-->
#     <jmxConfigurator/>
#     <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
#         <encoder>
#           <pattern>
#             %d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} %n service.name=%property{otel.resource.service.name}, deployment.environment=%property{otel.resource.deployment.environment}: %m%n
#           </pattern>
#         </encoder> 
#     </appender>

#     <!-- Just wrap your logging appender, for example ConsoleAppender, with OpenTelemetryAppender -->
#     <appender name="OTEL" class="io.opentelemetry.instrumentation.logback.mdc.v1_0.OpenTelemetryAppender">
#       <appender-ref ref="CONSOLE"/>
#     </appender>

#      <!-- Use the wrapped "OTEL" appender instead of the original "CONSOLE" one -->
#      <root level="INFO">
#        <appender-ref ref="OTEL"/>
#      </root>
# </configuration>'


xml_content='<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>
                logback: %d{HH:mm:ss.SSS} [%thread] %level %logger{36} - trace_id=%X{trace_id} span_id=%X{span_id} service.name=%property{otel.resource.service.name} trace_flags=%X{trace_flags} - %msg %kvp{DOUBLE}%n
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
    file_path="/home/ubuntu/spring-petclinic-microservices/spring-petclinic-$dir_path/src/main/resources/logback-spring.xml"
    echo "$xml_content" > "$file_path"
    echo "Overwritten $file_path with new XML content."
done

echo "Script execution completed."