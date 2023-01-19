---
title: Increase HPA Replicas
linkTitle: Increase HPA Replicas
weight: 8
---

## 1. Increase the HPA replica count

Increase the `maxReplicas` to 8

``` bash
kubectl edit hpa php-apache -n apache
```

{{% alert title="Workshop Question" color="danger" %}}

How many pods are now in a running state? How many are pending? Why are they pending?

{{% /alert %}}

## 2. Stop the load test

``` bash
kubectl delete -f loadgen.yaml --namespace loadgen
```

{{% alert title="Workshop Question" color="danger" %}}

What eventually happens to the php-apache pods when the load test is stopped?

{{% /alert %}}
