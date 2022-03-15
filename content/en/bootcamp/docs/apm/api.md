---
title: Using OpenTelementry in Instrumentation
weight: 9
---
The business teams want to add the service version, the customer profile that is defined by a color and the name of the analyzed file.

Switch to the provided milestone `12microservices-k8s-autoi` with the instructions from "Getting Started".

Implement the requested changes to the `public-api` microservice.

The Kubernetes manifests are located in the `k8s` folder. Add the service version by [configuring the OpenTelemetry resource attributes][splunk-py-otel-cfg].

The customer profile and the file name vary by request. Create attributes and assign them to the current span with the [OpenTelemetry Python API][otel-py-api].

[splunk-py-otel-cfg]: https://github.com/signalfx/splunk-otel-python/blob/main/docs/advanced-config.md#trace-configuration

[otel-py-api]: https://opentelemetry-python.readthedocs.io/en/stable/faq-and-cookbook.html

You can use a random function to generate the customer profile (e.g. red, blue, green) with this snippet:

```python
color = random.choice(['red', 'blue', 'green'])
```

Note 1: Do not use a temporary variable to retrieve the current span. Use the `trace` directly.

Note 2: Make sure to import modules.

Rebuild the container images for the private registry:

{{< tabpane >}}
{{< tab header="Shell Command" lang="bash" >}}
docker-compose build{{< /tab >}}
{{< /tabpane >}}

Push the images to the private registry:

{{< tabpane >}}
{{< tab header="Shell Command" lang="bash" >}}
docker-compose push{{< /tab >}}
{{< /tabpane >}}

Delete the `public-api` deployment:

{{< tabpane >}}
{{< tab header="Shell Command" lang="bash" >}}
kubectl delete deploy public-api{{< /tab >}}
{{< /tabpane >}}

Redeploy to the cluster with

{{< tabpane >}}
{{< tab header="Shell Command" lang="bash" >}}
kubectl apply -f k8s{{< /tab >}}
{{< /tabpane >}}

Test the service with

{{< tabpane >}}
{{< tab header="Shell Command" lang="bash" >}}
ENDPOINT=$(kubectl get service/public-api -o jsonpath='{.spec.clusterIP}')
curl http://$ENDPOINT:8000/api -F text=@hamlet.txt{{< /tab >}}
{{< /tabpane >}}

Verify in Splunk APM that traces contain the desired informations: TODO screenshot

[Create a new indexed span tag][index-span-tag] so that the business team is able to breakdown performance per customer profile.

The milestone for this task is `13custom-instr`. It adds the described custom instrumentation.

[span-tag]: (https://docs.splunk.com/Observability/apm/span-tags/index-span-tags.html#index-a-new-span-tag)
