---
title: 4.3 Redaction プロセッサーのテスト
linkTitle: 4.3 Redaction プロセッサーのテスト
weight: 3
---

`redaction` プロセッサーは、テレメトリーデータから **許可** または **削除** する属性と値を細かく制御できます。

この演習では、**Agent** がエクスポートする前のスパンデータの `user.visa` と `user.mastercard` の値を **リダクション** します。
{{% exercise title="redaction プロセッサーのテスト" %}}

**Gateway を起動する**: **Gateway terminal** ウィンドウで **Gateway** を起動します。

```bash
../otelcol --config=gateway.yaml
```

**`redaction/redact` プロセッサーを有効にする**: **Agent terminal** ウィンドウで `agent.yaml` を編集し、前の演習で挿入した `#` を削除します。

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

**Agent を起動する**: **Agent terminal** ウィンドウで **Agent** を起動します。

```bash
../otelcol --config=agent.yaml
```

**Load Generator を起動する**: **Loadgen terminal** ウィンドウで `loadgen` を起動します。

```bash
../loadgen -count 1
```

**デバッグ出力を確認する**: **Agent** と **Gateway** の両方で `user.visa` と `user.mastercard` の値が更新されていることを確認します。`user.amex` 属性の値は `blocked_values` に一致する正規表現パターンが追加されていないため、**リダクションされていない** ことに注意してください。

{{% tabs %}}
{{% tab title="新しいデバッグ出力" %}}

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
{{% tab title="元のデバッグ出力" %}}

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
redaction プロセッサーに `summary:debug` を含めると、どの一致したキーの値がリダクションされたかについての概要情報と、マスクされた値の数がデバッグ出力に含まれます。

```text
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
 ```

{{% /notice %}}

**ファイル出力を確認する**: `jq` を使用して、`gateway-traces.out` 内の `user.visa` と `user.mastercard` が更新されていることを確認します。

{{% tabs %}}
{{% tab title="属性の変更を検証する" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.visa" or .key == "user.mastercard" or .key == "user.amex") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="出力" %}}

`user.amex` は `blocked_values` に一致する正規表現パターンが追加されていないため、リダクションされていないことに注意してください。

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

これらは `attributes` プロセッサーと `redaction` プロセッサーが機密データを保護するために設定可能な方法のほんの一例です。

{{% /exercise %}}

> [!IMPORTANT]
> それぞれのターミナルで `Ctrl-C` を押して、**Agent** と **Gateway** のプロセスを停止してください。

<!--
**(Optional) Redact Amex CC number**:

Add the Amex card regex to `blocked_values` and restart **Agent** collector.

```yaml
'\b3[47][0-9]{2}[\s-]?[0-9]{6}[\s-]?[0-9]{5}\b'
```
-->
