---
title: 7.1 設定
linkTitle: 7.1 設定
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}
**`transform` Processorの追加**: **Agentターミナル** ウィンドウに切り替え、`agent.yaml` を編集して以下の `transform` Processorを追加します:

```yaml
  transform/logs:                      # Processor Type/Name
    log_statements:                    # Log Processing Statements
      - context: resource              # Log Context
        statements:                    # List of attribute keys to keep
          - keep_keys(attributes, ["com.splunk.sourcetype", "host.name", "otelcol.service.mode"])
```

`-context: resource` キーを使用することで、ログの `resourceLog` 属性をターゲットにしています。

この設定により、関連するリソース属性（`com.splunk.sourcetype`、`host.name`、`otelcol.service.mode`）のみが保持され、ログの効率が向上し、不要なメタデータが削減されます。

**ログ重大度マッピングのためのContextブロックの追加**: ログレコードの `severity_text` と `severity_number` フィールドを適切に設定するために、`log_statements` 内に `log` Contextブロックを追加します。この設定は、ログ本文から `level` 値を抽出し、それを `severity_text` にマッピングし、ログレベルに基づいて対応する `severity_number` を割り当てます:

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

`merge_maps` 関数は、2つのマップ（辞書）を1つに結合するために使用されます。この場合、`cache` オブジェクト（ログ本文から解析されたJSONデータを含む）を `attributes` マップにマージします。

- **パラメータ**:
  - `attributes`: データがマージされるターゲットマップ。
  - `cache`: 解析されたJSONデータを含むソースマップ。
  - `"upsert"`: このモードは、`attributes` マップにキーが既に存在する場合、その値が `cache` の値で更新されることを保証します。キーが存在しない場合は、挿入されます。

このステップは、ログ本文からのすべての関連フィールド（例: `level`、`message` など）が `attributes` マップに追加され、さらなる処理やエクスポートで利用可能になることを保証するため、非常に重要です。

**主要な変換の概要**:

- **JSON解析**: ログ本文から構造化データを抽出します。
- **JSONフラット化**: ネストされたJSONオブジェクトをフラットな構造に変換します。
- **属性のマージ**: 抽出されたデータをログ属性に統合します。
- **重大度テキストのマッピング**: ログのlevel属性からseverity_textを割り当てます。
- **重大度番号の割り当て**: 重大度レベルを標準化された数値に変換します。

`resource` 用のContextブロックと `log` 用のContextブロックの2つを含む、**単一の** `transform` Processorが必要です。

この設定により、ログの重大度が正しく抽出、標準化、構造化され、効率的な処理が可能になります。

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
すべてのJSONフィールドをトップレベル属性にマッピングするこの方法は、**OTTLのテストとデバッグ** にのみ使用してください。本番環境では高カーディナリティを引き起こす可能性があります。
{{% /notice %}}

**`logs` パイプラインの更新**: `transform/logs:` Processorを `logs:` パイプラインに追加します:

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

[**https://otelbin.io**](https://otelbin.io/) を使用してAgent設定を検証します。参考として、パイプラインの `logs:` セクションは以下のようになります:

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
