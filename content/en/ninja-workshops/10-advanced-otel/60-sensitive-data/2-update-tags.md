---
title: Updating Sensitive data in Tags
linkTitle: 6.2 Update Sensitive data
weight: 2
---

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

- **Configure the processors**:
Open the `agent.yaml` and add the `attributes/removetags`, `attributes/update`, and `redaction/update` configuration to the `processors` section

- **Add the `attribute` and `redaction` processors**: Make sure you add the processors to the `traces` pipeline.

{{% /notice %}}

Using **[otelbin.io](https://www.otelbin.io/)**, the results for the `traces` pipeline should look like this:

![otelbin-f-6-1-traces](../images/otelbin-f-6-1-trace.png)
