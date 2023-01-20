---
title: Setup
linkTitle: Setup
weight: 1
---

## 1. Set Environment Variables

Environment Variables:

``` bash
export USERNAME=<Your-UserName>
export SPLUNK_ACCESS_TOKEN=<Your-Token>
export SPLUNK_REALM=<Your-Realm>
```

## 2. Implement Auto-Instrumentation

``` bash
cd shop
vi Dockerfile
```

Add the Otel Java Agent to Java ENTRYPOINT:

Change this:

``` bash
ENTRYPOINT java  -Dotel.resource.attributes=service.name=shop,deployment.environment=${USERNAME}_Apm_Instrumentation_Shop -jar app.jar
```

To this:

``` bash
ENTRYPOINT java -javaagent:splunk-otel-javaagent-all.jar 
-Dotel.resource.attributes=service.name=shop,deployment.environment=${USERNAME}_Apm_Instrumentation_Shop
-jar app.jar
```

See examples at:

``` bash
vi ../Dockerfiles_Instrumented
```

Repeat for: `instruments / products / stock`

## 3. Build and Deploy Application

``` bash
cd "javashop-otel directory"
./BuildAndDeploy.sh
```
