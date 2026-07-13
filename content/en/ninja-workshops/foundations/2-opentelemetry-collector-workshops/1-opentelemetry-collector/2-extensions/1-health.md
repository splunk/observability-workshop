---
title: OpenTelemetry Collector Extensions
linkTitle: 2.1 Health Check
weight: 1
---

## Health Check

Extensions are configured in the same `config.yaml` file that we referenced in the installation step. Let's edit the `config.yaml` file and configure the extensions. Note that the **pprof** and **zpages** extensions are already configured in the default `config.yaml` file. For the purpose of this workshop, we will only be updating the **health_check** extension to expose the port on all network interfaces on which we can access the health of the collector.

{{% tab title="Command" %}}

``` bash
sudo vi /etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

{{% tab title="Extensions Configuration" %}}

```yaml {hl_lines="3"}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
```

{{% /tab %}}

Start the collector:

{{% tab title="Command" %}}

``` bash
otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

This extension enables an HTTP URL that can be probed to check the status of the OpenTelemetry Collector. This extension can be used as a liveness and/or readiness probe on Kubernetes. To learn more about the `curl` command, check out the [curl man page](https://curl.se/docs/manpage.html).

Open a new terminal session and SSH into your instance to run the following command:

{{< tabs >}}
{{% tab title="curl Command" %}}

```bash
curl http://localhost:13133
```

{{% /tab %}}
{{% tab title="curl Output" %}}

``` text
{"status":"Server available","upSince":"2024-10-07T11:00:08.004685295+01:00","uptime":"12.56420005s"}
```

{{% /tab %}}
{{< /tabs >}}
