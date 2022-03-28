---
title: Log Observer
weight: 5
---

## Splunk Log Observer (LO)

For the Splunk Log Observer component, we will configure the Spring PetClinic application to write logs to a file in the filesystem and configure the Splunk OpenTelemetry Collect to read (tail) that log file and report the information to the Splunk Observability Platform.

### Splunk Open Telemetry Collector (FluentD) Configuration

We need to configure the Splunk OpenTelemetry Collector to tail the Spring Pet Clinic log file and report the data to the Splunk Observability Cloud endpoint.

The Splunk OpenTelemetry Collector uses FluentD to consume/report logs and to configure the proper setting to report Spring PetClinic logs, we just need to add a FluentD configuration file in the default directory (/etc/otel/collector/fluentd/conf.d/).

Here's the sample FluentD configuration file (petclinic.conf, reading the file /tmp/spring-petclinic.log)

```text
<source>
  @type tail
  @label @SPLUNK
  tag petclinic.app
  path /tmp/spring-petclinic.log
  pos_file /tmp/spring-petclinic.pos_file
  read_from_head false
  <parse>
    @type none
  </parse>
</source>
```

So we need to create the file

```bash
sudo vim /etc/otel/collector/fluentd/conf.d/petclinic.conf
```

We also need to change permission and ownership of the petclinic.conf file

```bash
sudo chown td-agent:td-agent /etc/otel/collector/fluentd/conf.d/petclinic.conf
sudo chmod 755 /etc/otel/collector/fluentd/conf.d/petclinic.conf
```

And paste the contents from the snippet above. Once the file is created, we need to restart the FluentD process

```bash
sudo systemctl restart td-agent
```

### Spring Pet Clinic Logback Setting

The Spring PetClinic application can be configure to use a number of different java logging libraries. In this scenario, we are using logback. Here's a sample logback configuration file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xml>
<configuration scan="true" scanPeriod="30 seconds">
  <contextListener class="ch.qos.logback.classic.jul.LevelChangePropagator">
      <resetJUL>true</resetJUL>
  </contextListener>
  <logger name="org.springframework.samples.petclinic" level="debug"/>
  <appender name="file" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>/tmp/spring-petclinic.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>springLogFile.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>5</maxHistory>
      <totalSizeCap>1GB</totalSizeCap>
    </rollingPolicy>
    <encoder>
      <pattern>
      %d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} service.name=%property{otel.resource.service.name}, deployment.environment=%property{otel.resource.deployment.environment} %n
      </pattern>
    </encoder>
  </appender>
  <root level="debug">
    <appender-ref ref="file" />
  </root>
</configuration>
```

We just need to create a file named logback.xml in the configuration folder.

```bash
vim src/main/resources/logback.xml
```

and paste the XML content from the snippet above. After that, we need to rebuild the application and run it again:

```bash
./mvnw package -Dmaven.test.skip=true
java  -javaagent:./splunk-otel-javaagent.jar -jar target/spring-petclinic-*-SNAPSHOT.jar
```

Then let's visit the application again to generate more traffic, now we should see log messages being reported `http://<VM_IP_ADDRESS>:8080` (feel free to navigate and click around).

Then visit:
Hamburger Menu > Log Observer

And you can add a filter to select only log messages from your host and the Spring PetClinic Application:

1. Add Filter > Fields > host.name > your host name
2. Add Filter > Fields > service.name > your application name

### Summary

This the end of the exercise and we certainly covered a lot of ground. At this point you should have metrics, traces and logs being reported into your Splunk Observability account.
