---
title: 5.2 Setup Environment
linkTitle: 5.2 Setup Environment
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In the **Gateway terminal** run:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent terminal** run:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Start the Load Generator**: Open the **Logs terminal** window and run the `loadgen`.

> [!IMPORTANT]
> To ensure the logs are structured in JSON format, include the `-json` flag when starting the script.

```bash { title="Log Generator" }
../loadgen -logs -json -count 5
```

The `loadgen` will write 5 log lines to `./quotes.log` in JSON format.

{{% /notice %}}
