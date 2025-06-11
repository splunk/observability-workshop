---
title: Pre-requisites
weight: 2.1
archetype: chapter
time: 90 minutes
---

### Prerequisites

- Proficiency in editing YAML files using `vi`, `vim`, `nano`, or your preferred text editor.
- Supported Environments:
  - A provided Splunk Workshop Instance (preferred). Outbound access to port `2222` is required for `ssh` access.
  - Apple Mac (Apple Silicon). Installation of `jq` is required - [**https://jqlang.org/download/**](https://jqlang.org/download/)

{{% notice title="Exercise" style="green" icon="running" %}}

**Create a workshop directory**: In your environment create a new directory (e.g. `advanced-otel-workshop`). We will refer to this directory as `[WORKSHOP]` for the remainder of the workshop.

**Download workshop binaries**: Change into your `[WORKSHOP]` directory and download the OpenTelemetry Collector, Load Generator binaries and setup script:

{{% tabs %}}
{{% tab title="Splunk Workshop Instance" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_linux_amd64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/setup-workshop.sh -o setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Apple Silicon" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v{{< otel-version >}}/otelcol_darwin_arm64 -o otelcol && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64 -o loadgen && \
curl -L https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/advanced-otel/setup-workshop.sh -o setup-workshop.sh
```

<!--
{{% notice style="warning" title="macOS Users" icon="desktop" %}}
Before running the binaries on macOS, you need to remove the quarantine attribute that macOS applies to downloaded files. This step ensures they can execute without restrictions.

Run the following command in your terminal:

```bash { title="Remove Quarantine Attribute"}
xattr -dr com.apple.quarantine otelcol && \
xattr -dr com.apple.quarantine loadgen
```

{{% /notice %}}
-->
{{% /tab %}}
{{% /tabs %}}

<!--
**Update file permissions**: Once downloaded, update the file permissions to make all files executable:

```bash
chmod +x otelcol loadgen setup-workshop.sh && \
./otelcol -v && \
./loadgen --help && \
./setup-workshop.sh
```
-->

Run the `setup-workshop.sh` script which will configure the correct permissions and also create the initial configurations for the **Agent** and the **Gateway**.

{{% tabs %}}
{{% tab title="Setup Workshop" %}}

```bash
sh setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Verify Setup" %}}

```text
███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝

Welcome to the Splunk Advanced OpenTelemetry Workshop!
======================================================

macOS detected. Removing quarantine attributes...
otelcol version v0.126.0
Usage: loadgen [OPTIONS]
Options:
  -base       Send base traces (enabled by default)
  -health     Send health traces
  -security   Send security traces
  -logs       Enable logging of random quotes to quotes.log
  -json       Output logs in JSON format (only applicable with -logs)
  -count      Number of traces or logs to send (default: infinite)
  -h, --help  Display this help message

Example:
  loadgen -health -security -count 10   Send 10 health and security traces
  loadgen -logs -json -count 5          Write 5 random quotes in JSON format to quotes.log
Creating workshop directories...
✓ Created subdirectories:
  ├── 1-agent-gateway
  ├── 2-building-resilience
  ├── 3-dropping-spans
  ├── 4-sensitive-data
  ├── 5-transform-data
  └── 6-routing-data

Creating configuration files for 1-agent-gateway...
Creating OpenTelemetry Collector agent configuration file: 1-agent-gateway/agent.yaml
✓ Configuration file created successfully: 1-agent-gateway/agent.yaml
✓ File size:     4355 bytes

Creating OpenTelemetry Collector gateway configuration file: 1-agent-gateway/gateway.yaml
✓ Configuration file created successfully: 1-agent-gateway/gateway.yaml
✓ File size:     3376 bytes

✓ Completed configuration files for 1-agent-gateway

Creating configuration files for 2-building-resilience...
Creating OpenTelemetry Collector agent configuration file: 2-building-resilience/agent.yaml
✓ Configuration file created successfully: 2-building-resilience/agent.yaml
✓ File size:     4355 bytes

Creating OpenTelemetry Collector gateway configuration file: 2-building-resilience/gateway.yaml
✓ Configuration file created successfully: 2-building-resilience/gateway.yaml
✓ File size:     3376 bytes

✓ Completed configuration files for 2-building-resilience

Workshop environment setup complete!
Configuration files created in the following directories:
  1-agent-gateway/
    ├── agent.yaml
    └── gateway.yaml
  2-building-resilience/
    ├── agent.yaml
    └── gateway.yaml
```

{{% /tab %}}
{{% /tabs %}}

```text { title="Initial Directory Structure" }
[WORKSHOP]
├── otelcol                # OpenTelemetry Collector binary
├── loadgen                # Load Generator binary
├── 1-agent-gateway        # Directories for exercises
├── 2-building-resilience
├── 3-dropping-spans
├── 4-sensitive-data
├── 5-transform-data
└── 6-routing-data
```

<!--
{{% notice note %}}
Having access to [**jq**](https://jqlang.org/download/) is recommended (installed by default on Splunk workshop instances). This lightweight command-line tool helps process and format JSON data, making it easier to inspect traces, metrics, and logs from the OpenTelemetry Collector.
{{% /notice %}}
-->
{{% /notice %}}
