---
title: Deploy OpenTelemetry in Docker
weight: 9
---
You will need an access token for Splunk Observability Cloud. Set them up as environment variables:

```bash
export SPLUNK_ACCESS_TOKEN=YOURTOKEN
export SPLUNK_REALM=YOURREALM
```

Start with the [default configuration][otel-config] for the [OpenTelemetry Collector][otel-col]  and name it `collector.yaml` in the `src` directory.

You can also start with a blank configuration, which is what the milestone does for clarity.

Then run OpenTelemetry Collector with this configuration in a docker container:

{{< tabs >}}
{{% tab title="Shell Command" %}}
docker run --rm \
    -e SPLUNK_ACCESS_TOKEN=${SPLUNK_ACCESS_TOKEN} \
    -e SPLUNK_REALM=${SPLUNK_REALM} \
    -e SPLUNK_CONFIG=/etc/collector.yaml \
    -p 13133:13133 -p 14250:14250 -p 14268:14268 -p 4317:4317 \
    -p 6060:6060 -p 8888:8888 -p 9080:9080 -p 9411:9411 -p 9943:9943 \
    -v "${PWD}/collector.yaml":/etc/collector.yaml:ro \
    --name otelcol quay.io/signalfx/splunk-otel-collector:0.41.1{{% /tab %}}
{{< /tabs >}}

The milestone for this task is `03service-metrics-otel`.

[otel-config]: https://github.com/signalfx/splunk-otel-collector/blob/main/cmd/otelcol/config/collector/agent_config.yaml
[otel-col]: https://github.com/signalfx/splunk-otel-collector
