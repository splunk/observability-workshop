---
title: Deploying PHP/Apache
linkTitle: Deploying PHP/Apache
weight: 2
---

## 1. Create OpenTelemetry Collector receiver for PHP/Apache

Create a new file called `otel-apache.yaml` with the following contents:

``` yaml
agent:
  config:
    receivers:
      receiver_creator:
        receivers:
          smartagent/apache:
            rule: type == "port" && pod.name matches "apache" && port == 80
            config:
              type: collectd/apache
              url: http://php-apache.default.svc.cluster.local/server-status?auto
```

## 2.  Observation Rules in the OpenTelemetry config

The above file contains an observation rule for Apache using the OTel receiver_creator. This receiver can instantiate other receivers at runtime based on whether observed endpoints match a configured rule. The configured rules will be evaluated for each endpoint discovered. If the rule evaluates to true then the receiver for that rule will be started as configured against the matched endpoint.

In the file above we tell the OpenTelemetry agent to look for Pods that match the name "apache" and have port 80 open. Once found the agent will configure a Apache receiver to read Apache metrics from the configured url.

To use this the new apache configuration, you can upgrade the existing Splunk OpenTelemetry Collector Helm chart with the following command:

{{< tabpane >}}
{{< tab header="Helm Upgrade" lang="text" >}}
helm upgrade splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$(hostname)-k3s-cluster" \
--set="splunkObservability.logsEnabled=true" \
--set="clusterReceiver.eventsEnabled=true" \
--set="splunkObservability.infrastructureMonitoringEventsEnabled=true" \
splunk-otel-collector-chart/splunk-otel-collector \
--namespace splunk \
-f otel-apache.yaml
{{< /tab >}}
{{< tab header="Helm Upgrade Single Line" lang="bash" >}}
helm upgrade splunk-otel-collector --set="splunkObservability.realm=$REALM" --set="splunkObservability.accessToken=$ACCESS_TOKEN" --set="clusterName=$(hostname)-k3s-cluster" --set="splunkObservability.logsEnabled=true" --set="clusterReceiver.eventsEnabled=true" --set="splunkObservability.infrastructureMonitoringEventsEnabled=true" splunk-otel-collector-chart/splunk-otel-collector --namespace splunk -f otel-apache.yaml
{{< /tab >}}
{{< /tabpane >}}

## 3. Kubernetes ConfigMaps

A ConfigMap is an object in Kubernetes consisting of key-value pairs which can be injected into your application. With a ConfigMap you can separate configuration from your Pods. This way, you can prevent hardcoding configuration data. ConfigMaps are useful for storing and sharing non-sensitive, unencrypted configuration information. The OpenTelemetry collector/agent uses ConfigMaps to store the configuration of the agent and the K8s Cluster receiver. You can/will always verify the current configuration of an agent after a change by running the following commands:

``` bash
kubectl get cm -n splunk
```

Then when you have list of Configmaps from the namespace, select the one for the `splunk-otel-collector-otel-agent` and view it with the following command:

**Note** the extra flag `-o yaml`, this will print the content of the ConfigMap in a YAML format.  

``` bash
kubectl get cm splunk-otel-collector-otel-agent -n splunk -o yaml
```

Validate that content of `otel-apache.yaml` exists in the ConfigMap for the collector.

## 4. Create PHP/Apache Deployment YAML

In the terminal window create a new file called `php-apache.yaml` and copy the following YAML into the file.

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-apache
spec:
  selector:
    matchLabels:
      run: php-apache
  replicas: 1
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: rcastley/php-apache:latest
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: "16Mi"
            cpu: "8"
          requests:
            memory: "10Mi"
            cpu: "6"
---
apiVersion: v1
kind: Service
metadata:
  name: php-apache
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache
```

## 3. Deploy PHP/Apache

Save the above file and deploy the PHP/Apache application to the cluster.

``` bash
kubectl apply -f php-apache.yaml
```

After the deployment is complete verify PHP/Apache is running on the cluster. If it isn't, why isn't it? Use Splunk Observability to troubleshoot the issue.
