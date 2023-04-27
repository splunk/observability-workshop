---
title: OpenTelemetry Collector Extensions
linkTitle: 2. Extensions
weight: 2
---

Extensions are available primarily for tasks that do not involve processing telemetry data. Examples of extensions include health monitoring, service discovery, and data forwarding. Extensions are optional.

Let's edit the `config.yaml` file to add the following extensions:

``` bash
sudo vi /etc/otelcol-contrib/config.yaml
```

```yaml
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679
```

Restart the collector:

``` bash
sudo systemctl restart otelcol-contrib
```

## Health Check

```bash
curl http://localhost:13133
```

``` text
{"status":"Server available","upSince":"2023-04-27T10:11:22.153295874+01:00","uptime":"16m24.684476004s"}
```

## Performance Profiler

## zPages

{{% notice style="tip" %}}
Install a text-based web browser (or use your local browser using the instance IP address)

``` bash
sudo apt update && sudo apt install lynx -y
```

{{% /notice %}}

**ServiceZ** gives an overview of the collector services and quick access to the pipelinez, extensionz, and featurez zPages. The page also provides build and runtime information.

Example URL: [http://localhost:55679/debug/servicez](http://localhost:55679/debug/servicez)

**PipelineZ** brings insight on the running pipelines running in the collector. You can find information on type, if data is mutated and the receivers, processors and exporters that are used for each pipeline.

Example URL: [http://localhost:55679/debug/pipelinez](http://localhost:55679/debug/pipelinez)
  
**ExtensionZ** shows the extensions that are active in the collector.

Example URL: [http://localhost:55679/debug/extensionz](http://localhost:55679/debug/extensionz)
