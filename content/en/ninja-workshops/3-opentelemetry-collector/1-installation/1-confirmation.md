---
title: Installing OpenTelemetry Collector Contrib
linkTitle: 1.1 Confirm Installation
weight: 1
---

## Confirm the Collector is running

The collector should now be running. We will verify this as root using `systemctl` command. To exit the status just press `q`.

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl status otelcol-contrib
```

{{% /tab %}}
{{% tab title="Status Output" %}}

``` text
● otelcol-contrib.service - OpenTelemetry Collector Contrib
     Loaded: loaded (/lib/systemd/system/otelcol-contrib.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-10-07 10:27:49 BST; 52s ago
   Main PID: 17113 (otelcol-contrib)
      Tasks: 13 (limit: 19238)
     Memory: 34.8M
        CPU: 155ms
     CGroup: /system.slice/otelcol-contrib.service
             └─17113 /usr/bin/otelcol-contrib --config=/etc/otelcol-contrib/config.yaml

Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: Descriptor:
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> Name: up
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> Description: The scraping was successful
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> Unit:
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:      -> DataType: Gauge
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: NumberDataPoints #0
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: StartTimestamp: 1970-01-01 00:00:00 +0000 UTC
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: Timestamp: 2024-10-07 09:28:36.942 +0000 UTC
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]: Value: 1.000000
Oct 07 10:28:36 petclinic-rum-testing otelcol-contrib[17113]:         {"kind": "exporter", "data_type": "metrics", "name": "debug"}
```

{{% /tab %}}
{{< /tabs >}}

Because we will be making multiple configuration file changes, setting environment variables and restarting the collector, we need to stop the collector service and disable it from starting on boot.

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
sudo systemctl stop otelcol-contrib && sudo systemctl disable otelcol-contrib
```

{{% /tab %}}
{{< /tabs >}}

---

{{% expand title="{{% badge style=primary icon=user-ninja %}}**Ninja:** Build your own collector using Open Telemetry Collector Builder (ocb){{% /badge %}}" %}}
For this part we will require the following installed on your system:

- Golang (latest version)

  ``` bash
  cd /tmp
  wget https://golang.org/dl/go1.20.linux-amd64.tar.gz
  sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz
  ```

  Edit `.profile` and add the following environment variables:

  ``` bash
  export GOROOT=/usr/local/go
  export GOPATH=$HOME/go
  export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
  ```

  Renew your shell session:
  
  ``` bash
  source ~/.profile
  ```

  Check Go version:

  ``` bash
  go version
  ```  

