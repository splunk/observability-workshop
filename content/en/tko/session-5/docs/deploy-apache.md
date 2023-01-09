---
title: Deploying PHP/Apache
linkTitle: Deploying PHP/Apache
weight: 2
---

## 1. Create PHP/Apache Deployment YAML

In the terminal window create a new file using (`vim` or `nano`) called `php-apache.yaml` and copy the following YAML into the file.

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

Save the above file and deploy the PHP/Apache application to the cluster.

``` bash
kubectl apply -f php-apache.yaml
```

After the deployment is complete verify PHP/Apache is running on the cluster. If it isn't, why isn't it? Use Splunk Observability to troubleshoot the issue.
