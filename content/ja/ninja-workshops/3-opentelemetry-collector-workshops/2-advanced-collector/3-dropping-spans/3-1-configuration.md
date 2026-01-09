---
title: 3.1 設定
linkTitle: 3.1 設定
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway terminal** ウィンドウに切り替えて、`gateway.yaml` ファイルを開きます。以下の設定で `processors` セクションを更新します：

1. **`filter` プロセッサを追加する**：
   `/_healthz` という名前のSpanを除外するようにGatewayを設定します。`error_mode: ignore` ディレクティブは、フィルタリング中に発生したエラーを無視し、パイプラインがスムーズに動作し続けることを保証します。`traces` セクションはフィルタリングルールを定義し、`/_healthz` という名前のSpanを除外対象として指定します。

   ```yaml
     filter/health:                       # Defines a filter processor
       error_mode: ignore                 # Ignore errors
       traces:                            # Filtering rules for traces
         span:                            # Exclude spans named "/_healthz"
          - 'name == "/_healthz"'
   ```

2. **`traces` パイプラインに `filter` プロセッサを追加する**：
   `traces` パイプラインに `filter/health` プロセッサを追加します。最適なパフォーマンスを得るために、フィルターはできるだけ早い段階に配置します。`memory_limiter` の直後、`batch` プロセッサの前に配置してください。設定は次のようになります：

   ```yaml
     traces:
       receivers:
         - otlp
       processors:
         - memory_limiter
         - filter/health             # Filters data based on rules
         - resource/add_mode
         - batch
       exporters:
         - debug
         - file/traces
   ```

この設定により、ヘルスチェック関連のSpan（`/_healthz`）がパイプラインの早い段階でフィルタリングされ、テレメトリーデータの不要なノイズが削減されます。

{{% /notice %}}

**[otelbin.io](https://www.otelbin.io/)** を使用してAgent設定を検証します。参考として、パイプラインの `traces:` セクションは次のようになります：

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO4(filter<br>fa:fa-microchip<br>health):::processor
      PRO5(batch<br>fa:fa-microchip):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(&ensp;&ensp;file&ensp;&ensp;<br>fa:fa-upload<br>traces):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[**Traces**]
      direction LR
      REC1 --> PRO1
      PRO1 --> PRO4
      PRO4 --> PRO3
      PRO3 --> PRO5
      PRO5 --> EXP1
      PRO5 --> EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
