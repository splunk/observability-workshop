---
title: Zero Configuration Auto Instrumentation for Java
linkTitle: 2. Zero Configuration
weight: 2
---

## 1. Spring PetClinic Application

First thing we need to setup APM is... well, an application. For this exercise, we will use the Spring PetClinic application. This is a very popular sample java application built with Spring framework (Springboot).

Next we will clone the PetClinic repository, then we will compile, build, package and test the application.

```bash
git clone https://github.com/spring-projects/spring-petclinic
```

Change into the `spring-petclinic` directory:

```bash
cd spring-petclinic && git checkout 276880e
```

Start a MySQL database for PetClinic to use:

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/mysql:5.7.8
```

Next, run the `maven` command to compile/build/package PetClinic:

```bash
./mvnw package -Dmaven.test.skip=true
```

{{% notice title="Note" style="info" %}}
This will take a few minutes the first time you run, `maven` will download a lot of dependencies before it actually compiles the application. Future executions will be a lot shorter.
{{% /notice %}}

Once the compilation is complete, you can run the application with the following command:

```bash
java \
-Dotel.service.name=$(hostname)-petclinic-service \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

If you check the logs of the Splunk OpenTelemetry collector you will see that the collector automatically detected the application running and auto-instrumented it. You can view the logs using the following command:

```bash
sudo tail -f /var/log/syslog
```

You can validate if the application is running by visiting `http://<VM_IP_ADDRESS>:8080`.

## 2. Generating Traffic

Next we will start a Docker container running Locust that will generate some simple traffic to the PetClinic application. Locust is a simple load testing tool that can be used to generate traffic to a web application.

```bash
docker run --network="host" -d -p 8089:8089 -v /home/ubuntu/workshop/petclinic:/mnt/locust locustio/locust -f /mnt/locust/locustfile.py --headless -u 10 -r 3 -H http://127.0.0.1:8080
```

Then you can visit the Splunk APM UI and examine the application components, traces, etc. **Hamburger Menu → APM → Explore**.

Once your validation is complete you can stop the application by pressing `Ctrl-c`.

## 3. Enabling AlwaysOn Profiling and Metrics

To enable CPU and Memory Profiling on the application we can start the application by passing `splunk.profiler.enabled=true` and for metrics pass `splunk.metrics.enabled=true`. Make sure the application is stopped and run the following command to enable metrics and profiling.

```bash
java \
-Dotel.service.name=$(hostname)-petclinic-service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

You can now visit the Splunk APM UI and examine the application components, traces, profiling, DB Query performance and metrics **Hamburger Menu → APM → Explore**.

Once your validation is complete you can stop the application by pressing `Ctrl-c`.

## 4. Adding Resource Attributes to Spans

Resource attributes can be added to every reported span. For example `version=0.314`. A comma separated list of resource attributes can also be defined e.g. `key1=val1,key2=val2`.

Let's launch the PetClinic again using a new resource attribute. Note, that adding resource attributes to the run command will override what was defined when we installed the collector. So, we also need to specify our `deployment.environment` resource attribute along with our new resource attribute. Below you will see we are setting `deployment.environment=$(hostname)-petclinic` and `version=0.314`.

```bash
java \
-Dotel.service.name=$(hostname)-petclinic-service \
-Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-Dotel.resource.attributes=deployment.environment=$(hostname)-petclinic,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Back in the Splunk APM UI we can drill down on a recent trace and see the new `version` attribute in a span.
