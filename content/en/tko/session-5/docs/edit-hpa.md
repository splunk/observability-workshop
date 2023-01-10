---
title: Increase HPA Replicas
linkTitle: Increase HPA Replicas
weight: 7
---

## 1. Increase the HPA replica count

Increase the replica count to 8

``` bash
kubectl edit hpa php-apache
```

## 2. Stop the load test

``` bash
kubectl delete -f loadgen.yaml --namespace loadgen
```
