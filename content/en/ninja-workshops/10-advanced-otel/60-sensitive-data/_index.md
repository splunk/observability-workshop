---
title: Removing Tags and Redacting Sensitive Data in OpenTelemetry Collector
linkTitle: 6. Sensitive Data
time: 10 minutes
weight: 6
---

In this section, you'll learn how to configure the OpenTelemetry Collector to **remove specific tags** and **redact sensitive data** from your telemetry (spans). This is essential when dealing with sensitive information such as credit card numbers, personal data, or other security-related information that needs to be protected or anonymized.

We'll walk through how to configure several processors in the OpenTelemetry Collector, including:

- **Attributes** Processor
- **Redaction** Processor

### Setup

On your machine, navigate to the directory where you're running the workshop. Create a new subdirectory called `6-sensitive-data`, then copy the latest versions of `agent.yaml` and `trace.json` from `[WORKSHOP]\5-dropping-spans` into this new directory.

Next, move into the `[WORKSHOP]/6-sensitive-data` directory.

{{% tab title="Initial Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
├── 6-remove-sensitive-data
│   ├── gateway.yam
│   ├── agent.yam
│   ├── log-gen.sh (or .ps1)
│   ├── health.json
│   └── trace.json
└── otelcol
```

{{% /tab %}}

In this section, we will update the `agent.yaml` file to include **attributes** and **redaction** processors. These will help handle **sensitive data** within span data.

Previously, you may have noticed certain **tags (attributes) containing personal data** in the span data displayed in the console:

```text
<snip>
Attributes:
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.account_password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
  {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

So, Let's start an exercise to clean those up:

{{% notice title="Exercise" style="green" icon="running" %}}

- **Add a `Attributes` Processor** and name it `removetags:`
The `attributes` processor allows you to delete specific attributes (tags) from spans. In this case, we're removing the tag `user.account_password` using delete:

  ```yaml
    attributes/removetags:
      actions:
        - key: user.account_password
          action: delete
  ```

- **Add an other  `Attributes` Processor** and name it `update:`
The `attributes` processor also allows you to update specific attributes (tags) from spans. In this case, we're update the tag `user.phone_number` to a all five's, hash the `user.account_email` :

  ```yaml
    attributes/update:
      actions:
        - key: user.phone_number
          action: update
          value: "555-555-555" 
        - key: user.account_email
          action: hash
  ```

- **Update the `traces`  pipeline**: Add the both the processors into the `traces:` pipeline but make sure the `attributes/update:` is commented out.

  ```yaml
      traces:
        receivers: [otlp]       # Receiver  array for traces
        processors:             # Alternative syntax option [memory_limiter]
        - memory_limiter        # Handles memory limits for this pipeline
        - attributes/removetags # Removes user.account_password attribute
        - attributes/update     # Update and has tags 
        #- resourcedetection     # Adds system attributes to the data
        - resource/add_mode     # Adds collector mode metadata
        - batch
        exporters: [debug,otlphttp] # Array of trace Exporters
  ```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `Traces` pipeline should look like this:

![redacting 1](../images/senstive-data-6-1.png)
