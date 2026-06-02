---
title: 3.1 Configuration
linkTitle: 3.1 Configuration
weight: 1
---

{{% notice title="演習" style="green" icon="running" %}}

**Gateway terminal** ウィンドウに切り替えて、`gateway.yaml` ファイルを開いてください。`processors` セクションを以下の設定で更新します。

1. **`filter` プロセッサーを追加する**:  
   `/_healthz` という名前のスパンを除外するように Gateway を設定します。`error_mode: ignore` ディレクティブにより、フィルタリング中に発生したエラーは無視され、パイプラインは問題なく動作し続けます。`traces` セクションでフィルタリングルールを定義し、`/_healthz` という名前のスパンを除外対象として指定します。

   ```yaml
     filter/health:                       # Defines a filter processor
       error_mode: ignore                 # Ignore errors
       traces:                            # Filtering rules for traces
         span:                            # Exclude spans named "/_healthz"
          - 'name == "/_healthz"'
   ```

2. **`filter` プロセッサーを `traces` パイプラインに追加する**:  
   `filter/health` プロセッサーを `traces` パイプラインに含めます。最適なパフォーマンスを得るためには、フィルターをできるだけ早い段階、つまり `memory_limiter` の直後、`batch` プロセッサーの前に配置してください。設定は以下のようになります。

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

この設定により、ヘルスチェック関連のスパン (`/_healthz`) がパイプラインの早い段階でフィルタリングされ、テレメトリーデータの不要なノイズを削減できます。

{{% /notice %}}

<!--Validate the agent configuration using **[otelbin.io](https://www.otelbin.io/)**. For reference, the `traces:` section of your pipelines will look similar to this:-->

<!--
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
      REC1 -- > PRO1
      PRO1 -- > PRO4
      PRO4 -- > PRO3
      PRO3 -- > PRO5
      PRO5 -- > EXP1
      PRO5 -- > EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
-->