---
title: 4. Log Observer
weight: 4
---

## 1. Introduction

For the Splunk Log Observer component, we will configure the Spring PetClinic application to write logs to a file in the filesystem and configure the Splunk OpenTelemetry Collect to read (tail) that log file and report the information to the Splunk Observability Platform.

## 2. FluentD Configuration

We need to configure the Splunk OpenTelemetry Collector to tail the Spring PetClinic log file and report the data to the Splunk Observability Cloud endpoint.

The Splunk OpenTelemetry Collector uses FluentD to consume/report logs and to configure the proper setting to report Spring PetClinic logs, we just need to add a FluentD configuration file in the default directory (`/etc/otel/collector/fluentd/conf.d/`).

So we need to create the a new FluentD configuration file:

```bash
sudo vi /etc/otel/collector/fluentd/conf.d/petclinic.conf
```

Copy and paste in the following configuration, this will read the file `/tmp/spring-petclinic.log` that will be configured in the next section.

```ini
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

We now need to change permission and ownership of the petclinic.conf file so the agent can read it:

```bash
sudo chown td-agent:td-agent /etc/otel/collector/fluentd/conf.d/petclinic.conf
sudo chmod 755 /etc/otel/collector/fluentd/conf.d/petclinic.conf
```

Now that we have created the new configuration and changed the permissions we need to restart the FluentD process:

```bash
sudo systemctl restart td-agent
```

## 3. Logback Settings

The Spring PetClinic application can be configured to use a number of different java logging libraries. In this scenario, we are using logback. We just need to create a file named `logback.xml` in the configuration folder:

```bash
vi src/main/resources/logback.xml
```

Copy and paste the following XML content:

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
        %d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} %n service.name=%property{otel.resource.service.name}, deployment.environment=%property{otel.resource.deployment.environment}: %m%n
      </pattern>
    </encoder>
  </appender>
  <root level="debug">
    <appender-ref ref="file" />
  </root>
</configuration>
```

Now we need to rebuild the application and run it again:

```bash
./mvnw package -Dmaven.test.skip=true
```

And then run the application again:

```bash
java \
-Dotel.service.name=$(hostname)-petclinic.service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-Dotel.resource.attributes=deployment.environment=$(hostname)-petclinic,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Then let's visit the application again to generate more traffic, now we should see log messages being reported `http://<VM_IP_ADDRESS>:8080` (feel free to navigate and click around).

Then visit:
Hamburger Menu > Log Observer

And you can add a filter to select only log messages from your host and the Spring PetClinic Application:

- Add Filter → Fields → `host.name` → `<your host name>`
- Add Filter → Fields → `service.name` → `<your host name>-petclinic.service`

## 4. Summary

This the end of the exercise and we have certainly covered a lot of ground. At this point you should have metrics, traces (APM & RUM), logs, database query performance and code profiling being reported into Splunk Observability Cloud. **Congratulations**!
