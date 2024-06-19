---
title: Installing the AppDynamics Agent
linkTitle: 2. AppDynamics Agent
weight: 2
---

## 1. Introduction

## 2. Install AppDynamics Agent

- Login to the AppDynamics Controller.
- Under the **Home** menu, select **Getting Started**.
- Click **Getting Started Wizard**.
- Click **Java**.
- Ensure the **JVM** is **JDK8+**.
- Create a new application and enter application name. Please use the syntax `<initials>-petclinic-<date>` e.g. `rwc-petclinic-13-06-2024`.
- Create a new tier and enter tier name. Please use the syntax `<initials>-petclinic-tier` e.g. `rwc-petclinic-tier`.
- Enter a new Node Name. Please use the syntax `<initials>-petclinic-node` e.g. `rwc-petclinic-node`.
- Click **Continue**.
- Secure copy the zip file to your workshop instance.

    ```bash
    scp -P 2222 ~/Downloads/AppServerAgent-1.8-24.5.0.36037.zip splunk@13.40.168.134:/home/splunk
    ```

- SSH into the workshop instance.

- `mkdir appd`
- `unzip AppServerAgent-1.8-24.5.0.36037.zip -d opt/appdynamics`
- `cd ~/spring-petclinic`
- Start PetClinic with the AppDynamics agent.

    ```bash
    java \
    -Dserver.port=8081 \
    -javaagent:/home/splunk/appd/appagent/javaagent.jar \
    -Dappdynamics.agent.applicationName="rwc-petclinic-13-06-2024"\
    -Dappdynamics.agent.tierName="rwc-petclinic-tier" \
    -Dappdynamics.agent.nodeName="rwc-petclinic-node" \
    -jar target/spring-petclinic-*.jar
    ```
