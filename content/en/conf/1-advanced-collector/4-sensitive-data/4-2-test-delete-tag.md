---
title: 4.2 Test Attribute Processor
linkTitle: 4.2 Test Attribute Processor
weight: 2
---

In this exercise, we will **delete** the `user.account_password`, **update** the `user.phone_number` **attribute** and **hash** the `user.email` in the span data before it is exported by the **Agent**.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In your **Gateway terminal** window start the **Gateway**.

```bash
../otelcol --config=gateway.yaml
```

**Start the Agent**: In your **Agent terminal** window start the **Agent**.

```bash
../otelcol --config=agent.yaml
```

**Start the Load Generator**: In the **Spans terminal** window start the `loadgen`:

```bash
../loadgen -count 1
```

**Check the debug output**: For both the **Agent** and **Gateway** debug output, confirm that `user.account_password` has been removed, and both `user.phone_number` & `user.email` have been updated.

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(UNKNOWN NUMBER)
     -> user.email: Str(62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287)
     -> payment.amount: Double(51.71)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
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
     -> payment.amount: Double(95.22)
  ```

{{% /tab %}}
{{% /tabs %}}

**Check file output**: Using `jq` validate that `user.account_password` has been removed, and `user.phone_number` & `user.email` have been updated in `gateway-taces.out`:

{{% tabs %}}
{{% tab title="Validate attribute changes" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.password" or .key == "user.phone_number" or .key == "user.email") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="Output" %}}

Notice that the `user.account_password` has been removed, and the `user.phone_number` & `user.email` have been updated:

```json
{
  "key": "user.phone_number",
  "value": "UNKNOWN NUMBER"
}
{
  "key": "user.email",
  "value": "62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287"
}
```

{{% /tab %}}
{{% /tabs %}}

> [!IMPORTANT]
> Stop the **Agent** and the **Gateway** processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}
