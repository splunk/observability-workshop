---
title: Deploy Load Generator
linkTitle: 6. Deploy Load Generator
weight: 6
---

Now let's apply some load against the `php-apache` pod. To do this, you will need to start a different Pod to act as a client. The container within the client Pod runs in an infinite loop, sending HTTP GETs to the `php-apache` service.

## 1. Review loadgen YAML

Inspect the YAML file `~/workshop/k3s/loadgen.yaml` and validate the contents using the following command:

``` bash
cat ~/workshop/k3s/loadgen.yaml
```

This file contains the configuration for the load generator and will create a new ReplicaSet with two replicas of the load generator image.

``` yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: loadgen
  labels:
    app: loadgen
spec:
  replicas: 2
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
```

## 2. Create a new namespace

``` text
kubectl create namespace loadgen
```

## 3. Deploy the loadgen YAML

``` text
kubectl apply -f ~/workshop/k3s/loadgen.yaml --namespace loadgen
```

Once you have deployed the load generator, you can see the Pods running in the `loadgen` namespace. Use previous similar commands to check the status of the Pods from the command line.

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Which metrics in the Apache Navigator have now significantly increased?
{{% /notice %}}

## 4. Scale the load generator

A ReplicaSet is a process that runs multiple instances of a Pod and keeps the specified number of Pods constant. Its purpose is to maintain the specified number of Pod instances running in a cluster at any given time to prevent users from losing access to their application when a Pod fails or is inaccessible.

ReplicaSet helps bring up a new instance of a Pod when the existing one fails, scale it up when the running instances are not up to the specified number, and scale down or delete Pods if another instance with the same label is created. A ReplicaSet ensures that a specified number of Pod replicas are running continuously and helps with load-balancing in case of an increase in resource usage.

Let's scale our ReplicaSet to 4 replicas using the following command:

``` text
kubectl scale replicaset/loadgen --replicas 4 -n loadgen
```

Validate the replicas are running from both the command line and Splunk Observability Cloud:

``` text
kubectl get replicaset loadgen -n loadgen
```

![ReplicaSet](../images/k8s-workload-replicaset.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What impact can you see in the Apache Navigator?
{{% /notice %}}

Let the load generator run for around 2-3 minutes and keep observing the metrics in the Kubernetes Navigator and the Apache Navigator.
