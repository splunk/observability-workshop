---
title: 4.2 Setup environment for Resilience Testing
linkTitle: 4.2 Setup environment
weight: 2
---

### Setup Test environment

In this section we are going to simulate an outage on the network between the **Agent** and the **Gateway** and see if our configuration helps the Collector recover from that issue:

{{% notice title="Exercise" style="green" icon="running" %}}

**Run the Gateway**: Find your **Gateway** terminal window, and navigate to the `[WORKSHOP]/4-resilience` directory and start the **Gateway**.

It should start up normally and state : `Everything is ready. Begin running and processing data.`

**Run the Agent**: Find your **Agent** terminal window and navigate to the `[WORKSHOP]/4-resilience` directory and restart the agent with the resilience configurations specified in the YAML file.

It should also start up normally and state : `Everything is ready. Begin running and processing data.`

**Send a Test Trace**:
Find your `Test` terminal window and navigate to the `[WORKSHOP]/4-resilience` directory. From there, send a test trace to confirm that communication is functioning as expected.

Both the agent and gateway should display debug information, including the trace you just sent. Additionally, the gateway should generate a new `./gateway-traces.out` file.

If everything is working as expected, we can move on to testing the system’s resilience.

{{% /notice %}}

This setup enables your OpenTelemetry Collector to handle network interruptions smoothly by storing telemetry data on disk and retrying failed transmissions. It combines checkpointing for recovery with queuing for efficient retries, enhancing the resilience and reliability of your pipeline. Now, let’s test the configuration!
