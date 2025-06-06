---
title: 4.3 Test Redaction Processor
linkTitle: 4.3 Test Redaction Processor
weight: 3
---

The `redaction` processor gives precise control over which attributes and values are **permitted** or **removed** from telemetry data.

In this exercise, we will **redact** the `user.visa` & `user.mastercard` **values** in the span data before it is exported by the `agent`.
{{% notice title="Exercise" style="green" icon="running" %}}

**Prepare the terminals**: Delete the `*.out` files and clear the screen.

**Start the Gateway**: In your **Gateway terminal** window start the `gateway`.

```bash
../otelcol --config=gateway.yaml
```

**Enable the `redaction/redact` processor**: In the **Agent terminal** window, edit `agent.yaml` and remove the `#` we inserted in the previous exercise.

```yaml
    traces:
      receivers:
      - otlp
      processors:
      - memory_limiter
      - attributes/update              # Update, hash, and remove attributes
      - redaction/redact               # Redact sensitive fields using regex
      - resourcedetection
      - resource/add_mode
      - batch
      exporters:
      - debug
      - file
      - otlphttp
```

**Start the Agent**: In your **Agent terminal** window start the `agent`.

```bash
../otelcol --config=agent.yaml
```

**Start the Load Generator**: In the **Spans terminal** window start the `loadgen`:

```bash
../loadgen -count 1
```

**Check the debug output**: For both the `agent` and `gateway` confirm the values for `user.visa` & `user.mastercard` have been updated. Notice `user.amex` attribute value was NOT redacted because a matching regex pattern was not added to `blocked_values`

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(UNKNOWN NUMBER)
     -> user.email: Str(62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287)
     -> payment.amount: Double(69.71)
     -> user.visa: Str(****)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(****)
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
  ```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

 ```text
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
     -> payment.amount: Double(65.54)
  ```

{{% /tab %}}
{{% /tabs %}}

{{% notice note %}}
By including `summary:debug` in the redaction processor, the debug output will include summary information about which matching key values were redacted, along with the count of values that were masked.

```text
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
 ```

{{% /notice %}}

**Check file output**: Using `jq` verify that `user.visa` & `user.mastercard` have been updated in the `gateway-traces.out`.

{{% tabs %}}
{{% tab title="Validate attribute changes" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.visa" or .key == "user.mastercard" or .key == "user.amex") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="Output" %}}

Notice that `user.amex` has not been redacted because a matching regex pattern was not added to `blocked_values`:

```json
{
  "key": "user.visa",
  "value": "****"
}
{
  "key": "user.amex",
  "value": "3782 822463 10005"
}
{
  "key": "user.mastercard",
  "value": "****"
}
```

{{% /tab %}}
{{% /tabs %}}

These are just a few examples of how `attributes` and `redaction` processors can be configured to protect sensitive data.

> [!IMPORTANT]
> Stop the `agent` and the `gateway` processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}
<!--
**(Optional) Redact Amex CC number**:

Add the Amex card regex to `blocked_values` and restart `agent` collector.

```yaml
'\b3[47][0-9]{2}[\s-]?[0-9]{6}[\s-]?[0-9]{5}\b'
```
-->
