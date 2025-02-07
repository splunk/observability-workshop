---
title: 5. Dropping Spans
linkTitle: 5. Dropping Spans
time: 10 minutes
weight: 5
---

In this section, we will explore how to use the **Filter Processor** to selectively drop spans based on certain conditions.

Specifically, we will drop traces based on the span name, which is commonly used to filter out unwanted spans such as health checks or internal communication traces. In this case, we will be filtering out spans whose name is `"/_healthz"`, typically associated with health check requests.

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `5-dropping-spans`.
- Next, copy all contents from the `4-resilience` directory into `5-dropping-spans`.
- After copying, remove any `*.out` and `*.log` files.

Your updated directory structure will now look like this:
Create a new subdirectory named `5-dropping-spans` and copy all contents from the `4-resilience` directory into it. Then, delete any `*.out` and `*.log` files. Your updated directory structure should now look like this:

{{% tabs %}}
{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
│   └───checkpoint-dir
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}

Next, we will configure the **filter processor** and the respective pipelines.
