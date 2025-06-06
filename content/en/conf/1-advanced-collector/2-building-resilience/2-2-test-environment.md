---
title: 2.2 Setup environment for Resilience Testing
linkTitle: 2.2 Setup environment
weight: 2
---

Next, we will configure our environment to be ready for testing the **File Storage** configuration.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In the **Gateway terminal** window navigate to the `[WORKSHOP]/4-resilience` directory and run:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent terminal** window navigate to the `[WORKSHOP]/4-resilience` directory and run:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Send five test spans**: In the **Spans terminal** window navigate to the `[WORKSHOP]/4-resilience` directory and run:

```bash { title="Start Load Generator" }
../loadgen -count 5
```

Both the `agent` and `gateway` should display debug logs, and the `gateway` should create a `./gateway-traces.out` file.

{{% /notice %}}

If everything functions correctly, we can proceed with testing system resilience.
