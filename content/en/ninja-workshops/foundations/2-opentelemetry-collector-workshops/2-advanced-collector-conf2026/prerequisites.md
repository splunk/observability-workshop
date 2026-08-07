---
title: Prerequisites
weight: 2.1
archetype: chapter
time: 5 minutes
---

## Before you begin

Use a Splunk Show instance, a Linux laptop (`x86_64` or `arm64`),
or an Apple Silicon Mac. You also need `bash`, `curl`, `jq`, a text editor,
outbound HTTPS, and free local ports `4318`, `8006`, `8888`, and `13133`.
The Splunk Show instance path also requires `ssh` and `scp` on the computer running
your browser.

Pairing is optional. For cloud verification, sign in or
[create a free Splunk Observability Cloud organization](https://www.splunk.com/en_us/download/observability-cloud-free-edition.html).

{{% notice title="Windows and Intel Mac" style="warning" %}}
Use the Splunk Show instance from these computers.
{{% /notice %}}

{{% exercise title="Set up the workshop" %}}

{{< step "Create a folder" "1" >}}

```bash
mkdir -p ~/advanced-otel-workshop
cd ~/advanced-otel-workshop
```

The remaining pages refer to this folder as `[WORKSHOP]`.

{{< /step >}}

{{< step "Get the three workshop files" "2" >}}

Select the tab that matches the computer running the Collector.

{{% tabs %}}
{{% tab title="Splunk Show instance" %}}

{{% notice title="Keep your SSH details handy" style="info" %}}
The SSH command and password for your Splunk Show instance are provided by
email or by the workshop facilitator. Keep them in a convenient, secure place.
You must use the SSH command and password each time you open a new terminal and
connect to the instance.
{{% /notice %}}

Connect to the Splunk Show instance with the supplied SSH command, then run:

```bash
cd ~/advanced-otel-workshop
curl -fL https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_linux_amd64 -o otelcol
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen
curl -fL https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

Keep the supplied SSH details available; later steps use `scp` to move the YAML
between the Splunk Show instance and the computer running your browser.

{{% /tab %}}
{{% tab title="Linux x86_64" %}}

Use this tab for an `x86_64` or `amd64` Linux laptop.

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
then asks for your realm and access token.

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

`agent_config.yaml` contains eight pipelines: the six default Agent pipelines
from the Splunk Distribution plus two workshop-specific pipelines. It retains
normal host metrics, internal Collector metrics, process-list events, entity
events, and the standard log intake path.
`metrics/workshop` and `logs/workshop` provide bounded local validation; the
retained `logs` path is ready for the HEC take-home.

{{% expand title="Optional: find your realm and access token when using your own organization" %}}

Skip this section when you are using a Splunk Show instance.

When using your own Splunk Observability Cloud organization:

- Find the realm in the organization URL. For example, a URL containing `us1`
  uses the `us1` realm.
- Go to **Settings > Access Tokens**. Create a token or use an existing token
  that has ingest authorization.

{{% /expand %}}

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "One Agent configuration is ready." >}}
