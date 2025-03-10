---
title: 6.3 Test Redaction Processor
linkTitle: 6.3 Test Redaction Processor
weight: 3
---

The `redaction` processor gives precise control over which attributes and values are **permitted** or **removed** from telemetry data.

In this exercise, we will **redact** the `user.visa` & `user.mastercard` **values** in the span data before it is exported by the `agent`.
{{% notice title="Exercise" style="green" icon="running" %}}

**Prepare the terminals**: Delete the `*.out` files and clear the screen.

**Start the Gateway**: In your **Gateway terminal** window start the `gateway`.

**Enable the `redaction/redact` processor**: In the **Agent terminal** window, edit `agent.yaml` and remove the `#` we inserted in the previous exercise.

**Start the Agent**: In your **Agent terminal** window start the `agent`.

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
By including `summary:debug` in the redaction processor, the debug output will include summary information about which matching keys values were redacted, along with the count of values that were masked.

```text
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
 ```

{{% /notice %}}

**Check file output**: In the newly created `gateway-traces.out` file to verify confirm that `user.visa` & `user.mastercard` have been updated.

{{% tabs %}}
{{% tab title="Validate attribute changes" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.visa" or .key == "user.mastercard") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="Output" %}}

Notice that the `user.account_password` has been removed, and the `user.phone_number` & `user.email` have been updated:

```json
{
  "key": "user.visa",
  "value": "****"
}
{
  "key": "user.mastercard",
  "value": "****"
}
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}
<!--
**(Optional) Redact Amex CC number**:

Add the Amex card regex to `blocked_values` and restart `agent` collector.

```yaml
'\b3[47][0-9]{2}[\s-]?[0-9]{6}[\s-]?[0-9]{5}\b'
```
-->
These are just a few examples of how `attributes` and `redaction` processors can be configured to protect sensitive data.

Stop the `agent` and `gateway` using `Ctrl-C` in their respective terminals.
