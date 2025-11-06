---
title: Deploy Apache
linkTitle: 4. Deploy Apache
weight: 4
---

## 1. Review PHP/Apache deployment YAML

Inspect the YAML file `~/workshop/k3s/php-apache.yaml` and validate the contents using the following command:

``` bash
cat ~/workshop/k3s/php-apache.yaml
```

 This file contains the configuration for the PHP/Apache deployment and will create a new StatefulSet with a single replica of the PHP/Apache image.

A stateless application does not care which network it is using, and it does not need permanent storage. Examples of stateless apps may include web servers such as Apache, Nginx, or Tomcat.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: php-apache
spec:
  updateStrategy:
    type: RollingUpdate
  selector:
    matchLabels:
      run: php-apache
  serviceName: "php-apache-svc"
  replicas: 1
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: ghcr.io/splunk/php-apache:latest
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: "8"
            memory: "8Mi"
          requests:
            cpu: "6"
            memory: "4Mi"

---
apiVersion: v1
kind: Service
metadata:
  name: php-apache-svc
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache
```

## 2. Deploy PHP/Apache

Create an `apache` namespace then deploy the PHP/Apache application to the cluster.

Create the `apache` namespace:

``` bash
kubectl create namespace apache
```

Deploy the PHP/Apache application:

``` bash
kubectl apply -f ~/workshop/k3s/php-apache.yaml -n apache
```

Ensure the deployment has been created:

``` bash
kubectl get statefulset -n apache
```

{{% notice title="Workshop Question" style="tip" icon="question" %}}
What metrics for your Apache instance are being reported in the **Apache web servers (OTel) Navigator**?
{{% /notice %}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Using Log Observer what is the issue with the PHP/Apache deployment?

**Tip:** Adjust your filters to use: `k8s.namespace.name = apache` and `k8s.cluster.name = <your_cluster>`.
{{% /notice %}}
