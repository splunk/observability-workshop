---
title: Fix PHP/Apache Issue
linkTitle: Fix PHP/Apache Issue
weight: 3
---

## 3. Fix PHP/Apache Deployment

Edit the YAML file

``` yaml
        resources:
          limits:
            memory: 32Mi
            cpu: "2"
          requests:
            memory: 16Mi
            cpu: "1"
```

``` bash
kubectl apply -f php-apache.yaml
```
