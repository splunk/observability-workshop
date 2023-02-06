---
title: Deploy Load Generator
linkTitle: Deploy Load Generator
weight: 5
---

Now let's see how the autoscaler reacts to increased load. To do this, you'll start a different Pod to act as a client. The container within the client Pod runs in an infinite loop, sending queries to the php-apache Service.

## 1. Review loadgen YAML

Inspect the YAML file `~/workshop/k3s/loadgen.yaml` and validate the contents using the following command:

``` bash
cat ~/workshop/k3s/loadgen.yaml
```

This file contains the configuration for the load generator and will create a new StatefulSet with a single replica of the load generator image.

{{< readfile file="/workshop/k3s/loadgen.yaml" code="true" lang="yaml" >}}

## 2. Create a new namespace

``` text
kubectl create namespace loadgen
```

## 3. Deploy the loadgen YAML

``` text
kubectl apply -f ~/workshop/k3s/loadgen.yaml --namespace loadgen
```

Once you have deployed the load generator, you can see the Pod running in the `loadgen` namespace. Use previous similar commands to check the status of the Pod from the command line.

{{% alert title="Workshop Question" color="success" %}}
What metrics in the Apache Dashboard have now significantly increased?
{{% /alert %}}

## 4. Scale the load generator

A ReplicaSet is a process that runs multiple instances of a Pod and keeps the specified number of Pods constant. Its purpose is to maintain the specified number of Pod instances running in a cluster at any given time to prevent users from losing access to their application when a Pod fails or is inaccessible.

ReplicaSet helps bring up a new instance of a Pod when the existing one fails, scale it up when the running instances are not up to the specified number, and scale down or delete Pods if another instance with the same label is created. A ReplicaSet ensures that a specified number of Pod replicas are running continuously and helps with load-balancing in case of an increase in resource usage.

Let's scale our ReplicaSet to 4 replicas using the following command: 

``` text
kubectl scale statefulset/loadgen --replicas 4 -n loadgen
```

Validate the replicas are running from both the command line and Splunk Observability Cloud:

``` text
kubectl get statefulset loadgen -n loadgen
```

{{% alert title="Workshop Question" color="success" %}}
What impact did this have? Where in O11y can you see the increased replica number? Can you identify the point when you scaled?
{{% /alert %}}

Let the load generator run for around 2-3 minutes and keep observing the metrics in the Kubernetes Navigator and the Apache dashboard.
