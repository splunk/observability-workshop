---
title: 4.1 Configuration
linkTitle: 4.1 Configuration
weight: 1
---

In this step, we'll modify `agent.yaml` to include the `attributes` and `redaction` processors. These processors will help ensure that sensitive data within span attributes is properly handled before being logged or exported.

Previously, you may have noticed that some span attributes displayed in the console contained personal and sensitive data. We'll now configure the necessary processors to filter out and redact this information effectively.

```text
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

{{% notice title="Exercise" style="green" icon="running" %}}

Switch to your **Agent terminal** window and open the `agent.yaml` file in your editor. We’ll add two processors to enhance the security and privacy of your telemetry data.

**1. Add an `attributes` Processor**: The [**Attributes Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor) allows you to modify span attributes (tags) by updating, deleting, or hashing their values. This is particularly useful for obfuscating sensitive information before it is exported.

In this step, we’ll:

1. **Update** the `user.phone_number` attribute to a static value `("UNKNOWN NUMBER")`.
2. **Hash** the `user.email` attribute to ensure the original email is not exposed.
3. **Delete** the `user.password` attribute to remove it entirely from the span.

```yaml
  attributes/update:
    actions:                           # Actions
      - key: user.phone_number         # Target key
        action: update                 # Update action
        value: "UNKNOWN NUMBER"        # New value
      - key: user.email                # Target key
        action: hash                   # Hash the email value
      - key: user.password             # Target key
        action: delete                 # Delete the password
  ```

**2. Add a `redaction` Processor**: The [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor) detects and redacts sensitive data in span attributes based on predefined patterns, such as credit card numbers or other personally identifiable information (PII).

In this step:

- We set `allow_all_keys: true` to ensure all attributes are processed (if set to `false`, only explicitly allowed keys are retained).

- We define `blocked_values` with regular expressions to detect and redact **Visa** and **MasterCard** credit card numbers.

- The `summary: debug` option logs detailed information about the redaction process for debugging purposes.

```yaml
  redaction/redact:
    allow_all_keys: true               # If false, only allowed keys will be retained
    blocked_values:                    # List of regex patterns to block
      - '\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'       # Visa
      - '\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'  # MasterCard
    summary: debug                     # Show debug details about redaction
```

**Update the `traces` Pipeline**: Integrate both processors into the `traces` pipeline. Make sure that you comment out the redaction processor at first (we will enable it later in a separate exercise). Your configuration should look like this:

```yaml
    traces:
      receivers:
      - otlp
      processors:
      - memory_limiter
      - attributes/update              # Update, hash, and remove attributes
      #- redaction/redact               # Redact sensitive fields using regex
      - resourcedetection
      - resource/add_mode
      - batch
      exporters:
      - debug
      - file
      - otlphttp
```

{{% /notice %}}

<!--
Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces:` section of your pipelines will look similar to this:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRML(memory_limiter<br>fa:fa-microchip):::processor
      PRRD(resourcedetection<br>fa:fa-microchip):::processor
      PRRS(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRBA(batch<br>fa:fa-microchip):::processor
      PRUP(attributes<br>fa:fa-microchip<br>update):::processor
      EXP1(otlphttp<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;debug&ensp;&ensp;<br>fa:fa-upload):::exporter
      EXP3(file<br>fa:fa-upload):::exporter

    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[**Traces**]
      direction LR
      REC1 -- > PRML
      PRML -- > PRUP
      PRUP -- > PRRD
      PRRD -- > PRRS
      PRRS -- > PRBA
      PRBA -- > EXP2
      PRBA -- > EXP3
      PRBA -- > EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
-->