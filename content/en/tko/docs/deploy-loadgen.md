---
title: Deploy Load Generator
linkTitle: Deploy Load Generator
weight: 4
---

## 4. Create infinite-calls YAML

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: infinite-calls
  labels:
    app: infinite-calls
spec:
  replicas: 1
  selector:
    matchLabels:
      app: infinite-calls
  template:
    metadata:
      name: infinite-calls
      labels:
        app: infinite-calls
    spec:
      containers:
      - name: infinite-calls
        image: busybox
        command:
        - /bin/sh
        - -c
        - "while true; do wget -q -O- http://php-apache.default.svc.cluster.local; done"
```

## 5. Create infinite-calls pod

``` bash
kubectl create namespace loadgen
kubectl apply -f infinite-calls.yaml --namespace loadgen
```

## 6. Scale infinite-calls

``` bash
kubectl scale deployment/infinite-calls --replicas 4 --namespace loadgen
```
