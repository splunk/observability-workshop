---
title: Deploying PHP/Apache
linkTitle: Deploying PHP/Apache
weight: 2
---

## 1. Create PHP/Apache Deployment YAML

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
            memory: "16Mi"
            cpu: "8"
          requests:
            memory: "4Mi"
            cpu: "6"
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

## 2. Deploy PHP/Apache

``` bash
kubectl apply -f php-apache.yaml
```

After the deployment is complete verify PHP/Apache is running on the cluster. If it isn't, why isn't it? Use Splunk Observability to troubleshoot the issue.

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

## 7. Setup HPA

Create an autoscaling deployment for CPU

``` bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=4
```

## 8. Validate HPA

``` bash
kubectl get hpa
```

## 9. Autoscaling not working

Edit PHP/Apache YAML and reduce CPU resources further

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
kubectl apply -f php-apache.yaml
```

## 10. Increase the HPA replica count

Increase the replica count to 8

``` bash
kubectl edit hpa php-apache
```

## 11. Stop the load test

``` bash
kubectl delete -f infinite-calls.yaml --namespace loadgen
```
