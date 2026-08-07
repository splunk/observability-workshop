---
title: 5.1 Deploy the configuration
linkTitle: 5.1 Deploy the configuration
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
- The default `logs` pipeline still uses `splunk_hec` and
  `splunk_hec/profiling`. Do not paste HEC credentials into the YAML; the
  exporters continue to reference environment variables.

Select **Download YAML** and save the file as `agent_config.yaml`.

{{% notice title="Keep credentials outside the YAML" style="warning" %}}
The YAML must contain environment-variable references, not token values.
{{% /notice %}}

{{< /step >}}

{{< step "Replace the running configuration" "2" >}}

In the **Agent terminal**, press `Ctrl-C` to stop the agent. In the **Command
terminal**, back up the starter file:

```bash
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

Move the earlier plain-text log so the File Log receiver reads only the new JSON
test data:

```bash
test ! -f quotes.log || mv quotes.log quotes.log.before-config-builder
```

{{< /step >}}

{{< step "Restart the agent" "3" >}}

```bash
source ../workshop-env.sh
../otelcol --config=agent_config.yaml
```

In the **Command terminal**, confirm that the Collector is ready:

```bash
curl -fsS http://127.0.0.1:13133/ && echo "Collector is ready"
```

Leave the agent running for Step 5.2.

{{% expand title="If the agent does not start" %}}

Use the component and field named in the Collector error to correct the Config
Builder project. Download the YAML again, replace `agent_config.yaml`, and
restart the agent. If `workshop-env.sh` is missing, rerun
`[WORKSHOP]/setup-workshop.sh`.

{{% /expand %}}

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The updated single-agent configuration is running." >}}
