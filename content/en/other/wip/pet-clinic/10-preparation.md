---
title: Preparation of the Pet Clinic application. 
linkTitle: 1. Preparation
weight: 10
---

## 1. Deploying the prebuild containers into kubernetes

The first thing we need to set up is... well, an application.
The first deployment of our application will be using prebuild containers to give us the base scenario: A running Java microservices based  application running in kubernetes.

So let's deploy our application:
{{< tabs >}}
{{% tab title="kubectl apply" %}}

```bash
kubectl apply -f ~/workshop/petclinic/petclinic-deploy.yaml
```

{{% /tab %}}
{{% tab title="kubectl apply Output" %}}

```text
deployment.apps/config-server created
service/config-server created
deployment.apps/discovery-server created
service/discovery-server created
deployment.apps/api-gateway created
service/api-gateway created
service/api-gateway-external created
deployment.apps/customers-service created
service/customers-service created
deployment.apps/vets-service created
service/vets-service created
deployment.apps/visits-service created
service/visits-service created
deployment.apps/admin-server created
service/admin-server created
```

{{% /tab %}}
{{< /tabs >}}

and verify the deployment:
{{< tabs >}}
{{% tab title="kubectl get pods" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="kubectl get pods Output" %}}

```text
NAME                                 READY   STATUS    RESTARTS   AGE
discovery-server-945bc74bf-fr9gb     1/1     Running   0          99s
api-gateway-84f86f677-msfhg          1/1     Running   0          99s
config-server-6878b6fb94-sbdkx       1/1     Running   0          99s
admin-server-6d4c9fddb-mg628         1/1     Running   0          99s
vets-service-64c446cc94-hs2c5        1/1     Running   0          99s
customers-service-54d7cdf699-d7gqv   1/1     Running   0          99s
visits-service-6f94679459-6s4jt      1/1     Running   0          99s
```

{{% /tab %}}
{{< /tabs >}}

Make sure the out put of get pods matches the  out put as shown above... and that all 7 services are shown as **RUNNING**.

The application will take a few minutes to start up and synchronise all the services. so let get the actual application downloaded in the mean time.

## 2. Downloading the Spring Microservices PetClinic Application

 For this exercise, we will use the Spring microservices PetClinic application. This is a very popular sample Java application built with the Spring framework (Springboot) and we are using a proper microservices version.

First, clone the PetClinic GitHub repository, as we will need this later in the workshop to compile, build, package and containerize the application:

```bash
git clone https://github.com/hagen-p/spring-petclinic-microservices.git
```

Change into the `spring-petclinic` directory:

```bash
cd spring-petclinic-microservices
```
<!--
Start a MySQL database for PetClinic to use:

```bash
docker run -d -e MYSQL_USER=petclinic -e MYSQL_PASSWORD=petclinic -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=petclinic -p 3306:3306 docker.io/mysql:5.7.8
```

Next, we will start a Docker container running Locust that will generate some simple traffic to the PetClinic application. Locust is a simple load-testing tool that can be used to generate traffic to a web application.

```bash
docker run --network="host" -d -p 8090:8090 -v ~/workshop/petclinic:/mnt/locust docker.io/locustio/locust -f /mnt/locust/locustfile.py --headless -u 1 -r 1 -H http://127.0.0.1:8083
```
-->
Next, run the script that will use the `maven` command to compile/build/package the PetClinic Micro services into local Docker containers:
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

{{% notice style="info" %}}
This will take a few minutes the first time you run, `maven` will download a lot of dependencies before it compiles the application. Future builds will be a lot quicker.
{{% /notice %}}

## 3. Check Docker Images

Once the build completes, you need to verify if the containers are indeed build:

{{< tabs >}}
{{% tab title="Check Docker Containers" %}}

```bash
docker images
```

{{% /tab %}}
{{% tab title="Docker Output" %}}

``` text

splunk@show-no-config-i-027057abec7c0c6d3:~/spring-petclinic-microservices$ docker images
REPOSITORY                                          TAG       IMAGE ID       CREATED              SIZE
quay.io/phagen/spring-petclinic-api-gateway         latest    f954254824ed   7 seconds ago        510MB
<none>                                              <none>    5dbbb7d1fbb2   9 seconds ago        563MB
quay.io/phagen/spring-petclinic-discovery-server    latest    0761e73d679d   26 seconds ago       500MB
<none>                                              <none>    d71dc0ff96f4   28 seconds ago       544MB
quay.io/phagen/spring-petclinic-config-server       latest    81a0ab6495c2   39 seconds ago       488MB
<none>                                              <none>    69d60a035bb9   40 seconds ago       519MB
quay.io/phagen/spring-petclinic-visits-service      latest    ca306495bf11   50 seconds ago       526MB
<none>                                              <none>    b60155eb8ab4   52 seconds ago       596MB
quay.io/phagen/spring-petclinic-vets-service        latest    29f1b1909b8b   About a minute ago   527MB
<none>                                              <none>    b07e8de54c99   About a minute ago   598MB
quay.io/phagen/spring-petclinic-customers-service   latest    5b21e448c91e   About a minute ago   526MB
<none>                                              <none>    722fa001614c   About a minute ago   596MB
quay.io/phagen/spring-petclinic-admin-server        latest    4a1906a91210   About a minute ago   498MB
<none>                                              <none>    96f61c7bb66a   About a minute ago   540MB
eclipse-temurin                                     17        807dd649ff14   13 days ago          407MB

```

{{% /tab %}}
{{< /tabs >}}

## 4. Check the Pet shop Website

To test the application you need to obtain the public IP address of the instance you are running on. You can do this by running the following command:

```bash
curl ifconfig.me

```

You will see an IP address returned, make a note of this as we will need it to validate that the application is running.

