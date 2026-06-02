---
title: 6.2 Test Attribute Processor
linkTitle: 6.2 Test Attribute Processor
weight: 2
---

この演習では、`agent` がスパンデータをエクスポートする前に、`user.account_password` を **削除** し、`user.phone_number` の **属性** を **更新** し、`user.email` を **ハッシュ化** します。

{{% notice title="演習" style="green" icon="running" %}}

**Gateway を起動する**: **Gateway terminal** ウィンドウで `gateway` を起動します。

```bash
../otelcol --config=gateway.yaml
```

**Agent を起動する**: **Agent terminal** ウィンドウで `agent` を起動します。

```bash
../otelcol --config=agent.yaml
```

**Load Generator を起動する**: **Spans terminal** ウィンドウで `loadgen` を起動します。

```bash
../loadgen -count 1
```

**デバッグ出力を確認する**: `agent` と `gateway` の両方のデバッグ出力で、`user.account_password` が削除され、`user.phone_number` と `user.email` の両方が更新されていることを確認します。

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

**ファイル出力を確認する**: `jq` を使用して、`gateway-taces.out` 内で `user.account_password` が削除され、`user.phone_number` と `user.email` が更新されていることを検証します。

{{% tabs %}}
{{% tab title="Validate attribute changes" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.password" or .key == "user.phone_number" or .key == "user.email") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="Output" %}}

`user.account_password` が削除され、`user.phone_number` と `user.email` が更新されていることを確認します。

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
> 各ターミナルで `Ctrl-C` を押して、`agent` と `gateway` のプロセスを停止してください。

{{% /notice %}}
