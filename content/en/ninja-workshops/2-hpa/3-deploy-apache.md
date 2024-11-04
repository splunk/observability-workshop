---
title: Deploying PHP/Apache
linkTitle: 3. Deploying PHP/Apache
weight: 3
---

## 1. Namespaces in Kubernetes

Most of our customers will make use of some kind of private or public cloud service to run Kubernetes. They often choose to have only a few large Kubernetes clusters as it is easier to manage centrally.

Namespaces are a way to organize these large Kubernetes clusters into virtual sub-clusters. This can be helpful when different teams or projects share a Kubernetes cluster as this will give them the easy ability to just see and work with their resources.

Any number of namespaces are supported within a cluster, each logically separated from others but with the ability to communicate with each other. Components are only **visible** when selecting a namespace or when adding the `--all-namespaces` flag to `kubectl` instead of allowing you to view just the components relevant to your project by selecting your namespace.

Most customers will want to install the applications into a separate namespace.  This workshop will follow that best practice.

## 2.  DNS and Services in Kubernetes

The Domain Name System (DNS) is a mechanism for linking various sorts of information with easy-to-remember names, such as IP addresses. Using a DNS system to translate request names into IP addresses makes it easy for end-users to reach their target domain name effortlessly.

Most Kubernetes clusters include an internal DNS service configured by default to offer a lightweight approach for service discovery. Even when Pods and Services are created, deleted, or shifted between nodes, built-in service discovery simplifies applications to identify and communicate with services on the Kubernetes clusters.

In short, the DNS system for Kubernetes will create a DNS entry for each Pod and Service. In general, a Pod has the following DNS resolution:

``` text
pod-name.my-namespace.pod.cluster-domain.example
```

For example, if a Pod in the `default` namespace has the Pod name `my_pod`, and the domain name for your cluster is `cluster.local`, then the Pod has a DNS name:

``` text
my_pod.default.pod.cluster.local
```

Any Pods exposed by a Service have the following DNS resolution available:

``` text
my_pod.service-name.my-namespace.svc.cluster-domain.example
```

More information can be found here: [**DNS for Service and Pods**](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

## 3. Review OTel receiver for PHP/Apache

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
          smartagent/apache:
            rule: type == "port" && pod.name matches "apache" && port == 80
            config:
              type: collectd/apache
              url: http://php-apache-svc.apache.svc.cluster.local/server-status?auto
              extraDimensions:
                service.name: php-apache
```

## 4.  Observation Rules in the OpenTelemetry config

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
--set="logsEngine=otel" \
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

## 5. Kubernetes ConfigMaps

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

## 6. Review PHP/Apache deployment YAML

Inspect the YAML file `~/workshop/k3s/php-apache.yaml` and validate the contents using the following command:

``` bash
cat ~/workshop/k3s/php-apache.yaml
```

 This file contains the configuration for the PHP/Apache deployment and will create a new StatefulSet with a single replica of the PHP/Apache image.

A stateless application does not care which network it is using, and it does not need permanent storage. Examples of stateless apps may include web servers such as Apache, Nginx, or Tomcat.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: php-apache
spec:
  updateStrategy:
    type: RollingUpdate
  selector:
    matchLabels:
      run: php-apache
  serviceName: "php-apache-svc"
  replicas: 1
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: ghcr.io/splunk/php-apache:latest
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: "8"
            memory: "8Mi"
          requests:
            cpu: "6"
            memory: "4Mi"

---
apiVersion: v1
kind: Service
metadata:
  name: php-apache-svc
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache
```

## 7. Deploy PHP/Apache

Create an `apache` namespace then deploy the PHP/Apache application to the cluster.

Create the `apache` namespace:

``` bash
kubectl create namespace apache
```

Deploy the PHP/Apache application:

``` bash
kubectl apply -f ~/workshop/k3s/php-apache.yaml -n apache
```

Ensure the deployment has been created:

``` bash
kubectl get statefulset -n apache
```

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What metrics for your Apache instance are being reported in the Apache Navigator?

**Tip:** Use the Navigator Sidebar and click on the service name.
{{% /notice %}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Using Log Observer what is the issue with the PHP/Apache deployment?

**Tip:** Adjust your filters to use: `object = php-apache-svc` and `k8s.cluster.name = <your_cluster>`.
{{% /notice %}}
