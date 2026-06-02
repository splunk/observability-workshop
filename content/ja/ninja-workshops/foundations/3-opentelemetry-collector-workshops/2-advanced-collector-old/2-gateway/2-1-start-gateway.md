---
title: 2.1 Start Gateway
linkTitle: 2.1 Start Gateway
weight: 1
---

`gateway` の設定は、機能させるために追加の設定変更を必要としません。これは、時間を節約し、**Gateway** の中核となる概念に集中するためです。

**[otelbin.io](https://www.otelbin.io/)** を使用して `gateway` の設定を検証します。参考までに、パイプラインの `logs:` セクションは次のようになります。

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resource<br>fa:fa-microchip<br>add_mode):::processor
      PRO3(batch<br>fa:fa-microchip):::processor
      EXP1(&ensp;file&ensp;<br>fa:fa-upload<br>logs):::exporter
      EXP2(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-logs
    subgraph " "
      subgraph subID1[**Logs**]
      direction LR
      REC1 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> EXP2
      PRO3 --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-logs stroke:#34d399,stroke-width:1px, color:#34d399,stroke-dasharray: 3 3;
```

{{% notice title="演習" style="green" icon="running" %}}

**Gateway の起動**: **Gateway ターミナル** ウィンドウで、次のコマンドを実行して `gateway` を起動します。

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

すべて正しく設定されていれば、出力の最初と最後の行は次のようになります。

```text
2025/01/15 15:33:53 settings.go:478: Set config to [gateway.yaml]
<snip to the end>
2025-01-13T12:43:51.747+0100 info service@v0.120.0/service.go:261 Everything is ready. Begin running and processing data.
```

{{% /notice %}}

次に、新しく作成した `gateway` にデータを送信するように `agent` を設定します。
