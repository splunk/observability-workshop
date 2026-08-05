---
title: 5.1 Deploy the Configuration
linkTitle: 5.1 Deploy Configuration
weight: 1
---

{{% exercise title="Download and start the completed Agent configuration" %}}

{{< step "Review and download the YAML" "1" >}}

In **Collector YAML**, confirm:

- `filter/health`, `attributes`, and `redaction` are connected to `traces`.
- `transform` is connected to `logs` after `resource_detection`.
- The imported receivers, processors, exporters, extensions, and six pipelines
  are still present.

If `transform` is not after `resource_detection`, stop and ask the workshop
facilitator. Do not download the configuration or repair the generated YAML by
hand.

Choose **Download** and save the generated file as `agent_config.yaml`.

{{% notice title="Keep secrets outside the YAML" style="warning" %}}
The configuration must contain environment-variable references such as
`${SPLUNK_ACCESS_TOKEN}`, not real token values. Never paste
`workshop-env.sh` or credentials into Config Builder.
{{% /notice %}}

{{< /step >}}

{{< step "Back up and replace the starter configuration" "2" >}}

Stop the foreground Agent with `Ctrl-C`. In the **Agent Console**, preserve the
starter configuration without overwriting an earlier backup:

```bash
cd [WORKSHOP]/1-agent
if [ ! -f agent_config.start.yaml ]; then
  cp agent_config.yaml agent_config.start.yaml
fi
```

Put the downloaded file at `[WORKSHOP]/1-agent/agent_config.yaml`.

{{% tabs %}}
{{% tab title="Apple Silicon or same computer" %}}

```bash
cp ~/Downloads/agent_config.yaml [WORKSHOP]/1-agent/agent_config.yaml
```

Replace `[WORKSHOP]` with the full path to `advanced-otel-workshop`.

{{% /tab %}}
{{% tab title="Remote workshop instance" %}}

Run this command on your local computer with the SSH values supplied for your
instance:

```bash
scp -P 2222 ~/Downloads/agent_config.yaml \
  <workshop-user>@<workshop-host>:~/advanced-otel-workshop/1-agent/agent_config.yaml
```

If the workshop directory is not directly under the remote home directory,
replace the destination with its actual path.

{{% /tab %}}
{{% /tabs %}}

Move the earlier plaintext quote log so the File Log Receiver processes only
the new JSON test data:

```bash
if [ -f quotes.log ]; then
  mv quotes.log quotes.log.before-config-builder
fi
```

The file exporters use `append: false`, so the Agent starts fresh local trace,
metric, and log output files for this configuration.

{{< /step >}}

{{< step "Start the updated Agent" "3" >}}

From `[WORKSHOP]/1-agent`, source the generated environment file and start the
Agent:

```bash
source ../workshop-env.sh
../otelcol --config=agent_config.yaml
```

Confirm that startup reaches:

```text
Everything is ready. Begin running and processing data.
```

Leave the Agent running for Step 5.2.

{{% notice title="If workshop-env.sh is missing" style="info" %}}
`workshop-env.sh` is generated at `[WORKSHOP]/workshop-env.sh` when
`setup-workshop.sh` completes. Return to `[WORKSHOP]` and rerun
`./setup-workshop.sh`; do not create or download this credentials file by hand.
{{% /notice %}}

If the Collector reports a configuration error, stop it and use the component
name and field in the error message to correct the Config Builder project.
Download the corrected YAML and start the Agent again.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The updated Agent is running with all four processors enabled." >}}
