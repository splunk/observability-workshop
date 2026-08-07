---
title: 5.1 Deploy the Configuration
linkTitle: 5.1 Deploy Configuration
weight: 1
---

{{% exercise title="Download and start the completed configuration" %}}

{{< step "Download the YAML" "1" >}}

In **Collector YAML**, confirm:

- `filter/health`, `attributes`, and `redaction` are connected to `traces`.
- `transform` is connected to `logs/workshop` after `resourcedetection`.
- All eight imported pipelines are present: `traces`, `metrics`,
  `metrics/internal`, `logs/signalfx`, `logs`, `logs/entities`,
  `metrics/workshop`, and `logs/workshop`.
- `metrics/internal`, `logs/signalfx`, and `logs/entities` remain unchanged.
- The retained `logs` pipeline still uses `nop`; do not add HEC credentials
  during the live lab.

Choose **Download** and save the file as `agent_config.yaml`.

{{% notice title="Keep credentials outside the YAML" style="warning" %}}
The YAML must contain environment-variable references, not token values.
{{% /notice %}}

{{< /step >}}

{{< step "Replace the running configuration" "2" >}}

Stop the Agent with `Ctrl-C`, then back up the starter file:

```bash
cd [WORKSHOP]/1-agent
test -f agent_config.start.yaml || cp agent_config.yaml agent_config.start.yaml
```

Put the downloaded file at `[WORKSHOP]/1-agent/agent_config.yaml`.

{{< tabs id="config-transfer" >}}
{{% tab title="Same computer" %}}

```bash
cp ~/Downloads/agent_config.yaml [WORKSHOP]/1-agent/agent_config.yaml
```

Replace `[WORKSHOP]` with the full workshop path.

{{% /tab %}}
{{% tab title="Splunk Show instance" %}}

Run this on your local computer after replacing `workshop-user` and
`workshop-host` with the supplied SSH details:

```bash
scp ~/Downloads/agent_config.yaml \
  workshop-user@workshop-host:~/advanced-otel-workshop/1-agent/agent_config.yaml
```

This example uses standard SSH port 22. If your facilitator supplies a
different port or copy command, use those details instead.

{{% /tab %}}
{{< /tabs >}}

Move the earlier plaintext log so the File Log receiver reads only the new JSON
test data:

```bash
test ! -f quotes.log || mv quotes.log quotes.log.before-config-builder
```

{{< /step >}}

{{< step "Restart the Agent" "3" >}}

```bash
source ../workshop-env.sh
../otelcol --config=agent_config.yaml
```

In the **Command terminal**, confirm readiness:

```bash
curl -fsS http://127.0.0.1:13133/ && echo "Collector is ready"
```

Leave the Agent running for Step 5.2.

{{% expand title="If the Agent does not start" %}}

Use the component and field named in the Collector error to correct the Config
Builder project. Download the YAML again, replace `agent_config.yaml`, and
restart the Agent. If `workshop-env.sh` is missing, rerun
`[WORKSHOP]/setup-workshop.sh`.

{{% /expand %}}

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The updated single-Agent configuration is running." >}}
