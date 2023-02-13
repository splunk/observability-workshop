---
title: Increase HPA Replicas
linkTitle: 7. Increase HPA Replicas
weight: 8
---

## 1. Increase the HPA replica count

Increase the `maxReplicas` to 8

``` bash
kubectl edit hpa php-apache -n apache
```

Save the changes youhave made. (Hint: Use `Esc` followed by `:wq!` to save your changes).

{{% notice title="Workshop Question" style="tip" icon="question" %}}
How many pods are now in a running state? How many are pending? Why are they pending?
{{% /notice %}}

## 2. Stop the load test

``` bash
kubectl delete -f ~/workshop/k3s/loadgen.yaml --namespace loadgen
```

{{% notice title="Workshop Question" style="tip" icon="question" %}}
After about 5 minutes, what eventually happens to the `php-apache` pods when the load test is stopped?
{{% /notice %}}
