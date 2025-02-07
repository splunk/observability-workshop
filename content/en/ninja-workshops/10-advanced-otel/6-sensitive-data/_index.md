---
title: 6. Redacting Sensitive Data
linkTitle: 6. Sensitive Data
time: 10 minutes
weight: 6
---

In this section, you'll learn how to configure the OpenTelemetry Collector to remove specific tags and redact sensitive data from telemetry spans. This is crucial for protecting sensitive information such as credit card numbers, personal data, or other security-related details that must be anonymized before being processed or exported.

We'll walk through configuring key processors in the OpenTelemetry Collector, including:

- **[Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)**: Modifies or removes specific span attributes.
- [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md): Ensures sensitive data is sanitized before being stored or transmitted.

{{% notice title="Exercise" style="green" icon="running" %}}

- Inside the `[WORKSHOP]` directory, create a new subdirectory named `6-sensitive-data`.
- Next, copy all contents from the `5-dropping-spans` directory into `6-sensitive-data`.
- After copying, remove any `*.out` and `*.log` files.
- Make sure all terminal window are pointing to the `[WORKSHOP]/6-sensitive-data` folder.

Your updated directory structure will now look like this:

{{% tabs %}}
{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
├── 6-sensitive-data
│   ├───checkpoint-dir
│   ├── agent.yaml
│   ├── gateway.yaml
│   ├── health.json
│   ├── log-gen.sh (or .ps1)
│   └── trace.json
└── otelcol
```

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}
