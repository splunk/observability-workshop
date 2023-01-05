---
title: Deploy PHP/Apache
linkTitle: Deploy PHP/Apache
weight: 2
---

## Create PHP/Apache Deployment YAML

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-apache
spec:
  selector:
    matchLabels:
      run: php-apache
  replicas: 1
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: registry.k8s.io/hpa-example
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: 32Mi
            cpu: 200m
          requests:
            memory: 16Mi
            cpu: 100m
---
apiVersion: v1
kind: Service
metadata:
  name: php-apache
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache
```

## Deploy PHP/Apache

``` bash
kubectl apply -f php-apache.yaml
```

## Create infinite-calls YAML

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
        - "while true; do wget -q -O- http://php-apache; done"
```

## Create infinite-calls pod

``` bash
kubectl apply -f infinite-calls.yaml
```

## Scale infinite-calls

``` bash
kubectl scale deployment/infinite-calls --replicas 4
```

## Setup HPA

Create an autoscaling deployment for CPU

``` bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=4
```

## Stop the load test

``` bash
kubectl delete -f infinite-calls.yaml
```
