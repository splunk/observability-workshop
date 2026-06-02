---
title: 1.1 Validation & Load Generation
linkTitle: 1.1 Validation & Load Generation
weight: 1
---

このワークショップでは、[**https://otelbin.io**](https://otelbin.io/) を使用して YAML 構文を素早く検証し、OpenTelemetry の構成が正確であることを確認します。このステップは、セッション中にテストを実行する前にエラーを回避するのに役立ちます。

{{% notice title="Exercise" style="green" icon="running" %}}
構成を検証する方法は次のとおりです。

1. [**https://otelbin.io**](https://otelbin.io/) を開き、左ペインに YAML を貼り付けて既存の構成を置き換えます。
    > [!INFO]
    > Mac を使用しており、Splunk Workshop インスタンスを使用していない場合は、次のコマンドを実行することで、`agent.yaml` ファイルの内容を素早くクリップボードにコピーできます。
    >
    > ```bash
    > cat agent.yaml | pbcopy
    > ```

2. ページの上部で、検証対象として **Splunk OpenTelemetry Collector** が選択されていることを確認してください。このオプションを選択し**ない**場合、UI に `Receiver "hostmetrics" is unused. (Line 8)` という警告が表示されます。

3. 検証が完了したら、以下の画像表現を参照して、パイプラインが正しく設定されていることを確認してください。

ほとんどの場合、**主要なパイプライン**のみを表示します。ただし、3 つのパイプライン (Traces、Metrics、Logs) すべてが同じ構造を共有している場合は、それぞれを個別に示すのではなく、その旨を記載します。

```mermaid
%%{init:{"fontFamily":"monospace"}}%%
graph LR
    %% Nodes
      REC1(&nbsp;&nbsp;otlp&nbsp;&nbsp;<br>fa:fa-download):::receiver
      PRO1(memory_limiter<br>fa:fa-microchip):::processor
      PRO2(resourcedetection<br>fa:fa-microchip):::processor
      PRO3(resource<br>fa:fa-microchip<br>add_mode):::processor
      EXP1(&ensp;debug&ensp;<br>fa:fa-upload):::exporter
    %% Links
    subID1:::sub-traces
    subgraph " "
      subgraph subID1[**Traces/Metrics/Logs**]
      direction LR
      REC1 --> PRO1
      PRO1 --> PRO2
      PRO2 --> PRO3
      PRO3 --> EXP1
      end
    end
classDef receiver,exporter fill:#8b5cf6,stroke:#333,stroke-width:1px,color:#fff;
classDef processor fill:#6366f1,stroke:#333,stroke-width:1px,color:#fff;
classDef con-receive,con-export fill:#45c175,stroke:#333,stroke-width:1px,color:#fff;
classDef sub-traces stroke:#fff,stroke-width:1px, color:#fff,stroke-dasharray: 3 3;
```

{{% /notice %}}

---

## Load Generation Tool

このワークショップのために、`loadgen` ツールを特別に開発しました。`loadgen` は、トレースおよびロギングアクティビティをシミュレートするための柔軟な負荷生成ツールです。デフォルトで base、health、security のトレースをサポートし、オプションでランダムな引用をプレーンテキストまたは JSON 形式でファイルにロギングする機能も備えています。

`loadgen` によって生成される出力は、OpenTelemetry インストルメンテーションライブラリによって生成されるものを模倣しており、Collector の処理ロジックをテストすることを可能にし、現実のシナリオを模倣するためのシンプルかつ強力な方法を提供します。
