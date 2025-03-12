---
title: Pre-requisites
weight: 2.1
archetype: chapter
time: 90 minutes
---

### Prerequisites

- Proficiency in editing YAML files using `vi`, `vim`, `nano`, or your preferred text editor.
- Supported Environments:
  - Splunk Workshop Instance (preferred)
  - Apple Mac (Apple Silicon). Installation of `jq` is required - [**https://jqlang.org/download/**](https://jqlang.org/download/)

{{% notice title="Exercise" style="green" icon="running" %}}

**Create a workshop directory**: In your environment create a new directory (e.g., `advanced-otel`). We will refer to this directory as `[WORKSHOP]` for the remainder of the workshop.

**Download workshop binaries**: Change into your `[WORKSHOP]` directory and download the OpenTelemetry Collector and Load Generator binaries:

{{% tabs %}}
{{% tab title="Splunk Workshop Instance" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_linux_amd64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen
```

**Update file permissions**: Once downloaded, update the file permissions to make both executable:

```bash
chmod +x otelcol loadgen && \
./otelcol -v && \
./loadgen --help
```

{{% /tab %}}
{{% tab title="Apple Silicon" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_darwin_arm64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64 -o loadgen
```

{{% notice style="warning" title="macOS Users" icon="desktop" %}}
Before running the binaries on macOS, you need to remove the quarantine attribute that macOS applies to downloaded files. This step ensures they can execute without restrictions.

Run the following command in your terminal:

```bash { title="Remove Quarantine Attribute"}
xattr -dr com.apple.quarantine otelcol && \
xattr -dr com.apple.quarantine loadgen
```

**Update file permissions**: Once downloaded, update the file permissions to make both executable:

```bash
chmod +x otelcol loadgen && \
./otelcol -v && \
./loadgen --help
```

{{% /notice %}}

{{% /tab %}}
{{% /tabs %}}

```text { title="Initial Directory Structure" }
[WORKSHOP]
├── otelcol      # OpenTelemetry Collector binary
└── loadgen      # Load Generator binary
```

<!--
{{% notice note %}}
Having access to [**jq**](https://jqlang.org/download/) is recommended (installed by default on Splunk workshop instances). This lightweight command-line tool helps process and format JSON data, making it easier to inspect traces, metrics, and logs from the OpenTelemetry Collector.
{{% /notice %}}
-->
{{% /notice %}}
