---
title: 4. Redacting Sensitive Data
linkTitle: 4. Sensitive Data
time: 10 minutes
weight: 6
---

In this section, you'll learn how to configure the OpenTelemetry Collector to remove specific tags and redact sensitive data from telemetry spans. This is crucial for protecting sensitive information such as credit card numbers, personal data, or other security-related details that must be anonymized before being processed or exported.

We'll walk through configuring key processors in the OpenTelemetry Collector, including:

- **[Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)**: Modifies or removes specific span attributes.
- [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md): Ensures sensitive data is sanitized before being stored or transmitted.

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **Change _ALL_ terminal windows to the `4-sensitive-data` directory and run the `clear` command.**

Copy `*.yaml` from the `3-dropping-spans` directory into `4-sensitive-data`. Your updated directory structure will now look like this:

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
