---
title: 4.2 Setup environment for Resilience Testing
linkTitle: 4.2 Setup environment
weight: 2
---

Next, we will configure our environment to be ready for testing the **File Storage** configuration.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Start the Gateway**: In the **Gateway** terminal window, and navigate to the `[WORKSHOP]/4-resilience` directory and run:

  ```sh
  ../otelbin --config=gateway.yaml
  ```

- **Start the Agent**: In the **Agent** terminal window and navigate to the `[WORKSHOP]/4-resilience` directory and run:

  ```sh
  ../otelbin --config=agent.yaml
  ```

- **Send a test trace**: In the **Test** terminal window and navigate to the `[WORKSHOP]/4-resilience` directory and run:

  ```sh
  curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
  ```

{{% /notice %}}

Both the **Agent** and **Gateway** should display debug logs, and the **Gateway** should create a `./gateway-traces.out` file.

If everything functions correctly, we can proceed with testing system resilience.
