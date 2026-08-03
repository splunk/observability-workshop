---
title: 3.1 Protect Sensitive Span Attributes
linkTitle: 3.1 Configure Protection
weight: 1
---

{{% exercise title="Add attributes and redaction processors" %}}

{{< step "Create the attributes processor" "1" >}}

In **Component Inventory**, click **Add component**. Select component type
`processor`, select component `attributes`, and click **Next**.

In **Options**, add these actions in order:

1. Update `user.phone_number` to `UNKNOWN NUMBER`.
2. Hash `user.email`.
3. Delete `user.password`.

Review **Preview** and click **Add**. The generated component should be
equivalent to:

```yaml
processors:
  attributes:
    actions:
      - key: user.phone_number
        action: update
        value: UNKNOWN NUMBER
      - key: user.email
        action: hash
      - key: user.password
        action: delete
```

{{% notice title="Use the exact password key" style="info" %}}
The load generator emits `user.password`. The processor key must match it
exactly or the password attribute will remain in the exported span.
{{% /notice %}}

{{< /step >}}

{{< step "Create the redaction processor" "2" >}}

Click **Add component** again. Select component type `processor`, select
component `redaction`, and click **Next**.

Set `allow_all_keys` to `true`, set `summary` to `debug`, and add these two
blocked-value regular expressions:

```text
\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b
\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b
```

The first pattern matches the synthetic Visa value and the second matches the
Mastercard value. The Amex value is intentionally left unmatched so the test
can demonstrate an incomplete policy.

Review **Preview** and click **Add**. The generated component should be
equivalent to:

```yaml
processors:
  redaction:
    allow_all_keys: true
    blocked_values:
      - '\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'
      - '\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'
    summary: debug
```

{{< /step >}}

{{< step "Add both processors to the traces pipeline" "3" >}}

Select **Pipelines**, click the pencil-shaped **Edit** icon for `traces`, and
select both `attributes` and `redaction` in the **processors** selector. Keep
all existing selections and click **Edit**.

Open **Collector YAML** and confirm:

- Both processor definitions are present.
- `attributes` and `redaction` each appear exactly once in
  `service.pipelines.traces.processors`.
- All existing trace receivers and exporters remain connected.

The relevant pipeline list should be equivalent to:

```yaml
service:
  pipelines:
    traces:
      processors:
        - memory_limiter
        - resource/add_mode
        - batch
        - resource_detection
        - filter
        - attributes
        - redaction
```

The order of `attributes` and `redaction` does not change this exercise's
result. Confirm that both appear exactly once and that the existing receivers,
processors, and exporters remain connected.

Keep the project open and continue to Chapter 4.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The traces pipeline now filters health checks and protects the selected sensitive attributes." >}}
