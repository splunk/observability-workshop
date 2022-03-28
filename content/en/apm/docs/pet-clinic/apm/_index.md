---
title: Auto-instrument Java app
weight: 3
---

### Splunk Application Performance Monitoring (APM)

#### Download and Build the Spring PetClinic App
First thing we need to setup APM is... well, an application. For this exercise, we will use the Spring Pet Clinic application. This is a very popular sample java application built with Spring framework (Springboot).

We will now clone the application repository, then we will compile, build, package and test the application.

    git clone https://github.com/spring-projects/spring-petclinic

(eventually -> https://github.com/asomensari-splunk/spring-petclinic)

then we open the directory

    cd spring-petclinic

and run the maven command to compile/build/package

    ./mvnw package -Dmaven.test.skip=true

(this might take a few minutes the first time you run, maven will download a lot of dependencies before it actually compiles the app. Future executions will be a lot shorter)

Once the compilation is complete, you can run the application with the following command:

    java -jar target/spring-petclinic-*.jar

You can validate if the application is running by visiting

    http://<VM_IP_ADDRESS>:8080 

(feel free to navigate and click around )

#### Instrument the Application With Splunk OpenTelemetry Java Libraries
Now that the application is running, it is time to setup the APM instrumentation. The Splunk APM product uses Open Telemetry libraries to instrument the applications ([https://github.com/signalfx/splunk-otel-java](https://github.com/signalfx/splunk-otel-java)).
The Otel-Java library will instrument code to generate metrics and spans/traces that are reported to the OpenTelemetry Collector.

Let's continue the process by visiting the Splunk Observability Cloud UI again.

![Hamburguer Menu](https://github.com/asomensari-splunk/spring-petclinic/blob/main/src/main/resources/static/resources/images/hamburguer.png?raw=true) (Hamburguer Menu) >> Data Setup

Then

APM Instrumentation >> Java >> Add Connection

The APM Instrumentation Wizard will show a few options for you to select, things like application name, environment, etc. In this scenario we are using:
- Application Name: petclinic
- Environment: conf21

At the end of the wizard, you'll be given a set of commands to run (similar to the Splunk IM instructions)

*(make sure you are in the spring-petclinic directory)*

    curl -L https://github.com/signalfx/splunk-otel-java/releases/latest/download/splunk-otel-javaagent-all.jar -o splunk-otel-javaagent.jar

*(this command downloads the Splunk Open Telemetry Java Instrumentation library)*

    export OTEL_SERVICE_NAME='petclinic'
    export OTEL_RESOURCE_ATTRIBUTES='deployment.environment=conf21,version=0.314'
    export OTEL_EXPORTER_OTLP_ENDPOINT='http://localhost:4317'


*(OPTIONAL: Splunk AlwaysOn Profiling: If you want to enable and test the AlwaysOn Profiling feature (currently beta), you can find details here: https://github.com/signalfx/splunk-otel-java/blob/main/profiler/README.md)*

To use the Splunk AlwaysOn Profiler you need:
1. Profiler needs to be enabled for your account (at least while the feature is under beta), contact your Splunk Observability Sales Rep/Engineer to get it configured.
2. Enable the profiler via environment property:

*(this enables profiling in the Splunk Java Otel Instrumentation Library)*


    export SPLUNK_PROFILER_ENABLED='true'




*(these commands define settings required by the instrumentation library)*

Lastly, we will run our application adding the -javaagent tag in front of the command

    java  -javaagent:./splunk-otel-javaagent.jar -jar target/spring-petclinic-*-SNAPSHOT.jar

Let's go visit our application again to generate some traffic.

    http://<VM_IP_ADDRESS>:8080 

*(click around, generate errors, add visits, etc )*

Then you can visit the APM UI and examine the application components, traces, etc

Hamburguer Menu >> APM >> Explore
