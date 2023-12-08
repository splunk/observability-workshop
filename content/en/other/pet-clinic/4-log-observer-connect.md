---
title: 4. Log Observer
weight: 4
---

## 1. Introduction

For the Splunk Log Observer component, we will configure the Spring PetClinic application to write logs to a file in the filesystem and configure the Splunk OpenTelemetry Collect to read (tail) that log file and report the information to the Splunk Observability Platform.

## 2. OpenTelemetry Filelog Configuration

We need to configure the Splunk OpenTelemetry Collector to tail the Spring PetClinic log file and report the data to the Splunk Cloud HEC URL.

The Splunk OpenTelemetry Collector uses the [Filelog Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/filelogreceiver/README.md) to consume logs. We will need to edit the collectors' configuration file:

``` bash
sudo vi /etc/otel/collector/agent_config.yaml
```

Under `receivers:` create the Filelog Receiver (make sure to indent correctly):

``` yaml {hl_lines="2-3"}
receivers:
  filelog:
    include: [/home/ubuntu/spring-petclinic.log]
```

The under the `service:` section, find the `logs:` pipeline, replace `fluentforward` with`filelog` and remove `otlp`(again, make sure to indent correctly):

``` yaml {hl_lines="2-7"}
    logs:
      receivers: [filelog]
```

Save the file and exit the editor. Next, we need to validate that the HEC Token and HEC URL are configured for the collector to use. We will inspect the `/etc/otel/collector/splunk-otel-collector.conf` file:

```bash
sudo cat /etc/otel/collector/splunk-otel-collector.conf
```

Make sure `SPLUNK_HEC_URL` and `SPLUNK_HEC_TOKEN` have values set, we can then restart the collector to apply the changes:

``` bash
sudo systemctl restart splunk-otel-collector
```

## 3. Logback Settings

The Spring PetClinic application can be configured to use several different Java logging libraries. In this scenario, we are going to use logback. We just need to create a file named `logback.xml` in the configuration folder:

```bash
vi ~/spring-petclinic/src/main/resources/logback.xml
```

Copy and paste the following XML content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<configuration scan="true" scanPeriod="30 seconds">
  <contextListener class="ch.qos.logback.classic.jul.LevelChangePropagator">
      <resetJUL>true</resetJUL>
  </contextListener>
  <logger name="org.springframework.samples.petclinic" level="info"/>
  <appender name="file" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>/home/ubuntu/spring-petclinic.log</file>
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

Now we need to rebuild the application and run it again:

```bash
./mvnw package -Dmaven.test.skip=true
```

Once the rebuild has been completed we can then run the application again:

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

## 4. View Logs

From the left-hand menu click on **Log Observer**. Click on **Index** and select **o11y-workshop-XXX.splunkcloud.com** (where **XXX** will be the realm you are running in). On the right-hand side select **petclinic-workshop** and then click **Apply**. You should see log messages being reported.

Next, click **Add Filter** search for the field `service_name` select the value `<your host name>-petclinic-service` and click `=` (include). You should now see only the log messages from your PetClinic application.

![Log Observer](../images/log-observer.png)

## 4. Summary

This is the end of the exercise and we have certainly covered a lot of ground. At this point, you should have metrics, traces (APM & RUM), logs, database query performance and code profiling being reported into Splunk Observability Cloud. **Congratulations**!
