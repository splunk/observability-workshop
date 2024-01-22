---
title: Log Observer
linkTitle: 60. Log Observer
weight: 60
---

## 1. Introduction

For the Splunk Log Observer component, we will configure the Spring PetClinic application to use an Otel Based format to write logs, This will allow the (Auto)-instrumentation to add Otel relevant information to the logs that can be used to correlate Metric, traces and logs. 

## 2. Update Logback config for the services

The Spring PetClinic application can be configured to use several different Java logging libraries. In this scenario, the application is using `logback`.  to make sure we get the otel information in the logs we just need to update a file named `logback.xml` for each of the services in the petclinc microservices folders.

Spring boot will allow you to set a global template, but for ease of use,  we will replace the existing content of the `logback-spring.xml` files of each service with the following XML content using a prepared script:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/base.xml"/>
    <!-- Required for Loglevel managment into the Spring Petclinic Admin Server-->
    <jmxConfigurator/>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
          <pattern>
            %d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} %n service.name=%property{otel.resource.service.name}, deployment.environment=%property{otel.resource.deployment.environment}: %m%n
          </pattern>
        </encoder> 
    </appender>

    <!-- Just wrap your logging appender, for example ConsoleAppender, with OpenTelemetryAppender -->
    <appender name="OTEL" class="io.opentelemetry.instrumentation.logback.mdc.v1_0.OpenTelemetryAppender">
      <appender-ref ref="CONSOLE"/>
    </appender>

     <!-- Use the wrapped "OTEL" appender instead of the original "CONSOLE" one -->
     <root level="INFO">
       <appender-ref ref="OTEL"/>
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

## 3. Recompile and store the services locally

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

Next, run the script that will push the newly build containers into our local repository:

{{< tabs >}}
{{% tab title="pushing Containers" %}}

```bash
. ~/workshop/petclinic/scripts/push_docker.sh 
```

{{% /tab %}}
{{% tab title="Docker Push Output (partial)" %}}

```text
The push refers to repository [localhost:5000/spring-petclinic-vets-service]
0391386bcb2a: Preparing 
bbb67f51a186: Preparing 
105351d0ada3: Preparing 
49cfeae6cb9f: Preparing 
b4da5101fcde: Preparing 
49cfeae6cb9f: Pushed 
e742c14be110: Mounted from spring-petclinic-visits-service 
540aa741fede: Mounted from spring-petclinic-visits-service 
a1dfe59d4939: Mounted from spring-petclinic-visits-service 
1e99e92c46bf: Mounted from spring-petclinic-visits-service 
f5aa38537736: Mounted from spring-petclinic-visits-service 
d2210512edb4: Mounted from spring-petclinic-visits-service 
8e87ff28f1b5: Mounted from spring-petclinic-visits-service 
local: digest: sha256:42337b2a4ff7d0ac9b7c2cf3c70aa20b7b52d092f1e05d351e031dd7fad956fc size: 3040
The push refers to repository [localhost:5000/spring-petclinic-customers-service]
15d54d9adca8: Preparing 
886f6def5b35: Preparing 
1575ae90e858: Preparing 
ccc884d92d18: Preparing 
b4da5101fcde: Preparing 
ccc884d92d18: Pushed 
e742c14be110: Mounted from spring-petclinic-vets-service 
540aa741fede: Mounted from spring-petclinic-vets-service 
a1dfe59d4939: Mounted from spring-petclinic-vets-service 
1e99e92c46bf: Mounted from spring-petclinic-vets-service 
f5aa38537736: Mounted from spring-petclinic-vets-service 
d2210512edb4: Mounted from spring-petclinic-vets-service 
8e87ff28f1b5: Mounted from spring-petclinic-vets-service 
local: digest: sha256:3601c6e7f58224001946058fb0400483fbb8f1b0ea8a6dbaf403c62b4c1908be size: 3042
```

{{% /tab %}}
{{< /tabs >}}

The containers should now be stored in the local repository, lets confirm by checking the catalog,

```bash
 curl -X GET http://localhost:5000/v2/_catalog 
```

The result should be :

```text
{"repositories":["spring-petclinic-admin-server","spring-petclinic-api-gateway","spring-petclinic-config-server","spring-petclinic-customers-service","spring-petclinic-discovery-server","spring-petclinic-vets-service","spring-petclinic-visits-service"]}
```

## 5. Deploy new services to kubernetes

To see the changes in effect, we need to redeploy the services, by applying the local version of the deployment yaml.

```bash
kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
```
this will cause the containers to be replaced with the local version, you can verify this by chcking the continers

## 6. View Logs

From the left-hand menu click on **Log Observer** and ensure **Index** is set to **splunk4rookies-workshop**.

Next, click **Add Filter** search for the field `service_name` select the value `<INSTANCE>-petclinic-service` and click `=` (include). You should now see only the log messages from your PetClinic application.

![Log Observer](../images/log-observer.png)

## 7. Summary

This is the end of the workshop and we have certainly covered a lot of ground. At this point, you should have metrics, traces (APM & RUM), logs, database query performance and code profiling being reported into Splunk Observability Cloud.

**Congratulations!**



docker system prune -a --volumes


  81  . ~/workshop/petclinic/scripts/add_otel.sh
   82  . ~/workshop/petclinic/scripts/update_logback.sh
   83  ./mvnw clean install -DskipTests -P buildDocker
   84  . ~/workshop/petclinic/scripts/push_docker.sh
   85  . ~/workshop/petclinic/scripts/set_local.sh
   86  kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
   87  k9s
   88  kubectl delete -f ~/workshop/petclinic/petclinic-local.yaml
   89  kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
   90  k9s
   91  kubectl delete -f ~/workshop/petclinic/petclinic-local.yaml
   92  kubectl apply -f ~/workshop/petclinic/petclinic-local.yaml
   93  k9s
   94  kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"true\"}}}}}"