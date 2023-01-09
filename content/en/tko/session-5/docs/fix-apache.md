---
title: Fix PHP/Apache Issue
linkTitle: Fix PHP/Apache Issue
weight: 3
---
## 1. Kubernetes resources


## 2. Fix PHP/Apache Deployment

To fix the PHP/Apache deployment, edit the deployment and reduce the CPU resources further.

```bash
kubectl edit deployment php-apache
```

Find the resources section and reduce the CPU limits to **2** and the CPU requests to **1** e.g.

``` yaml
resources:
  limits:
    memory: "16Mi"
    cpu: "2"
  requests:
    memory: "4Mi"
    cpu: "1"
```

Save the above changes. The deployment will be updated and the pods will be restarted. You can validate the changes have been applied by running the following command:

## 3. Validate the changes

``` bash
kubectl describe deployment php-apache
```

Validate the pod is now running in Splunk Observability Cloud.
