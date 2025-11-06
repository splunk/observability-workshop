---
title: Apache OTel Receiver
linkTitle: 3. Apache OTel Receiver
weight: 3
---

## 1. Review OTel receiver for PHP/Apache

Inspect the YAML file `~/workshop/k3s/otel-apache.yaml` and validate the contents using the following command:

``` bash
cat ~/workshop/k3s/otel-apache.yaml
```

This file contains the configuration for the OpenTelemetry agent to monitor the PHP/Apache deployment.

```yaml
agent:
  config:
    receivers:
      receiver_creator:
        receivers:
          apache:
            rule: type == "port" && pod.name matches "apache" && port == 80
            config:
              endpoint: http://php-apache-svc.apache.svc.cluster.local/server-status?auto
```

## 2.  Observation Rules in the OpenTelemetry config

The above file contains an observation rule for Apache using the OTel `receiver_creator`. This receiver can instantiate other receivers at runtime based on whether observed endpoints match a configured rule.

The configured rules will be evaluated for each endpoint discovered. If the rule evaluates to true, then the receiver for that rule will be started as configured against the matched endpoint.

In the file above we tell the OpenTelemetry agent to look for Pods that match the name `apache` and have port `80` open. Once found, the agent will configure an Apache receiver to read Apache metrics from the configured URL. Note, the K8s DNS-based URL in the above YAML for the service.

To use the Apache configuration, you can upgrade the existing Splunk OpenTelemetry Collector Helm chart to use the `otel-apache.yaml` file with the following command:

{{< tabs >}}
{{% tab title="Helm Upgrade" %}}

``` bash
helm upgrade splunk-otel-collector \
--set="splunkObservability.realm=$REALM" \
--set="splunkObservability.accessToken=$ACCESS_TOKEN" \
--set="clusterName=$INSTANCE-k3s-cluster" \
--set="splunkPlatform.endpoint=$HEC_URL" \
--set="splunkPlatform.token=$HEC_TOKEN" \
--set="splunkPlatform.index=splunk4rookies-workshop" \
splunk-otel-collector-chart/splunk-otel-collector \
-f ~/workshop/k3s/otel-collector.yaml \
-f ~/workshop/k3s/otel-apache.yaml
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="NOTE" style="info" %}}
The **REVISION** number of the deployment has changed, which is a helpful way to keep track of your changes.

``` text
Release "splunk-otel-collector" has been upgraded. Happy Helming!
NAME: splunk-otel-collector
LAST DEPLOYED: Mon Nov  4 14:56:25 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Platform endpoint "https://http-inputs-workshop.splunkcloud.com:443/services/collector/event".

Splunk OpenTelemetry Collector is installed and configured to send data to Splunk Observability realm eu0.
```

{{% /notice %}}

## 3. Kubernetes ConfigMaps

A ConfigMap is an object in Kubernetes consisting of key-value pairs that can be injected into your application. With a ConfigMap, you can separate configuration from your Pods.

Using ConfigMap, you can prevent hardcoding configuration data. ConfigMaps are useful for storing and sharing non-sensitive, unencrypted configuration information.

The OpenTelemetry collector/agent uses ConfigMaps to store the configuration of the agent and the K8s Cluster receiver. You can/will always verify the current configuration of an agent after a change by running the following commands:

``` bash
kubectl get cm
```

{{% notice title="Workshop Question" style="tip" icon="question" %}}
How many ConfigMaps are used by the collector?
{{% /notice %}}

When you have a list of ConfigMaps from the namespace, select the one for the `otel-agent` and view it with the following command:

``` bash
kubectl get cm splunk-otel-collector-otel-agent -o yaml
```

{{% notice title="NOTE" style="info" %}}
The option `-o yaml` will output the content of the ConfigMap in a readable YAML format.
{{% /notice %}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Is the configuration from `otel-apache.yaml` visible in the ConfigMap for the collector agent?
{{% /notice %}}
