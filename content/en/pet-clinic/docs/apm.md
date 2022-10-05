---
title: Zero Configuration Java application
weight: 3
---

## Spring PetClinic Application

First thing we need to setup APM is... well, an application. For this exercise, we will use the Spring Pet Clinic application. This is a very popular sample java application built with Spring framework (Springboot).

Next we will clone the PetClinic repository, then we will compile, build, package and test the application.

```bash
git clone https://github.com/spring-projects/spring-petclinic
```

Change into the `spring-petclinic` directory:

```bash
cd spring-petclinic
```

Start a MySQL database for Pet Clinic to use:

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/mysql:5.7.8
```

Next, run the maven command to compile/build/package Pet Clinic:

```bash
./mvnw package -Dmaven.test.skip=true
```

{{% alert title="Information" %}}
This will take a few minutes the first time you run, maven will download a lot of dependencies before it actually compiles the app. Future executions will be a lot shorter.
{{% /alert %}}

Once the compilation is complete, you can run the application with the following command:

```bash
java -jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

If you check the logs of the Splunk OpenTelemetry collector you will see that the collector automatically detected the application running and auto-instrumented it. You can view the logs using the following command:

```bash
sudo tail -f /var/log/syslog
```

You can validate if the application is running by visiting `http://<VM_IP_ADDRESS>:8080`. Now generate some traffic, click around, generate errors, add visits, etc. Then you can visit the Splunk APM UI and examine the application components, traces, etc. **Hamburguer Menu → APM → Explore**.

**Once your validation is complete you can stop the application by pressing** `Ctrl-c` **.**

To enable CPU and Memory Profiling on the application we can start the application by passing `splunk.profiler.enabled=true` and for metrics pass `splunk.metrics.enabled=true`. Make sure the application is stopped and run the following command to enable metrics and profiling.

```bash
java -Dsplunk.profiler.enabled=true \
-Dsplunk.metrics.enabled=true \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Let's go visit our application again to generate some traffic `http://<VM_IP_ADDRESS>:8080`. Click around, generate errors, add visits, etc. Then you can visit the Splunk APM UI and examine the application components, traces, profiling, DB Query performance and metrics **Hamburguer Menu → APM → Explore**.
