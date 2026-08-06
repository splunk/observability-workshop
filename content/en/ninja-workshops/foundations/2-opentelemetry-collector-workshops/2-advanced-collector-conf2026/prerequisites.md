---
title: Prerequisites
weight: 2.1
archetype: chapter
time: 5 minutes
---

## Before you begin

Use a provided Linux workshop instance, a Linux laptop (`x86_64` or `arm64`),
or an Apple Silicon Mac. You also need `curl`, `jq`, and a text editor.

Pairing is optional. For cloud verification, sign in or
[create a free Splunk Observability Cloud organization](https://www.splunk.com/en_us/download/observability-cloud-free-edition.html).

{{% notice title="Windows and Intel Mac" style="warning" %}}
Use the provided Linux workshop instance from these computers.
{{% /notice %}}

{{% exercise title="Set up the workshop" %}}

{{< step "Create a folder" "1" >}}

```bash
mkdir advanced-otel-workshop
cd advanced-otel-workshop
```

The remaining pages refer to this folder as `[WORKSHOP]`.

{{< /step >}}

{{< step "Download the three workshop files" "2" >}}

Select the tab that matches the computer running the Collector.

{{% tabs %}}
{{% tab title="Linux x86_64" %}}

Use this tab for an `x86_64` or `amd64` Linux laptop and for the provided
workshop instance.

```bash
curl -fL https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_linux_amd64 -o otelcol
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Linux ARM64" %}}

Use this tab when `uname -m` reports `arm64` or `aarch64`.

```bash
curl -fL https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_linux_arm64 -o otelcol
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-arm64 -o loadgen
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Apple Silicon" %}}

```bash
curl -fL https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_darwin_arm64 -o otelcol
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64 -o loadgen
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% /tabs %}}

{{< /step >}}

{{< step "Run setup" "3" >}}

```bash
./setup-workshop.sh
```

Press **Enter** at the cloud-export prompt to use local validation only. Enter
`y` to also send metrics and traces to Splunk Observability Cloud; the script
then asks for your realm and ingest token.

Setup creates one Agent configuration:

```text
[WORKSHOP]
├── 1-agent
│   └── agent_config.yaml
├── loadgen
├── otelcol
├── setup-workshop.sh
└── workshop-env.sh
```

`agent_config.yaml` receives metrics, traces, and logs, processes them, and
writes local debug and file output. Cloud export is added to the same traces
and metrics pipelines when selected.

{{% expand title="Optional: where to find cloud values" %}}

Find the realm under **Settings > your user name > Organizations** and the
ingest token under **Settings > Access Tokens**. See
[View your realm](https://help.splunk.com/en/splunk-observability-cloud/administer/org-reference-info/view-your-realm-api-endpoints-and-organization)
and
[Org access tokens](https://help.splunk.com/en/splunk-observability-cloud/administer/authentication-and-security/authentication-tokens/org-access-tokens).

{{% /expand %}}

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "One Agent configuration is ready." >}}
