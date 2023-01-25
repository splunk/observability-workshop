---
title: Deploy Load Generator
linkTitle: Deploy Load Generator
weight: 5
---

Now to see how the autoscaler reacts to increased load. To do this, you'll start a different Pod to act as a client. The container within the client Pod runs in an infinite loop, sending queries to the php-apache service.

## 1. Create loadgen YAML

In the terminal window create a new called `loadgen.yaml` and copy the following YAML into the file:

{{< tabpane >}}
{{< tab header="loadgen.yaml" lang="yaml" >}}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: loadgen
  labels:
    app: loadgen
spec:
  replicas: 1
  selector:
    matchLabels:
      app: loadgen
  template:
    metadata:
      name: loadgen
      labels:
        app: loadgen
    spec:
      containers:
      - name: infinite-calls
        image: busybox
        command:
        - /bin/sh
        - -c
        - "while true; do wget -q -O- http://php-apache-svc.apache.svc.cluster.local; done"

{{< /tab >}}
{{< /tabpane >}}

## 2. Create a new namespace

``` text
kubectl create namespace loadgen
```

## 3. Deploy the load generator

``` text
kubectl apply -f loadgen.yaml --namespace loadgen
```

Once you have deployed the load generator, you can see the Pod running in the `loadgen` namespace. Use previous similar commands to check the status of the Pod from the command line.

{{% alert title="Workshop Question" color="success" %}}
What metrics in the Apache Dashboard have now been significantly increased?
{{% /alert %}}

## 4. Scale the load generator

A ReplicaSet is a process that runs multiple instances of a Pod and keeps the specified number of Pods constant. Its purpose is to maintain the specified number of Pod instances running in a cluster at any given time to prevent users from losing access to their application when a Pod fails or is inaccessible.

ReplicaSet helps bring up a new instance of a Pod when the existing one fails, scale it up when the running instances are not up to the specified number, and scale down or delete Pods if another instance with the same label is created. A ReplicaSet ensures that a specified number of Pod replicas are running continuously and helps with load-balancing in case of an increase in resource usage.

``` text
kubectl scale statefulset/loadgen --replicas 4 -n loadgen
```

Validate the replicas are running from both the command line and Splunk Observability Cloud:

``` text
kubectl get statefulset loadgen -n loadgen
```

{{% alert title="Workshop Question" color="success" %}}
What has happened to the Memory metric for the `php-apache-0` Pod?
{{% /alert %}}

Let the load generator run for around 2-3 minutes and keep observing the metrics in the Kubernetes Navigator and the Apache dashboard.
