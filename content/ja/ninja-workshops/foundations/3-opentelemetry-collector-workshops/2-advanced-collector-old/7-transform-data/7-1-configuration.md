---
title: 7.1 Configuration
linkTitle: 7.1 Configuration
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}
**`transform` プロセッサーの追加**: **Agent terminal** ウィンドウに切り替えて `agent.yaml` を編集し、以下の `transform` プロセッサーを追加します。

```yaml
  transform/logs:                      # Processor Type/Name
    log_statements:                    # Log Processing Statements
      - context: resource              # Log Context
        statements:                    # List of attribute keys to keep
          - keep_keys(attributes, ["com.splunk.sourcetype", "host.name", "otelcol.service.mode"])
```

`-context: resource` キーを使用することで、ログの `resourceLog` 属性を対象としています。

この設定により、関連するリソース属性（`com.splunk.sourcetype`、`host.name`、`otelcol.service.mode`）のみが保持され、ログの効率が向上し、不要なメタデータが削減されます。

**ログ重大度マッピングのためのコンテキストブロックの追加**: ログレコードの `severity_text` および `severity_number` フィールドを適切に設定するために、`log_statements` 内に `log` コンテキストブロックを追加します。この設定では、ログ本文から `level` 値を抽出し、`severity_text` にマッピングして、ログレベルに対応する `severity_number` を割り当てます。

```yaml
      - context: log                   # Log Context
        statements:                    # Transform Statements Array
          - set(cache, ParseJSON(body)) where IsMatch(body, "^\\{")  # Parse JSON log body into a cache object
          - flatten(cache, "")                                        # Flatten nested JSON structure
          - merge_maps(attributes, cache, "upsert")                   # Merge cache into attributes, updating existing keys
          - set(severity_text, attributes["level"])                   # Set severity_text from the "level" attribute
          - set(severity_number, 1) where severity_text == "TRACE"    # Map severity_text to severity_number
          - set(severity_number, 5) where severity_text == "DEBUG"
          - set(severity_number, 9) where severity_text == "INFO"
          - set(severity_number, 13) where severity_text == "WARN"
          - set(severity_number, 17) where severity_text == "ERROR"
          - set(severity_number, 21) where severity_text == "FATAL"
```

`merge_maps` 関数は、2つのマップ（ディクショナリ）を1つに結合するために使用されます。ここでは、`cache` オブジェクト（ログ本文から解析された JSON データを含む）を `attributes` マップにマージします。

- **パラメータ**:
  - `attributes`: データがマージされる対象のマップです。
  - `cache`: 解析された JSON データを含むソースマップです。
  - `"upsert"`: このモードでは、`attributes` マップ内にキーが既に存在する場合、その値が `cache` の値で更新されます。キーが存在しない場合は挿入されます。

このステップは非常に重要で、ログ本文に含まれるすべての関連フィールド（例: `level`、`message` など）が `attributes` マップに追加され、後続の処理やエクスポートで利用可能になることを保証します。

**主な変換処理のまとめ**:

- **JSON の解析**: ログ本文から構造化データを抽出します。
- **JSON のフラット化**: ネストされた JSON オブジェクトをフラットな構造に変換します。
- **属性のマージ**: 抽出したデータをログの属性に統合します。
- **重大度テキストのマッピング**: ログの level 属性から severity_text を割り当てます。
- **重大度番号の割り当て**: 重大度レベルを標準化された数値に変換します。

最終的に、`resource` 用と `log` 用の2つのコンテキストブロックを含む **1つの** `transform` プロセッサーが構成されている必要があります。

この設定により、ログの重大度が正しく抽出、標準化、構造化され、効率的な処理が可能になります。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
すべての JSON フィールドをトップレベル属性にマッピングするこの方法は、**OTTL のテストとデバッグ** にのみ使用してください。本番環境のシナリオでは高カーディナリティを引き起こします。
{{% /notice %}}

**`logs` パイプラインの更新**: `transform/logs:` プロセッサーを `logs:` パイプラインに追加します。

```yaml
    logs:
      receivers:
      - otlp
      - filelog/quotes
      processors:
      - memory_limiter
      - resourcedetection
      - resource/add_mode
      - transform/logs                 # Transform logs processor
      - batch
      exporters:
      - debug
      - otlphttp
```

{{% /notice %}}

[**https://otelbin.io**](https://otelbin.io/) を使用してエージェント設定を検証します。参考までに、パイプラインの `logs:` セクションは以下のようになります。

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      REC2(filelog<br>fa:fa-download<br>quotes):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(transform<br>fa:fa-microchip<br>logs):::processor
      PRO5(batch<br>fa:fa-microchip):::processor
      EXP1(otlphttp<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;debug&ensp;&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-logs
    subgraph " "
      subgraph subID1[**Logs**]
      direction LR
      REC1 --> PRO1
      REC2 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> PRO4
      PRO4 --> PRO5
      PRO5 --> EXP2
      PRO5 --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-logs stroke:#34d399,stroke-width:1px, color:#34d399,stroke-dasharray: 3 3;
```
