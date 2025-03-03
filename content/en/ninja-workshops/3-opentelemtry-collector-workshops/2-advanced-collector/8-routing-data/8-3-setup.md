---
title: 8.3 Setup Environment
linkTitle: 8.3 Setup Environment
weight: 3
---

In this section, we will test the `routing` rule configured for the **Gateway**. The expected result is that the`span` from the `security.json` file will be sent to the `gateway-traces-security.out` file.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In the **Gateway terminal** window navigate to the `[WORKSHOP]/8-routing` directory and run:

```sh {title="Gateway"}
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent terminal** window navigate to the `[WORKSHOP]/8-routing` directory and run:

```sh { title="Agent" }
../otelcol --config=agent.yaml
```

**Start the Loadgen**: In the **Spans terminal** window navigate to the `[WORKSHOP]/8-routing` directory. Run the `loadgen` with the `security` option:

```sh { title="Loadgen" }
../loadgen -security
```

{{% /notice %}}
