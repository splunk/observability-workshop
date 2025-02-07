---
title: 2.1 Test Gateway
linkTitle: 2.1 Test Gateway
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**:

1. Find your **Gateway** terminal window.
2. Navigate to the`[WORKSHOP]/2-gateway` directory.
3. Run the following command to test the gateway configuration:

```text
../otelcol --config=gateway.yaml
```

If everything is set up correctly, the first and last lines of the output should look like:

```text
2025/01/15 15:33:53 settings.go:478: Set config to [gateway.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.116.0/service.go:261 Everything is ready. Begin running and processing data.
```

{{% /notice %}}

Next, we will configure the **Agent** to send data to the newly created **Gateway**.
