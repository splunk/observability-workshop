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

**Start the Load Generator**: In the **Loadgen terminal** window, execute the following command to start the load generator with **JSON enabled**:

```bash { title="Log Generator" }
../loadgen -logs -json -count 5
```

The `loadgen` will write 5 log lines to `./quotes.log` in JSON format.

{{% /notice %}}
