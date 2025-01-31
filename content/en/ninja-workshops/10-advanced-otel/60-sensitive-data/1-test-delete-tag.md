---
title: Testing the Tag delete
linkTitle: 6. Test Tag Delete
time: 10 minutes
weight: 6
---

### Test the Filelog receiver

Find your `gateway` terminal window, navigate to the `[WORKSHOP]/3-filelog` directory, start the `gateway` collector and wait until it is ready to receive data.

Next, to test the Filelog Receiver, find your `agent` terminal window, navigate to the `[WORKSHOP]/3-filelog` directory and start the agent.

The 

{{% notice title="Exercise" style="green" icon="running" %}}

- Update Sensitive Data

The attributes/update processor is used to update or redact sensitive data. We perform the following actions:

- Redacting credit card numbers: Replace the `user.amex` card number with the word `"redacted"`.
- Deleting the `user.account_password` field to remove passwords from traces.
- Hashing the `user.account_email` to anonymize email addresses.

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

Block sensitive data: Credit card numbers matching the provided regex patterns (Visa and MasterCard) will be blocked and redacted.

```yaml
redaction/update:
  allow_all_keys: true
  blocked_values:
    - "4[0-9]{12}(?:[0-9]{3})?"  # Visa card regex
    - "(5[1-5][0-9]{14})"         # MasterCard card regex
  summary: debug  # Show detailed debug information about redactions
```

{{% /notice %}}

In the next exercise you will configure the processors and add to the `traces` pipeline.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Configure the processors**:
Open the `agent.yaml` and add the `attributes/removetags`, `attributes/update`, and `redaction/update` configuration to the `processors` section

- **Add the `attribute` and `redaction` processors**: Make sure you add the processors to the `traces` pipeline.

- **Validate the agent configuration**:
Using **[otelbin.io](https://www.otelbin.io/)**, the results for the `traces` pipeline should look like this:

{{% /notice %}}

![otelbin-f-6-1-traces](../images/otelbin-f-6-1-trace.png)
