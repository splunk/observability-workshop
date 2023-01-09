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
    extensions:
      zpages:
        endpoint: 0.0.0.0:55679
```

Then upgrade the existing Splunk OpenTelemetry Collector Helm chart with the following command:

``` bash
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
```

## 2. Create PHP/Apache Deployment YAML

In the terminal window create a new file using (`vim` or `nano`) called `php-apache.yaml` and copy the following YAML into the file.

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
            memory: "4Mi"
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
