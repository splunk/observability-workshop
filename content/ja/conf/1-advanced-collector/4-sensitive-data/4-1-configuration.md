---
title: 4.1 Configuration
linkTitle: 4.1 Configuration
weight: 1
---

このステップでは、`agent.yaml` を変更して `attributes` プロセッサーと `redaction` プロセッサーを追加します。これらのプロセッサーは、span 属性内の機密データがログ出力やエクスポートの前に適切に扱われるようにするのに役立ちます。

これまでに、コンソールに表示された一部の span 属性に個人情報や機密データが含まれていることに気づいた方もいるかもしれません。ここでは、こうした情報を効果的にフィルタリングして秘匿化するために必要なプロセッサーを設定します。

```text
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

{{% notice title="演習" style="green" icon="running" %}}

**Agent ターミナル** ウィンドウに切り替えて、エディターで `agent.yaml` ファイルを開いてください。テレメトリーデータのセキュリティとプライバシーを強化するため、2つのプロセッサーを追加します。

**1. `attributes` プロセッサーを追加する**: [**Attributes Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor) を使用すると、span 属性（タグ）の値を更新、削除、またはハッシュ化することで変更できます。これは、エクスポート前に機密情報を難読化する際に特に役立ちます。

このステップでは、以下を実施します。

1. `user.phone_number` 属性を静的な値 `("UNKNOWN NUMBER")` に **更新** します。
2. `user.email` 属性を **ハッシュ化** して、元のメールアドレスが露出しないようにします。
3. `user.password` 属性を **削除** して、span から完全に取り除きます。

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

**2. `redaction` プロセッサーを追加する**: [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor) は、クレジットカード番号やその他の個人を特定できる情報（PII）など、事前定義されたパターンに基づいて span 属性内の機密データを検出して秘匿化します。

このステップでは、以下を実施します。

- `allow_all_keys: true` を設定して、すべての属性が処理されるようにします（`false` に設定すると、明示的に許可されたキーのみが保持されます）。

- `blocked_values` に正規表現を定義して、**Visa** および **MasterCard** のクレジットカード番号を検出して秘匿化します。

- `summary: debug` オプションは、デバッグ目的で秘匿化処理に関する詳細情報をログに記録します。

```yaml
  redaction/redact:
    allow_all_keys: true               # If false, only allowed keys will be retained
    blocked_values:                    # List of regex patterns to block
      - '\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'       # Visa
      - '\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'  # MasterCard
    summary: debug                     # Show debug details about redaction
```

**`traces` パイプラインを更新する**: 両方のプロセッサーを `traces` パイプラインに統合します。最初は redaction プロセッサーをコメントアウトしておくようにしてください（後の別の演習で有効化します）。設定は次のようになります。

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

<!--
Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces:` section of your pipelines will look similar to this:

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
      REC1 -- > PRML
      PRML -- > PRUP
      PRUP -- > PRRD
      PRRD -- > PRRS
      PRRS -- > PRBA
      PRBA -- > EXP2
      PRBA -- > EXP3
      PRBA -- > EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
-->
