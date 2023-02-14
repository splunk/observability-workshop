---
title: Setup Horizontal Pod Autoscaling (HPA)
linkTitle: 6. Setup HPA
weight: 6
---

In Kubernetes, a HorizontalPodAutoscaler automatically updates a workload resource (such as a Deployment or StatefulSet), with the aim of automatically scaling the workload to match demand.

Horizontal scaling means that the response to increased load is to deploy more Pods. This is different from vertical scaling, which for Kubernetes would mean assigning more resources (for example: memory or CPU) to the Pods that are already running for the workload.

If the load decreases, and the number of Pods is above the configured minimum, the HorizontalPodAutoscaler instructs the workload resource (the Deployment, StatefulSet, or other similar resource) to scale back down.

## 1. Setup HPA

Inspect the `~/workshop/k3s/hpa.yaml` file and validate the contents using the following command:

``` bash
cat ~/workshop/k3s/hpa.yaml
```

This file contains the configuration for the Horizontal Pod Autoscaler and will create a new HPA for the `php-apache` deployment.

``` yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
  namespace: apache
spec:
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        averageUtilization: 50
        type: Utilization
  - type: Resource
    resource:
      name: memory
      target:
        averageUtilization: 75
        type: Utilization
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: php-apache
```

Once deployed, `php-apache` will autoscale when either the average CPU usage and average memory usage for the deployment goes above 75%, with a minimum of 1 pod and a maximum of 4 pods.

``` text
kubectl apply -f ~/workshop/k3s/hpa.yaml
```

## 2. Validate HPA

``` text
kubectl get hpa -n apache
```

Go to the **Workloads** or **Node Detail** tab in Kubernetes and check the HPA deployment.

{{% alert title="Workshop Question" color="success" %}}
How many additional `php-apache-x` pods have been created?
{{% /alert %}}

{{% alert title="Workshop Question" color="success" %}}
Which metrics in the Apache Dashboards have significantly increased again?
{{% /alert %}}

## 3. Increase the HPA replica count

Increase the `maxReplicas` to 8

``` bash
kubectl edit hpa php-apache -n apache
```

Save the changes youhave made. (Hint: Use `Esc` followed by `:wq!` to save your changes).

{{% alert title="Workshop Question" color="success" %}}
How many pods are now in a running state? How many are pending? Why are they pending?
{{% /alert %}}
