---
title: Setup Horizontal Pod Autoscaler
linkTitle: Setup HPA
weight: 5
---

## 1. Setup HPA

Create an autoscaling deployment for CPU

``` text
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=4
```

## 2. Validate HPA

``` text
kubectl get hpa
```
