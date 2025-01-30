---
title: Removing Tags and Redacting Sensitive Data in OpenTelemetry Collector
linkTitle: 6. Sensitive Data
time: 10 minutes
weight: 6
---

In this section, you'll learn how to configure the OpenTelemetry Collector to remove specific tags and redact sensitive data from your telemetry (traces). This is essential when dealing with sensitive information such as credit card numbers, personal data, or other security-related information that needs to be protected or anonymized.

We'll walk through how to configure several processors in the OpenTelemetry Collector, including:

- **Removing Tags**.
- **Redacting Sensitive Data** (such as credit card numbers and account credentials).
- **Using regular expressions to block sensitive data**.

By the end of this workshop, you'll have a working OpenTelemetry Collector configuration that securely handles sensitive telemetry data.

Here’s a breakdown of the main components:

Processors: These will handle the data removal and redaction.
Batch Processor: We'll use it to control how traces are batched and exported.
Memory Limiter: Ensures that the collector does not consume too much memory.
Redaction Processor: A dedicated processor for redacting sensitive data, including credit card numbers and account details.

### Step 1: Initial Setup

On your machine, navigate to the directory where you're running the workshop. Create a new subdirectory called `6-remove-sensitive-data`, then copy the latest versions of `agent.yaml` and `trace.json` from `1-agent` into this new directory.

Next, move into the `[WORKSHOP]/6-remove-sensitive-data` directory 

```text
WORKSHOP
├── 1-agent
├── 2-gateway
├── 3-filelog
├── 4-resilience
├── 5-dropping-spans
├── 6-remove-sensitive-data
│   ├── agent.yaml
│   └── trace.json
└── otelcol
```

#### 1.2 Setup and Review Simulated Trace Data

For this section, you'll need to generate some trace data that includes sensitive data.

Copy the following JSON and save to the file named `trace.json` in the `6-remove-sensitive-data` directory:

