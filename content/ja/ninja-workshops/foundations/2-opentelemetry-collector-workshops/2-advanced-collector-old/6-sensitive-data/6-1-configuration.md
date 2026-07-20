---
title: 6.1 設定
linkTitle: 6.1 設定
weight: 1
---

このステップでは、`agent.yaml`を変更して `attributes` および `redaction` Processorを追加します。これらのProcessorにより、Span属性内の機密データがログ出力やエクスポートされる前に適切に処理されるようになります。

以前のステップで、コンソールに表示されたSpan属性の一部に個人情報や機密データが含まれていることに気づいたかもしれません。ここでは、これらの情報を効果的にフィルタリングおよびマスキングするために必要なProcessorを設定します。

```text
<snip>
Attributes:
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.account_password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
  {"kind": "exporter", "data_type": "traces", "name": "debug"}
```

{{% notice title="Exercise" style="green" icon="running" %}}

**Agent terminal** ウィンドウに切り替えて、エディタで `agent.yaml` ファイルを開きます。テレメトリデータのセキュリティとプライバシーを強化するために、Attributes ProcessorとRedaction Processorの2つのProcessorを追加します。

**`attributes` Processorの追加**: [**Attributes Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor) を使用すると、Span属性（タグ）の値を更新、削除、またはハッシュ化して変更できます。これは、エクスポートされる前に機密情報を難読化するのに特に便利です。

このステップでは以下を行います:

1. `user.phone_number` 属性を固定値 `("UNKNOWN NUMBER")` に **更新** します。
2. `user.email` 属性を **ハッシュ化** して、元のメールアドレスが公開されないようにします。
3. `user.password` 属性を **削除** して、Spanから完全に除去します。

```yaml
  attributes/update:
    actions:                           # Actions
      - key: user.phone_number         # Target key
        action: update                 # Update action
        value: "UNKNOWN NUMBER"        # New value
      - key: user.email                # Target key
        action: hash                   # Hash the email value
      - key: user.password             # Target key
        action: delete                 # Delete the password
  ```

**`redaction` Processorの追加**: [**The Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor) は、クレジットカード番号やその他の個人識別情報（PII）などの定義済みパターンに基づいて、Span属性内の機密データを検出しマスキングします。

このステップでは以下を行います:

- `allow_all_keys: true` を設定して、すべての属性が処理されるようにします（`false` に設定すると、明示的に許可されたキーのみが保持されます）。

- `blocked_values` に正規表現を定義して、**Visa** および **MasterCard** のクレジットカード番号を検出しマスキングします。

- `summary: debug` オプションにより、デバッグ目的でマスキング処理の詳細情報がログに記録されます。

```yaml
  redaction/redact:
    allow_all_keys: true               # If false, only allowed keys will be retained
    blocked_values:                    # List of regex patterns to block
      - '\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'       # Visa
      - '\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'  # MasterCard
    summary: debug                     # Show debug details about redaction
```

**`traces` パイプラインの更新**: 両方のProcessorを `traces` パイプラインに統合します。最初はredaction Processorをコメントアウトしておいてください（後の演習で有効にします）。

> [!NOTE]
> この演習では `redaction/redact` Processorをコメントアウトしたままにしてください。後の演習で有効にします。

```yaml
    traces:
      receivers:
      - otlp
      processors:
      - memory_limiter
      - attributes/update              # Update, hash, and remove attributes
      #- redaction/redact               # Redact sensitive fields using regex
      - resourcedetection
      - resource/add_mode
      - batch
      exporters:
      - debug
      - file
      - otlphttp
```

{{% /notice %}}

**[otelbin.io](https://www.otelbin.io/)** を使用してエージェント設定を検証します。参考として、パイプラインの `traces:` セクションは以下のようになります:

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRML(memory_limiter<br>fa:fa-microchip):::processor
      PRRD(resourcedetection<br>fa:fa-microchip):::processor
      PRRS(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRBA(batch<br>fa:fa-microchip):::processor
      PRUP(attributes<br>fa:fa-microchip<br>update):::processor
      EXP1(otlphttp<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;debug&ensp;&ensp;<br>fa:fa-upload):::exporter
      EXP3(file<br>fa:fa-upload):::exporter

    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1["`**Traces**`"]
      direction LR
      REC1 --> PRML
      PRML --> PRUP
      PRUP --> PRRD
      PRRD --> PRRS
      PRRS --> PRBA
      PRBA --> EXP2
      PRBA --> EXP3
      PRBA --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
