---
title: Deploy Load Generator
linkTitle: Deploy Load Generator
weight: 4
---

## 1. Create loadgen YAML

In the terminal window create a new file using (`vim` or `nano`) called `loadgen.yaml` and copy the following YAML into the file.

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loadgen
  labels:
    app: loadgen
spec:
  replicas: 1
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
        - "while true; do wget -q -O- http://php-apache.apache.svc.cluster.local; done"
```

## 2. Create a new namespace

``` text
kubectl create namespace loadgen
```

## 3. Deploy the load generator

``` text
kubectl apply -f loadgen.yaml --namespace loadgen
```

## 4. Scale the load generator

``` text
kubectl scale deployment/loadgen --replicas 4 -n loadgen
```