{{% tabs %}}
{{% tab title="Compacted JSON" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"my.service"}},{"key":"deployment.environment","value":{"stringValue":"my.environment"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"I'm a server span","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[{"key":"user.name","value":{"stringValue":"George Lucas"}},{"key":"user.user_id","value":{"stringValue":"oldbenkenobi"}},{"key":"user.phone_number","value":{"stringValue":"+1555-867-5309"}},{"key":"user.email","value":{"stringValue":"george@deathstar.email"}},{"key":"user.account_password","value":{"stringValue":"LOTR>StarWars1-2-3"}},{"key":"user.visa","value":{"stringValue":"4111 1111 1111 1111"}},{"key":"user.amex","value":{"stringValue":"3782 822463 10005"}},{"key":"user.mastercard","value":{"stringValue":"5555 5555 5555 4444"}}]}]}]}]}
```

{{% /tab %}}

{{% tab title="Formatted JSON" %}}

```json
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": {
              "stringValue": "my.service"
            }
          },
          {
            "key": "deployment.environment",
            "value": {
              "stringValue": "my.environment"
            }
          }
        ]
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "my.library",
            "version": "1.0.0",
            "attributes": [
              {
                "key": "my.scope.attribute",
                "value": {
                  "stringValue": "some scope attribute"
                }
              }
            ]
          },
          "spans": [
            {
              "traceId": "5B8EFFF798038103D269B633813FC60C",
              "spanId": "EEE19B7EC3C1B174",
              "parentSpanId": "EEE19B7EC3C1B173",
              "name": "I'm a server span",
              "startTimeUnixNano": "1544712660000000000",
              "endTimeUnixNano": "1544712661000000000",
              "kind": 2,
              "attributes": [
                {
                  "key": "user.name",
                  "value": {
                    "stringValue": "George Lucas"
                  }
                },
                {
                  "key": "user.user_id",
                  "value": {
                    "stringValue": "oldbenkenobi"
                  }
                },
                {
                  "key": "user.phone_number",
                  "value": {
                    "stringValue": "+1555-867-5309"
                  }
                },
                {
                  "key": "user.email",
                  "value": {
                    "stringValue": "george@deathstar.email"
                  }
                },
                {
                  "key": "user.account_password",
                  "value": {
                    "stringValue": "LOTR>StarWars1-2-3"
                  }
                },
                {
                  "key": "user.visa",
                  "value": {
                    "stringValue": "4111 1111 1111 1111"
                  }
                },
                {
                  "key": "user.amex",
                  "value": {
                    "stringValue": "3782 822463 10005"
                  }
                },
                {
                  "key": "user.mastercard",
                  "value": {
                    "stringValue": "5555 5555 5555 4444"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

In this exercise, we will update the `agent.yaml` file by adding `attribute` and `redaction` processors. 
### Step 2 Configure Agent
### Breakdown of Key Configurations

#### 2.1 Remove Tags (Attributes)

The `attributes/removetags` processor allows you to delete specific attributes (tags) from spans. In this case, we're removing the tag `user.user_id`:

```yaml
attributes/removetags:
  actions:
    - key: user.user_id
      action: delete
```

#### 2.2. Update Sensitive Data

The attributes/update processor is used to update or redact sensitive data. We perform the following actions:

Redacting credit card numbers: Replace the amex card number with the word "redacted".
Deleting the account_password field to remove passwords from traces.
Hashing the account_email to anonymize email addresses.

```yaml
attributes/update:
  actions:
    - key: user.amex
      value: redacted
      action: update
    - key: user.account_password
      action: delete
    - key: user.account_email
      action: hash
```

#### 2.3. Redaction Processor

The redaction/update processor provides fine-grained control over which attributes are allowed or blocked from traces. We configure this processor to:

Allow specific keys: `description`, `group`, `id`, and name are the only allowed attributes.
Block sensitive data: Credit card numbers matching the provided regex patterns (Visa and MasterCard) will be blocked and redacted.

```yaml
redaction/update:
  allow_all_keys: false
  allowed_keys:
    - description
    - group
    - id
    - name
  ignored_keys:
    - safe_attribute  # Attributes that will not be redacted
  blocked_values:
    - "4[0-9]{12}(?:[0-9]{3})?"  # Visa card regex
    - "(5[1-5][0-9]{14})"         # MasterCard card regex
  summary: debug  # Show detailed debug information about redactions
```

Open the `agent.yaml` and add the `attributes/removetags`, `attributes/update`, and `redaction/update` configuration to the `processors` section:

{{% notice title="Exercise" style="green" icon="running" %}}
- **Configure the processors**:
Open the `agent.yaml` and add the `attributes/removetags`, `attributes/update`, and `redaction/update` configuration to the `processors` section

- **Add the `attribute` and `redaction` processors**: Make sure you add the processors to the `traces` pipeline. 

{{% /notice %}}

Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**, the results for the `traces` pipeline should look like this:

![otelbin-f-6-1-traces](../images/otelbin-f-6-1-trace.png)


### Step 2: Verify the Redaction
Ensure that the `agent` is started the `[WORKSHOP]/6-sensitive-data` folder using the correct agent configuration yaml. Next, update and use the **cURL** command we used earlier to send the `health.json` payload, and send the `trace.json` data created above.

After the collector processes the data, verify that:

- The user_id field is deleted.
- The amex cc number field is redacted with the word redacted.
- The account_password field is deleted.
- The account_email field is hashed.
- Sensitive credit card numbers (Visa, MasterCard) are properly masked using regex.
- Check the exported trace data in the file or backend you're using.

### Step 3: Debugging and Monitoring

If you're unsure whether the redaction is working correctly, the summary field in the redaction/update processor will provide helpful debug information.

- Set summary: debug in the configuration.
- This will show detailed diagnostic information about which attributes are redacted, deleted, or updated.

```yaml
summary: debug  # Provides debug-level details on redactions
```

This will log information about each redacted or deleted attribute, helping you troubleshoot if something is missing.

### Step 4: Advanced Configuration (Optional)

#### 4.1 Redacting More Data

You can easily extend the configuration to redact additional sensitive information. For example, if you need to redact phone numbers, social security numbers, or other personally identifiable information (PII), you can add more blocked_values in the redaction processor.

Example:

```yaml
blocked_values:
  - "(\\+\\d{1,2}\\s?)?\\(?\\d{3}\\)?\\s?-?\\d{3}-?\\d{4}"  # Phone number regex
```

#### 4.2 Using Multiple Redaction Strategies

You can combine different strategies for redaction, such as:

-Replacing values with a fixed string ("REDACTED").
-Hashing values for anonymity.
-Deleting values to remove them completely from telemetry data.

### Conclusion

Congratulations! You've successfully configured the OpenTelemetry Collector to remove tags and redact sensitive data. By following the steps in this workshop, you've ensured that any sensitive information in your telemetry data is properly handled and protected. This configuration is critical for adhering to privacy standards and ensuring secure handling of data in your observability pipelines.

Feel free to extend this configuration to suit your own use cases, and explore more advanced redaction patterns based on your requirements.