- ocb installed
  - Download the ocb binary from the [project releases](https://github.com/open-telemetry/opentelemetry-collector/releases/tag/cmd%2Fbuilder%2Fv0.80.0)
    and run the following commands:

    ```bash
    mv ocb_0.80.0_darwin_arm64 /usr/bin/ocb
    chmod 755 /usr/bin/ocb
    ```

    An alternative approach would be to use the golang tool chain to build the binary locally by doing:

    ```bash
    go install go.opentelemetry.io/collector/cmd/builder@v0.80.0
    mv $(go env GOPATH)/bin/builder /usr/bin/ocb
    ```

- (Optional) Docker

## Why build your own collector?

The default distribution of the collector (core and contrib) either contains too much or too little in what they have to offer.

It is also not advised to run the contrib collector in your production environments due to the amount of components installed which more than likely are not needed by your deployment.

## Benefits of building your own collector?

When creating your own collector binaries, (commonly referred to as distribution), means you build what you need.

The benefits of this are:

1. Smaller sized binaries
2. Can use existing go scanners for vulnerabilities
3. Include internal components that can tie in with your organization

## Considerations for building your collector?

Now, this would not be a 🥷 Ninja zone if it didn't come with some drawbacks:

1. Go experience is recommended if not required
1. **No** Splunk support
1. Responsibility for distribution and lifecycle management

It is important to note that the project is working towards stability but it does not mean changes made will not break your workflow. The team at Splunk provides increased support and a higher level of stability so they can provide a curated experience helping you with your deployment needs.

## The Ninja Zone

Once you have all the required tools installed to get started, you will need to create a new file named `otelcol-builder.yaml` and we will follow this directory structure:

``` bash
.
└── otelcol-builder.yaml
```

Once we have the file created, we need to add a list of components for it to install with some additional metadata.

For this example, we are going to create a builder manifest that will install only the components we need for the introduction config:

```yaml
dist:
  name: otelcol-ninja
  description: A custom build of the Open Telemetry Collector
  output_path: ./dist

extensions:
- gomod: go.opentelemetry.io/collector/extension/ballastextension v0.80.0
- gomod: go.opentelemetry.io/collector/extension/zpagesextension  v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/httpforwarder v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.80.0

exporters:
- gomod: go.opentelemetry.io/collector/exporter/loggingexporter v0.80.0
- gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/splunkhecexporter v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/signalfxexporter v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/sapmexporter v0.80.0

processors:
- gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.80.0
- gomod: go.opentelemetry.io/collector/processor/memorylimiterprocessor v0.80.0

receivers:
- gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/jaegerreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/prometheusreceiver v0.80.0
- gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/zipkinreceiver v0.80.0
```

Once the yaml file has been updated for the _ocb_, then run the following command:

```shell
ocb --config=otelcol-builder.yaml
```

Which leave you with the following directory structure:

``` text
├── dist
│   ├── components.go
│   ├── components_test.go
│   ├── go.mod
│   ├── go.sum
│   ├── main.go
│   ├── main_others.go
│   ├── main_windows.go
│   └── otelcol-ninja
└── otelcol-builder.yaml
```

### References

1. [https://opentelemetry.io/docs/collector/custom-collector/](https://opentelemetry.io/docs/collector/custom-collector/)

{{% /expand %}}

---

## Default configuration

OpenTelemetry is configured through YAML files. These files have default configurations that we can modify to meet our needs. Let's look at the default configuration that is supplied:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
cat /etc/otelcol-contrib/config.yaml
```

{{% /tab %}}
{{% tab title="config.yaml" %}}

```yaml { lineNos="table" wrap="true"}
# To limit exposure to denial of service attacks, change the host in endpoints below from 0.0.0.0 to a specific network interface.
# See https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/security-best-practices.md#safeguards-against-denial-of-service-attacks

extensions:
  health_check:
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  opencensus:
    endpoint: 0.0.0.0:55678

  # Collect own metrics
  prometheus:
    config:
      scrape_configs:
      - job_name: 'otel-collector'
        scrape_interval: 10s
        static_configs:
        - targets: ['0.0.0.0:8888']

  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_binary:
        endpoint: 0.0.0.0:6832
      thrift_compact:
        endpoint: 0.0.0.0:6831
      thrift_http:
        endpoint: 0.0.0.0:14268

  zipkin:
    endpoint: 0.0.0.0:9411

processors:
  batch:

exporters:
  debug:
    verbosity: detailed

service:

  pipelines:

    traces:
      receivers: [otlp, opencensus, jaeger, zipkin]
      processors: [batch]
      exporters: [debug]

    metrics:
      receivers: [otlp, opencensus, prometheus]
      processors: [batch]
      exporters: [debug]

    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]

  extensions: [health_check, pprof, zpages]
```

{{% /tab %}}
{{< /tabs >}}

Congratulations! You have successfully downloaded and installed the OpenTelemetry Collector. You are well on your way to becoming an OTel Ninja. But first let's walk through configuration files and different distributions of the OpenTelemetry Collector.

{{% notice style="note" %}}

Splunk does provide its own, fully supported, distribution of the OpenTelemetry Collector. This distribution is available to install from the [**Splunk GitHub Repository**](https://github.com/signalfx/splunk-otel-collector) or via a wizard in Splunk Observability Cloud that will build out a simple installation script to copy and paste. This distribution includes many additional features and enhancements that are not available in the OpenTelemetry Collector Contrib distribution.

- The Splunk Distribution of the OpenTelemetry Collector is production-tested; it is in use by the majority of customers in their production environments.
- Customers that use our distribution can receive direct help from official Splunk support within SLAs.
- Customers can use or migrate to the Splunk Distribution of the OpenTelemetry Collector without worrying about future breaking changes to its core configuration experience for metrics and traces collection (OpenTelemetry logs collection configuration is in beta). There may be breaking changes to the Collector's metrics.

{{% /notice %}}

We will now walk through each section of the configuration file and modify it to send host metrics to Splunk Observability Cloud.
