---
title: 6.3 Redaction Processor のテスト
linkTitle: 6.3 Redaction Processor のテスト
weight: 3
---

`redaction` プロセッサーは、テレメトリーデータから **許可** または **削除** する属性と値を、きめ細かく制御できます。

この演習では、`agent` がエクスポートする前のスパンデータに含まれる `user.visa` と `user.mastercard` の **値** を **マスク** します。
{{% notice title="演習" style="green" icon="running" %}}

**ターミナルの準備**: `*.out` ファイルを削除し、画面をクリアします。

**Gateway の起動**: **Gateway terminal** ウィンドウで `gateway` を起動します。

```bash
../otelcol --config=gateway.yaml
```

**`redaction/redact` プロセッサーの有効化**: **Agent terminal** ウィンドウで `agent.yaml` を編集し、前の演習で挿入した `#` を削除します。

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

**Agent の起動**: **Agent terminal** ウィンドウで `agent` を起動します。

```bash
../otelcol --config=agent.yaml
```

**Load Generator の起動**: **Spans terminal** ウィンドウで `loadgen` を起動します。

```bash
../loadgen -count 1
```

**デバッグ出力の確認**: `agent` と `gateway` の両方で、`user.visa` と `user.mastercard` の値が更新されていることを確認します。`user.amex` 属性の値は、`blocked_values` に一致する正規表現パターンが追加されていないため、マスクされていない点に注目してください。

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
redaction プロセッサーに `summary:debug` を含めると、どの一致キー値がマスクされたかの概要情報と、マスクされた値の件数がデバッグ出力に含まれます。

```text
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
 ```

{{% /notice %}}

**ファイル出力の確認**: `jq` を使用して、`gateway-traces.out` 内で `user.visa` と `user.mastercard` が更新されていることを確認します。

{{% tabs %}}
{{% tab title="属性変更の検証" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.visa" or .key == "user.mastercard" or .key == "user.amex") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="出力" %}}

`user.amex` は、`blocked_values` に一致する正規表現パターンが追加されていないため、マスクされていない点に注目してください。

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

これらは、機密データを保護するために `attributes` プロセッサーと `redaction` プロセッサーをどのように構成できるかを示すほんの一例です。

> [!IMPORTANT]
> `agent` と `gateway` のプロセスは、それぞれのターミナルで `Ctrl-C` を押して停止してください。

{{% /notice %}}
<!--
**(Optional) Redact Amex CC number**:

Add the Amex card regex to `blocked_values` and restart `agent` collector.

```yaml
'\b3[47][0-9]{2}[\s-]?[0-9]{6}[\s-]?[0-9]{5}\b'
```
-->
