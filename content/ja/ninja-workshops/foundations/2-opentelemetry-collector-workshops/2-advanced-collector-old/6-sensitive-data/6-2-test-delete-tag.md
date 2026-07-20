---
title: 6.2 Attribute Processorのテスト
linkTitle: 6.2 Attribute Processorのテスト
weight: 2
---

この演習では、`agent`がエクスポートする前に、Spanデータ内の`user.account_password`を**削除**し、`user.phone_number` **属性**を**更新**し、`user.email`を**ハッシュ化**します。

{{% notice title="演習" style="green" icon="running" %}}

**Gatewayの起動**: **Gatewayターミナル**ウィンドウで`gateway`を起動します。

```bash
../otelcol --config=gateway.yaml
```

**Agentの起動**: **Agentターミナル**ウィンドウで`agent`を起動します。

```bash
../otelcol --config=agent.yaml
```

**Load Generatorの起動**: **Spansターミナル**ウィンドウで`loadgen`を起動します。

```bash
../loadgen -count 1
```

**デバッグ出力の確認**: `agent`と`gateway`の両方のデバッグ出力で、`user.account_password`が削除され、`user.phone_number`と`user.email`が更新されていることを確認します。

{{% tabs %}}
{{% tab title="新しいデバッグ出力" %}}

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
{{% tab title="元のデバッグ出力" %}}

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

**ファイル出力の確認**: `jq`を使用して、`gateway-taces.out`内の`user.account_password`が削除され、`user.phone_number`と`user.email`が更新されていることを検証します。

{{% tabs %}}
{{% tab title="属性変更の検証" %}}

```bash
jq '.resourceSpans[].scopeSpans[].spans[].attributes[] | select(.key == "user.password" or .key == "user.phone_number" or .key == "user.email") | {key: .key, value: .value.stringValue}' ./gateway-traces.out
```

{{% /tabs %}}
{{% tab title="出力" %}}

`user.account_password`が削除され、`user.phone_number`と`user.email`が更新されていることを確認します。

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
> それぞれのターミナルで `Ctrl-C` を押して、`agent`と`gateway`のプロセスを停止してください。

{{% /notice %}}
