---
title: Setup Horizontal Pod Autoscaler
linkTitle: Setup HPA
weight: 5
---

## 7. Setup HPA

Create an autoscaling deployment for CPU

``` bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=4
```

## 8. Validate HPA

``` bash
kubectl get hpa
```
