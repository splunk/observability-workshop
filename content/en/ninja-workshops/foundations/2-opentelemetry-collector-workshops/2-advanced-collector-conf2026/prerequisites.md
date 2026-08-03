---
title: Prerequisites
weight: 2.1
archetype: chapter
time: 5 minutes
---

## Prerequisites

- Proficiency in editing YAML files using `vi`, `vim`, `nano`, or your
  preferred text editor.
- `jq` is required for JSON validation exercises later in the workshop. Verify
  it with `jq --version` and, if it is missing, follow the
  [jq download instructions](https://jqlang.org/download/).
- Supported environments:
  - A provided Splunk Workshop Instance (preferred). Outbound access to port
    `2222` is required for SSH access.
  - Apple Mac with Apple Silicon.

### Values requested by the setup script

For the complete Linux workshop, have these values ready:

- Your Splunk Observability Cloud **realm** and an **ingest access token**.
  Find the realm under **Settings > your user name > Organizations** using
  [View your realm and API endpoints](https://help.splunk.com/en/splunk-observability-cloud/administer/org-reference-info/view-your-realm-api-endpoints-and-organization),
  and find or create an ingest token under **Settings > Access Tokens** using
  [Org access tokens](https://help.splunk.com/en/splunk-observability-cloud/administer/authentication-and-security/authentication-tokens/org-access-tokens).
- `SPLUNK_API_URL`. The script proposes the installer-compatible value
  `https://api.<realm>.observability.splunkcloud.com`; accept it unless your
  organization provides a different endpoint.

The script derives `SPLUNK_INGEST_URL` as
`https://ingest.<realm>.observability.splunkcloud.com` and uses
`127.0.0.1` for `SPLUNK_LISTEN_INTERFACE`, matching the default Agent behavior
of the Splunk Distribution.

`SPLUNK_HEC_TOKEN` and `SPLUNK_HEC_URL` are optional. They are for sending logs
to a Splunk Platform HTTP Event Collector, not for the core Observability Cloud
metrics and traces exercises. During the workshop, press Enter to skip both and
use the local debug/file exporters. As homework, use a HEC token and endpoint
from your own **non-production** Splunk Enterprise or Splunk Cloud Platform
instance; never use production credentials in a shared workshop.

{{% notice title="Unsupported environments" style="warning" %}}
Windows and Intel Macs are not supported by this workshop setup. Windows users
should use the provided Splunk Workshop Instance.
{{% /notice %}}

{{% notice title="Apple Silicon and local-only mode" style="note" %}}
Apple Silicon is supported for local Collector and Config Builder exercises.
The setup automatically selects local-only mode, skips the cloud and HEC
credential prompts, points those exporters at unused local ports, and records
both cloud flags as `false`. Skip Step 1.6 and all cloud-validation subsections.
Connection errors for the local placeholders can be ignored; the workshop
`debug` and `file` exporters provide the results.
{{% /notice %}}

{{% exercise title="Create the workshop directory" %}}

{{< step "Initial Setup" "1" >}}

Create a new directory and change into it:

```bash
mkdir advanced-otel-workshop && \
cd advanced-otel-workshop
```

We will refer to this directory as `[WORKSHOP]` for the remainder of the
workshop.

{{% notice title="Remove any existing OpenTelemetry Collectors" style="warning" %}}
If you completed another workshop on the provided Linux instance, ensure that
an existing Kubernetes Collector or application does not conflict with this
workshop:

```bash
helm delete splunk-otel-collector
kubectl delete ~/workshop/apm/deployment.yaml
```

These cleanup commands apply to the provided workshop instance, not macOS.
{{% /notice %}}

{{< /step >}}

{{< step "Download workshop binaries" "2" >}}

Change into `[WORKSHOP]` and download the pinned Collector, matching load
generator, and setup script:

{{% tabs %}}
{{% tab title="Splunk Workshop Instance" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_linux_amd64 -o otelcol && \
curl -L https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/loadgen/build/loadgen-linux-amd64 -o loadgen && \
curl -L https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/setup-workshop-conf2026.sh -o setup-workshop.sh && \
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Apple Silicon" %}}

```bash
curl -L https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_darwin_arm64 -o otelcol && \
curl -L https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/loadgen/build/loadgen-darwin-arm64 -o loadgen && \
curl -L https://github.com/chentaow-splunk/observability-workshop/raw/refs/heads/codex/advanced-collector-conf2026/workshop/ninja/advanced-otel/setup-workshop-conf2026.sh -o setup-workshop.sh && \
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% /tabs %}}

{{< /step >}}

{{< step "Run the setup" "3" >}}

Run the setup script:

```bash
./setup-workshop.sh
```

The script:

- Verifies Collector version `0.157.0`.
- Handles macOS quarantine attributes when running on Apple Silicon.
- On Linux, prompts for the realm and access token if they are not already
  present in `REALM` and `SPLUNK_ACCESS_TOKEN`/`ACCESS_TOKEN`.
- On Linux, prompts for `SPLUNK_API_URL` and optional Splunk HEC credentials,
  then derives `SPLUNK_INGEST_URL` and the Agent listen interface using the
  Distribution's installer defaults. Apple Silicon uses local-only values.
- Creates the single-Agent starter configuration.

It also generates `[WORKSHOP]/workshop-env.sh`. This file does **not** exist in
the GitHub repository and will not appear until `./setup-workshop.sh` completes
successfully. It is created beside `otelcol` and `loadgen`, not inside
`1-agent`, because it contains the environment variables used by every
exercise.

The resulting directory is:

```text { title="Initial Directory Structure" }
[WORKSHOP]
├── 1-agent
│   └── agent_config.yaml
├── loadgen
├── otelcol
├── setup-workshop.sh
└── workshop-env.sh
```

`workshop-env.sh` has owner-only permissions and is intentionally not part of
the repository because it can contain access tokens. Do not share or commit it.
If it is missing, return to `[WORKSHOP]`, rerun `./setup-workshop.sh`, and check
that the script reached `Workshop environment setup complete.`

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "Workshop environment is ready—onto Chapter 1: Agent Configuration." >}}
