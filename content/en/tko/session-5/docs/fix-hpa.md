---
title: Fix Horizontal Pod Autoscaler Issue
linkTitle: Fix HPA Issue
weight: 7
draft: true
---

## 1. Autoscaling not working

Edit PHP/Apache YAML and reduce CPU resources further

``` text
kubectl edit deployment php-apache -n apache
```

``` yaml
resources:
  limits:
    memory: 32Mi
    cpu: "1"
  requests:
    memory: 16Mi
    cpu: "0.5"
```

``` bash
kubectl apply -f php-apache.yaml -n apache
```
