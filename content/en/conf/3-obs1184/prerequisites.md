---
title: Prerequisites
weight: 2.1
archetype: chapter
time: 5 minutes
---

## Before you begin

1. Pair up with other attendees (optional).

2. Open Splunk Observability Cloud. Choose one of these options:

   - Sign in to the Observability Workshop organization provided with your
     Splunk Show instance.
   - Register for a free Splunk Observability Cloud organization and sign in.

   **Registration:** [Register for Splunk Observability Cloud Free](https://www.splunk.com/en_us/download/observability-cloud-free-edition.html)

3. Choose one supported execution path.

   The workshop requires `bash`, `curl`, `jq`, a text editor, outbound HTTPS,
   and free local ports `2222`, `4318`, and `13133`. The Splunk Show path also
   requires `ssh` on your local computer. The `scp` command is optional and is
   needed only if you choose to transfer files manually.

   - **Splunk Show instance:** Open a terminal on your computer and connect to
     the Splunk Show instance with the supplied SSH command. Keep the supplied
     SSH command and password handy because you use them in each new terminal.
     For example, enter:

     ```bash
     ssh -p 2222 splunk@127.0.0.1
     ```

     At the prompt, enter the provided password.
   - **Linux laptop or Apple silicon Mac:** Use Terminal locally. Linux systems
     can use an `x86_64`/`amd64` or `arm64`/`aarch64` processor.

{{% notice title="Windows and Intel-based Mac computers" style="warning" %}}
Connect to a Splunk Show instance to participate in this workshop remotely.
Contact a facilitator if you need help.
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

Select the tab for the computer that runs the Collector.

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
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/loadgen/build/loadgen-linux-amd64 -o loadgen
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

Keep the supplied SSH details available for each new terminal. The guided
workshop does not require `scp`.

{{% /tab %}}
{{% tab title="Linux x86_64" %}}

Use this tab for an `x86_64` or `amd64` Linux laptop.

```bash
curl -fL https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_linux_amd64 -o otelcol
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/loadgen/build/loadgen-linux-amd64 -o loadgen
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Linux ARM64" %}}

Use this tab when `uname -m` reports `arm64` or `aarch64`.

```bash
curl -fL https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_linux_arm64 -o otelcol
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/loadgen/build/loadgen-linux-arm64 -o loadgen
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% tab title="Apple silicon" %}}

```bash
curl -fL https://github.com/signalfx/splunk-otel-collector/releases/download/v0.157.0/otelcol_darwin_arm64 -o otelcol
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/loadgen/build/loadgen-darwin-arm64 -o loadgen
curl -fL https://github.com/splunk/observability-workshop/raw/refs/heads/main/workshop/ninja/obs1184/setup-workshop-conf2026.sh -o setup-workshop.sh
chmod +x setup-workshop.sh
```

{{% /tab %}}
{{% /tabs %}}

{{< /step >}}

{{< step "Run setup" "3" >}}

```bash
./setup-workshop.sh
```

At the cloud-export prompt, press **Enter** to send metrics and traces to
Splunk Observability Cloud. To keep all workshop data local, enter `n`.
The script then asks for your realm and access token. On a Splunk Show
instance, the supplied realm appears as the default, and an access token is
already available. Press **Enter** to use each supplied value, or enter a
replacement, such as the realm and access token for your Splunk Observability
Cloud Free organization. Token characters are hidden while you type.

Setup creates one agent configuration:

```text
[WORKSHOP]
├── 1-agent
│   └── agent_config.yaml
├── loadgen
├── otelcol
├── setup-workshop.sh
└── workshop-env.sh
```

You learn about the components and pipelines in `agent_config.yaml` in Step
1.6.

{{% expand title="Optional: find your realm and access token when using your own organization" %}}

Skip this section when you are using a Splunk Show instance.

If you use your own Splunk Observability Cloud organization:

- Find the realm in the organization URL. For example, a URL containing `us1`
  uses the `us1` realm.
- Go to **Settings > Access Tokens**. Create a token or use an existing token
  that has ingest authorization.

{{% /expand %}}

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "One agent configuration is ready." >}}
