---
title: 4.3 Redaction Processorのテスト
linkTitle: 4.3 Redaction Processorのテスト
weight: 3
---

`redaction` プロセッサは、テレメトリーデータからどの属性と値を**許可**または**削除**するかを正確に制御できます。

この演習では、**Agent** がエクスポートする前に、Spanデータの `user.visa` と `user.mastercard` の値を**秘匿化**します。
{{% notice title="Exercise" style="green" icon="running" %}}

**Gatewayを起動する**：**Gateway terminal** ウィンドウで **Gateway** を起動します。

```bash
../otelcol --config=gateway.yaml
```

**`redaction/redact` プロセッサを有効にする**：**Agent terminal** ウィンドウで、`agent.yaml` を編集して前の演習で追加した `#` を削除します。

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

**Agentを起動する**：**Agent terminal** ウィンドウで **Agent** を起動します。

```bash
../otelcol --config=agent.yaml
```

**Load Generatorを起動する**：**Loadgen terminal** ウィンドウで `loadgen` を起動します

```bash
../loadgen -count 1
```

**デバッグ出力を確認する**：**Agent** と **Gateway** の両方で、`user.visa` と `user.mastercard` の値が更新されていることを確認します。`user.amex` 属性の値は、`blocked_values` に一致する正規表現パターンが追加されていないため、秘匿化されて**いない**ことに注意してください。

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
redaction プロセッサに `summary:debug` を含めると、デバッグ出力に、どの一致するキー値が秘匿化されたか、およびマスクされた値の数に関するサマリー情報が含まれます。

```text
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
 ```

{{% /notice %}}

**ファイル出力を確認する**：`jq` を使用して、`gateway-traces.out` で `user.visa` と `user.mastercard` が更新されていることを検証します。

{{% tabs %}}
{{% tab title="Validate attribute changes" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.visa" or .key == "user.mastercard" or .key == "user.amex") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="Output" %}}

`blocked_values` に一致する正規表現パターンが追加されていないため、`user.amex` は秘匿化されていないことに注意してください

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

これらは、`attributes` と `redaction` プロセッサを設定して機密データを保護する方法のほんの一例です。

{{% /notice %}}

> [!IMPORTANT]
> **Agent** と **Gateway** プロセスを、それぞれのターミナルで `Ctrl-C` を押して停止してください。

<!--
**(Optional) Redact Amex CC number**:

Add the Amex card regex to `blocked_values` and restart **Agent** collector.

```yaml
'\b3[47][0-9]{2}[\s-]?[0-9]{6}[\s-]?[0-9]{5}\b'
```
-->