We also need to obtain the `INSTANCE` environment variable value, as this is what is being used as the `otel.service.name` attribute. You can do this by running the following command:

```bash
echo $INSTANCE
```

Also, make a note of this value as we will need it to filter the data in the UI.
<!-- 
2.1 Deploy the Helm Chart with the Operator enabled
To install the chart with operator in an existing cluster, make sure you have cert-manager installed and available. Both the cert-manager and operator are subcharts of this chart and can be enabled with --set certmanager.enabled=true,operator.enabled=true. These helm install commands will deploy the chart to the current namespace for this example.

# Check if a cert-manager is already installed by looking for cert-manager pods.

kubectl get pods -l app=cert-manager --all-namespaces

# If cert-manager is deployed, make sure to remove certmanager.enabled=true to the list of values to set

helm install splunk-otel-collector -f ./my_values.yaml --set operator.enabled=true,certmanager.enabled=true,environment=dev splunk-otel-collector-chart/splunk-otel-collector
2.2 Verify all the OpenTelemetry resources (collector, operator, webhook, instrumentation) are deployed successfully
Expand for kubectl commands to run and output
2.3 Instrument Application by Setting an Annotation
Depending on the variety of applications you are instrumenting, you may want to use different scopes for annotations. This step shows how to annotate namespaces and individual pods.

You can now run the application with the following command. Notice that we are passing the `mysql` profile to the application, this will tell the application to use the MySQL database we started earlier. We are also setting the `otel.service.name` to a logical service name that will also be used in the UI for filtering:

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```
-->
You can validate if the application is running by visiting `http://<IP_ADDRESS>:81` (replace `<IP_ADDRESS>` with the IP address you obtained earlier). You should see the PetClinic application running.  

<!--
## 2. AlwaysOn Profiling and Metrics

When we installed the collector we configured it to enable **AlwaysOn Profiling** and **Metrics**. This means that the collector will automatically generate CPU and Memory profiles for the application and send them to Splunk Observability Cloud.

When you start the PetClinic application you will see the collector automatically detect the application and instrument it for traces and profiling.

{{% tab title="Example output" %}}

``` text {wrap="false"}
Picked up JAVA_TOOL_OPTIONS: -javaagent:/usr/lib/splunk-instrumentation/splunk-otel-javaagent.jar -Dsplunk.profiler.enabled=true -Dsplunk.profiler.memory.enabled=true
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
[otel.javaagent 2023-06-26 13:32:04:661 +0100] [main] INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: splunk-1.25.0-otel-1.27.0
[otel.javaagent 2023-06-26 13:32:05:294 +0100] [main] INFO com.splunk.javaagent.shaded.io.micrometer.core.instrument.push.PushMeterRegistry - publishing metrics for SignalFxMeterRegistry every 30s
[otel.javaagent 2023-06-26 13:32:07:043 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2023-06-26 13:32:07:044 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - Profiler configuration:
[otel.javaagent 2023-06-26 13:32:07:047 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                  splunk.profiler.enabled : true
[otel.javaagent 2023-06-26 13:32:07:048 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -                splunk.profiler.directory : /tmp
[otel.javaagent 2023-06-26 13:32:07:049 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -       splunk.profiler.recording.duration : 20s
[otel.javaagent 2023-06-26 13:32:07:050 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -               splunk.profiler.keep-files : false
[otel.javaagent 2023-06-26 13:32:07:051 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -            splunk.profiler.logs-endpoint : null
[otel.javaagent 2023-06-26 13:32:07:053 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -              otel.exporter.otlp.endpoint : null
[otel.javaagent 2023-06-26 13:32:07:054 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -           splunk.profiler.memory.enabled : true
[otel.javaagent 2023-06-26 13:32:07:055 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -             splunk.profiler.tlab.enabled : true
[otel.javaagent 2023-06-26 13:32:07:056 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -        splunk.profiler.memory.event.rate : 150/s
[otel.javaagent 2023-06-26 13:32:07:057 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.call.stack.interval : PT10S
[otel.javaagent 2023-06-26 13:32:07:058 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -  splunk.profiler.include.internal.stacks : false
[otel.javaagent 2023-06-26 13:32:07:059 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger -      splunk.profiler.tracing.stacks.only : false
[otel.javaagent 2023-06-26 13:32:07:059 +0100] [main] INFO com.splunk.opentelemetry.profiler.ConfigurationLogger - -----------------------
[otel.javaagent 2023-06-26 13:32:07:060 +0100] [main] INFO com.splunk.opentelemetry.profiler.JfrActivator - Profiler is active.
```

{{% /tab %}}

## 3. Review Profiling Data Collection

You can now visit the Splunk APM UI and examine the application components, traces, profiling, DB Query performance and metrics. From the left-hand menu **APM** → **Explore**, click the environment dropdown and select your environment e.g. `<INSTANCE>-petclinic` (where`<INSTANCE>` is replaced with the value you noted down earlier).

![APM Environment](../images/apm-environment.png)

Once your validation is complete you can stop the application by pressing `Ctrl-c`.

## 4. Adding Resource Attributes to Spans

Resource attributes can be added to every reported span. For example `version=0.314`. A comma-separated list of resource attributes can also be defined e.g. `key1=val1,key2=val2`.

Let's launch the PetClinic again using new resource attributes. Note, that adding resource attributes to the run command will override what was defined when we installed the collector. Let's add two new resource attributes `deployment.environment=$INSTANCE-petclinic-env,version=0.314`:

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Back in the Splunk APM UI we can drill down on a recent trace and see the new `version` attribute in a span.
-->
![Pet shop](../images/petclinic.png)  
Make sure the application is working correctly by visiting the **All Owners** and **Veterinarians** tabs, you should get a list of names in each case.
