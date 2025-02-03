---
title: Redacting Sensitive Data
linkTitle: 6. Sensitive Data
time: 10 minutes
weight: 6
---

In this section, you'll learn how to configure the OpenTelemetry Collector to remove specific tags and redact sensitive data from telemetry spans. This is crucial for protecting sensitive information such as credit card numbers, personal data, or other security-related details that must be anonymized before being processed or exported.

We'll walk through configuring key processors in the OpenTelemetry Collector, including:

- **Attributes Processor**: Modifies or removes specific span attributes.
- **Redaction Processor**: Ensures sensitive data is sanitized before being stored or transmitted.

### Setup

Navigate to the directory where you're running the workshop. Create a new subdirectory called `6-sensitive-data`, then copy the latest versions of `agent.yaml` and `trace.json` from `[WORKSHOP]/5-dropping-spans` into this new directory.

Change into the `[WORKSHOP]/6-sensitive-data` directory to begin configuring the processors. Your updated workshop structure should now look like this:

{{% tab title="Updated Directory Structure" %}}

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
├── 6-sensitive-data
│   ├── gateway.yaml
│   ├── agent.yaml
│   ├── log-gen.sh (or .ps1)
│   ├── health.json
│   └── trace.json
└── otelcol
```

{{% /tab %}}

Next, we'll update `agent.yaml` to include the `attributes` and `redaction` processors. These processors will ensure that sensitive data within span attributes is properly handled before being logged or exported.

Previously, you may have noticed that certain span attributes displayed in the console contained personal data. In the following steps, we'll configure the necessary processors to filter out and redact this information effectively.

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
    attributes/removetags:           # Processor Type/Name
      actions:                       # Array of actions
        - key: user.account_password # Target key
          action: delete             # Action is delete 
  ```

- **Add an other  `Attributes` Processor** and name it `update:`
The `attributes` processor also allows you to update specific attributes (tags) from spans. In this case, we're update the tag `user.phone_number` to "UNKNOWN NUMBER", hash the `user.email` and replace the amex card number with the word "Redacted":

  ```yaml
    attributes/update:              # Processor Type/Name
      actions:                      # Array of actions
        - key: user.phone_number    # Target key
          action: update            # Action is update key with value
          value: "UNKNOWN NUMBER" 
        - key: user.email           # Target key
          action: hash              # Action is hash key
          action: update            # Target key
          value: "Redacted"         # Action is update key with value
  ```

- **Add a `redaction` Processor** and name it `redact:`

  ```yaml
    redaction/redact:               # Processor Type/Name
      allow_all_keys: true          # False removes all key unless in allow list 
      blocked_values:               # List of regex to check and hash
          # Visa card regex.  - Please note the '' around the regex
        - '\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'
          # MasterCard card regex - Please note the '' around the regex
        - '\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b' 
      summary: debug  # Show detailed debug information about the redaction 

  ```

- **Update the `traces`  pipeline**: Add the both the `attribute` processors and the  `redaction` processor into the `traces:` pipeline but make sure `attributes/update:`  & `redaction/redact` are commented out.

  ```yaml
      traces:
        receivers: [otlp]       # Receiver  array for traces
        processors:             # Alternative syntax option [memory_limiter]
        - memory_limiter        # Handles memory limits for this pipeline
        - attributes/removetags # Removes user.account_password attribute
        #- attributes/update     # Update and hash tags 
        #- redaction/redact      # Redacting fields on regex 
        - resourcedetection     # Adds system attributes to the data
        - resource/add_mode     # Adds collector mode metadata
        - batch
        exporters: [debug,otlphttp] # Array of trace Exporters
  ```

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `Traces` pipeline should look like this:

![redacting 1](../images/senstive-data-6-1.png)
