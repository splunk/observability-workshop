---
title: 5.1 Configuration
linkTitle: 5.1 Configuration
weight: 1
---

{{% notice title="演習" style="green" icon="running" %}}

**Gateway ターミナル** ウィンドウに切り替え、`gateway.yaml` ファイルを開いてください。`processors` セクションを以下の設定で更新します。

1. **`filter` プロセッサーを追加する**:  
   `/_healthz` という名前のスパンを除外するように Gateway を設定します。`error_mode: ignore` ディレクティブは、フィルタリング中に発生したエラーを無視し、パイプラインが問題なく稼働し続けることを保証します。`traces` セクションではフィルタリングルールを定義しており、特に `/_healthz` という名前のスパンを除外対象とします。

   ```yaml
   filter/health:                       # Defines a filter processor
     error_mode: ignore                 # Ignore errors
     traces:                            # Filtering rules for traces
       span:                            # Exclude spans named "/_healthz"
         - 'name == "/_healthz"'
   ```

2. **`filter` プロセッサーを `traces` パイプラインに追加する**:  
   `filter/health` プロセッサーを `traces` パイプラインに含めます。最適なパフォーマンスを得るために、フィルターはできるだけ早い段階、つまり `memory_limiter` の直後、`batch` プロセッサーの前に配置します。設定は以下のようになります。

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

この構成により、ヘルスチェック関連のスパン (`/_healthz`) がパイプラインの早い段階で除外され、テレメトリーデータ内の不要なノイズが削減されます。

{{% /notice %}}

**[otelbin.io](https://www.otelbin.io/)** を使用してエージェントの設定を検証してください。参考までに、パイプラインの `traces:` セクションは以下のようになります。

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
      subgraph subID1["`**Traces**`"]
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
