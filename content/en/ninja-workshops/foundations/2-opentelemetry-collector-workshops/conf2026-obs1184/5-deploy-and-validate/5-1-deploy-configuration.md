---
title: 5.1 Deploy the configuration
linkTitle: 5.1 Deploy the configuration
weight: 1
time: 3 minutes
---

{{% exercise title="Start the completed configuration" %}}

You kept one Config Builder project open while completing Chapters 2 through
4. Deploying it now applies the filter, sensitive-data protection, and log
transformation together. A single restart also makes the before-and-after
validation easier to follow.

{{< step "Review the completed YAML" "1" >}}

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

{{< tabs id="completed-config-source" >}}
{{% tab title="Same computer" %}}

Select **Download YAML** and save the file as `agent_config.yaml`.

{{% /tab %}}
{{% tab title="Splunk Show instance" %}}

You do not need to download or transfer the YAML. To avoid file-transfer and
copy-and-paste issues, Step 2 uses the completed configuration that is already
available on the Splunk Show instance.

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Keep credentials outside the YAML" style="warning" %}}
The YAML must contain environment-variable references, not token values.
{{% /notice %}}

{{< /step >}}

{{< step "Replace the running configuration" "2" >}}

In the **Agent terminal**, press `Ctrl-C` to stop the agent. Then select the tab
for your execution path.

{{< tabs id="config-transfer" >}}
{{% tab title="Same computer" %}}

```bash
cp ~/Downloads/agent_config.yaml [WORKSHOP]/1-agent/agent_config.yaml
```

Replace `[WORKSHOP]` with the full workshop path.

{{% /tab %}}
{{% tab title="Splunk Show instance" %}}

In the **Command terminal** on the Splunk Show instance, copy the completed
configuration into the agent folder:

```bash
cp ~/workshop/ninja/obs1184/agent_config.solution.yaml \
  ~/advanced-otel-workshop/1-agent/agent_config.yaml
```

This local copy avoids `scp` and does not require you to paste the completed
YAML into the SSH session.

{{% /tab %}}
{{< /tabs >}}

{{% notice title="Recovery copy" style="info" %}}
If you need a new copy of the completed configuration, Splunk Show attendees
can copy
`~/workshop/ninja/obs1184/agent_config.solution.yaml` again. Attendees running
the Collector on the same computer as the browser can download
[agent_config.solution.yaml](https://github.com/splunk/observability-workshop/blob/main/workshop/ninja/obs1184/agent_config.solution.yaml)
and copy it to `[WORKSHOP]/1-agent/agent_config.yaml`.
{{% /notice %}}

Move the earlier plain-text log so the File Log receiver reads only the new JSON
test data:

```bash
test ! -f quotes.log || mv quotes.log quotes.log.before-config-builder
```

{{< /step >}}

{{< step "Restart the agent" "3" >}}

{{% notice title="Stop the previous Collector first" style="warning" %}}
Only one Collector can listen on the workshop ports. Make sure the previous
Collector stopped after you pressed `Ctrl-C`. In the **Command terminal**, run
`ps aux | grep '[o]telcol'`. If the command lists the workshop Collector,
return to its terminal and press `Ctrl-C` before you continue.
{{% /notice %}}

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

1. Read the first startup error. Collector errors usually identify the
   component, configuration field, or network address that caused the failure.
2. If the error includes `address already in use`, run
   `ps aux | grep '[o]telcol'`. Stop the previous workshop Collector with
   `Ctrl-C`, then start the agent again.
3. To see more Collector diagnostics, restart it with debug logging:

   ```bash
   source ../workshop-env.sh
   SPLUNK_COLLECTOR_LOG_LEVEL=debug ../otelcol --config=agent_config.yaml
   ```

4. If the error identifies a component or field in `agent_config.yaml`, compare
   it with the completed configuration described in the **Recovery copy** note.
   Replace the file with that recovery copy if you cannot resolve the error.
5. If `workshop-env.sh` is missing, rerun `[WORKSHOP]/setup-workshop.sh`.

{{% /expand %}}

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The updated single-agent configuration is running." >}}
