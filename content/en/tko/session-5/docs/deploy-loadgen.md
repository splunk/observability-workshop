---
title: Deploy Load Generator
linkTitle: Deploy Load Generator
weight: 4
---

## 1. Create infinite-calls YAML

In the terminal window create a new file using (`vim` or `nano`) called `infinite-calls.yaml` and copy the following YAML into the file.

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

## 2. Create a new namespace

``` text
kubectl create namespace loadgen
```

## 3. Deploy infinite-calls

``` text
kubectl apply -f infinite-calls.yaml --namespace loadgen
```

## 4. Scale infinite-calls

``` text
kubectl scale deployment/infinite-calls --replicas 4 -n loadgen
```
