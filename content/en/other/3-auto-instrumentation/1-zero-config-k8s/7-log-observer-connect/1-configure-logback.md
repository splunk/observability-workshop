---
title: Configuring Logback
linkTitle: 1. Configure Logback
weight: 1
---

First, clone the PetClinic GitHub repository, as we will need this later in the workshop to compile, build, package and containerize the application:

```bash
cd ~ && git clone https://github.com/hagen-p/spring-petclinic-microservices.git
```

Then change into the `spring-petclinic-microservices` directory:

```bash
cd ~/spring-petclinic-microservices
```

The Spring PetClinic application can be configured to use several different Java logging libraries. In this scenario, the application is using `logback`.  To make sure we get the OpenTelemetry information in the logs we need to update a file named `logback.xml` with the log structure and add an OpenTelemetry dependency to the `pom.xml` of each of the services in the PetClinic microservices folders.

First, let's set the Log Structure/Format. SpringBoot will allow you to set a global template, but for ease of use, we will replace the existing content of the `logback-spring.xml` files of each service with the following XML content using a prepared script.

{{% notice note %}}
The following entries will be added:

- **trace_id**
- **span_id**
- **trace_flags**
- **service.name**
- **deployment.environment**

{{% /notice %}}

These fields allow the **Splunk Observability Cloud** to display **Related Content** when using the log pattern shown below:

``` xml
<pattern>
  logback: %d{HH:mm:ss.SSS} [%thread] severity=%-5level %logger{36} - trace_id=%X{trace_id} span_id=%X{span_id} service.name=%property{otel.resource.service.name} trace_flags=%X{trace_flags} - %msg %kvp{DOUBLE}%n
</pattern>
```

The following script will update the `logback-spring.xml` for all of the services with the log structure in the format above:

{{< tabs >}}
{{% tab title="Update Logback files" %}}

``` bash
. ~/workshop/petclinic/scripts/update_logback.sh
```

{{% /tab %}}
{{% tab title="Replace Output" %}}

```text
Overwritten /home/splunk/spring-petclinic-microservices/spring-petclinic-admin-server/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/splunk/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/splunk/spring-petclinic-microservices/spring-petclinic-config-server/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/splunk/spring-petclinic-microservices/spring-petclinic-customers-service/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/splunk/spring-petclinic-microservices/spring-petclinic-discovery-server/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/splunk/spring-petclinic-microservices/spring-petclinic-vets-service/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/splunk/spring-petclinic-microservices/spring-petclinic-visits-service/src/main/resources/logback-spring.xml with new XML content.
Script execution completed.
```

{{% /tab %}}
{{< /tabs >}}

We can verify if the replacement has been successful by examining the `logback-spring.xml` file from one of the services:

{{< tabs >}}
{{% tab title="cat logback-spring.xml" %}}

``` bash
cat /home/splunk/spring-petclinic-microservices/spring-petclinic-customers-service/src/main/resources/logback-spring.xml
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
<?xml version="1.0" encoding="UTF-8"?>
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
</configuration>
```

{{% /tab %}}
{{< /tabs >}}
