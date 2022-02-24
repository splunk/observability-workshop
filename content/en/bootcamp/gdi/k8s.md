---
title: Kubernetes
weight: 21
---
The development team has started using [Kubernetes][kubernetes] for container orchestration. Switch to the provided milestone `09k8s` with the instructions from "Getting Started".

Rebuild the container images for the private registry:

```bash
docker-compose build
```

Push the images to the private registry:

```bash
docker-compose push
```

Then deploy the services into the cluster:

```bash
kubectl apply -f k8s
```

Test the service with

```bash
ENDPOINT=$(kubectl get service/wordcount -o jsonpath='{.spec.clusterIP}')
curl http://$ENDPOINT:8000/wordcount -F text=@hamlet.txt
```

Configure and install an OpenTelemetry Collector using [Splunk's helm chart][splunk-otel-helm]:

1. Review the [configuration how-to][otel-docs] and the [advanced configuration][otel-adv-cfg] to create a `values.yaml` that adds the required receivers for redis and prometheus.

1. Use the environment variables for realm,token and cluster name and pass them to `helm` as arguments.

The milestone for this task is `09k8s-otel`.

[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[splunk-otel-helm]: https://github.com/signalfx/splunk-otel-collector-chart
[otel-docs]: https://github.com/signalfx/splunk-otel-collector-chart#how-to-install
[otel-adv-cfg]: https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/advanced-configuration.md
