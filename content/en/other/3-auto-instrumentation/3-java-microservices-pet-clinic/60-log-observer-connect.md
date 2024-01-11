---
title: Log Observer
linkTitle: 60. Log Observer
weight: 60
---

## 1. Introduction

For the Splunk Log Observer component, we will configure the Spring PetClinic application to use an Otel Based format to write logs, This will allow the (Auto)-instrumentation to add Otel relevant information to the logs that can be used to correlate Metric, traces and logs. 

## 2. Update Logback config for the services

The Spring PetClinic application can be configured to use several different Java logging libraries. In this scenario, the application is using `logback`.  to make sure we get the otel information in the logs we just need to update a file named `logback.xml` for each of the services in the petclinc microservices folders.

Spring boot will allow you to set a global template, but for ease of use, replace the existing content  of the `logback-spring.xml` files of each service with the following XML content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
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
</configuration>
```

{{< tabs >}}
{{% tab title="Update Logback files" %}}

``` bash
. ~/workshop/petclinic/scripts/update_logback.sh
```

{{% /tab %}}
{{% tab title="Replace Output" %}}

```text
Overwritten /home/ubuntu/spring-petclinic-microservices/spring-petclinic-admin-server/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/ubuntu/spring-petclinic-microservices/spring-petclinic-api-gateway/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/ubuntu/spring-petclinic-microservices/spring-petclinic-config-server/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/ubuntu/spring-petclinic-microservices/spring-petclinic-customers-service/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/ubuntu/spring-petclinic-microservices/spring-petclinic-discovery-server/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/ubuntu/spring-petclinic-microservices/spring-petclinic-vets-service/src/main/resources/logback-spring.xml with new XML content.
Overwritten /home/ubuntu/spring-petclinic-microservices/spring-petclinic-visits-service/src/main/resources/logback-spring.xml with new XML content.
Script execution completed.
```

{{% /tab %}}
{{< /tabs >}}

We can verify if the replacement has been successful by examining the spring-logback.xml file from one of the services

```bash
cat /home/ubuntu/spring-petclinic-microservices/spring-petclinic-customers-service/src/main/resources/logback-spring.xml
```

Next, run the script that will use the `maven` command to compile/build/package the PetClinic microservices:
{{< tabs >}}
{{% tab title="Running maven" %}}

```bash
./mvnw clean install -DskipTests -P buildDocker
```

{{% /tab %}}
{{% tab title="Maven Output" %}}

```text

Successfully tagged quay.io/phagen/spring-petclinic-api-gateway:latest
[INFO] Built quay.io/phagen/spring-petclinic-api-gateway
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] 
[INFO] spring-petclinic-microservices 0.0.1 ............... SUCCESS [  0.770 s]
[INFO] spring-petclinic-admin-server ...................... SUCCESS [01:03 min]
[INFO] spring-petclinic-customers-service ................. SUCCESS [ 29.031 s]
[INFO] spring-petclinic-vets-service ...................... SUCCESS [ 22.145 s]
[INFO] spring-petclinic-visits-service .................... SUCCESS [ 20.451 s]
[INFO] spring-petclinic-config-server ..................... SUCCESS [ 12.260 s]
[INFO] spring-petclinic-discovery-server .................. SUCCESS [ 14.174 s]
[INFO] spring-petclinic-api-gateway 0.0.1 ................. SUCCESS [ 29.832 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 03:14 min
[INFO] Finished at: 2024-01-02T12:43:20Z
[INFO] ------------------------------------------------------------------------
```

{{% /tab %}}
{{< /tabs >}}

docker push localhost:5000/spring-petclinic-api-gateway:local
docker push localhost:5000/spring-petclinic-discovery-server:local
docker push localhost:5000/spring-petclinic-config-server:local
docker push localhost:5000/spring-petclinic-visits-service:local
docker push localhost:5000/spring-petclinic-vets-service:local
docker push localhost:5000/spring-petclinic-customers-service:local


{"repositories":["spring-petclinic-admin-server","spring-petclinic-api-gateway","spring-petclinic-config-server","spring-petclinic-customers-service","spring-petclinic-discovery-server","spring-petclinic-vets-service","spring-petclinic-visits-service"]}

docker images
## 4. View Logs

From the left-hand menu click on **Log Observer** and ensure **Index** is set to **splunk4rookies-workshop**.

Next, click **Add Filter** search for the field `service_name` select the value `<INSTANCE>-petclinic-service` and click `=` (include). You should now see only the log messages from your PetClinic application.

![Log Observer](../images/log-observer.png)

## 4. Summary

This is the end of the workshop and we have certainly covered a lot of ground. At this point, you should have metrics, traces (APM & RUM), logs, database query performance and code profiling being reported into Splunk Observability Cloud.

**Congratulations!**



docker system prune -a --volumes