---
title: 1.3 File Exporter
linkTitle: 1.3 File Exporter
weight: 2
---

画面上のデバッグ出力だけでなく、パイプラインのエクスポートフェーズでも出力を生成したい場合があります。そのために、比較用にOTLPデータをファイルに書き込む **File Exporter** を追加します。

OpenTelemetryの **debug exporter** と **file exporter** の違いは、目的と出力先にあります。

| 機能             | Debug Exporter                  | File Exporter                 |
|---------------------|---------------------------------|-------------------------------|
| **出力先** | コンソール/ログ                     | ディスク上のファイル                  |
| **目的**         | リアルタイムデバッグ             | 永続的なオフライン分析   |
| **最適な用途**        | テスト中の素早い確認 | 一時的な保存と共有 |
| **本番利用**  | いいえ                              | まれだが可能            |
| **永続性**     | なし                              | あり                           |

まとめると、 **Debug Exporter** はリアルタイムの開発中トラブルシューティングに最適であり、 **File Exporter** はテレメトリデータをローカルに保存して後で使用する場合に適しています。

{{% notice title="演習" style="green" icon="running" %}}

**Agent terminal** ウィンドウでCollectorが実行されていないことを確認し、`agent.yaml` を編集して **File Exporter** を設定します。

1. **`file` exporterの設定**: [**File Exporter**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/fileexporter/README.md)はテレメトリデータをディスク上のファイルに書き込みます。

    ```yaml
      file:                                # File Exporter
        path: "./agent.out"                # Save path (OTLP/JSON)
        append: false                      # Overwrite the file each time
    ```

1. **Pipelinesセクションの更新**: `file` exporterを `traces` パイプラインにのみ追加します。

    ```yaml
      pipelines:
        traces:
          receivers:
          - otlp                           # OTLP Receiver
          processors:
          - memory_limiter                 # Memory Limiter processor
          - resourcedetection              # Add system attributes to the data
          - resource/add_mode              # Add collector mode metadata
          exporters:
          - debug                          # Debug Exporter
          - file                           # File Exporter
        metrics:
          receivers:
          - otlp
          processors:
          - memory_limiter
          - resourcedetection
          - resource/add_mode
          exporters:
          - debug
        logs:
          receivers:
          - otlp
          processors:
          - memory_limiter
          - resourcedetection
          - resource/add_mode
          exporters:
          - debug
    ```

{{% /notice %}}

[**https://otelbin.io**](https://otelbin.io/)を使用してエージェント設定を検証します。

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
      EXP2(&ensp;file&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1["`**Traces**`"]
      direction LR
      REC1 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> EXP1
      PRO3 --> EXP2
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fbbf24,stroke-width:1px, color:#fbbf24,stroke-dasharray: 3 3;
```
