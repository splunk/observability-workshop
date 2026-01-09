---
title: 4. 機密データの秘匿化
linkTitle: 4. 機密データ
time: 10 minutes
weight: 6
---

このセクションでは、OpenTelemetry Collector を設定して、テレメトリーSpanから特定のタグを削除し、機密データを秘匿化する方法を学びます。これは、クレジットカード番号、個人データ、その他のセキュリティ関連の詳細など、処理またはエクスポートする前に匿名化する必要がある機密情報を保護するために重要です。

OpenTelemetry Collector の主要なプロセッサの設定について説明します：

- **[Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)**：特定のSpan属性を変更または削除します。
- [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md)：機密データが保存または送信される前にサニタイズされることを保証します。

{{% notice title="Exercise" style="green" icon="running" %}}

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `4-sensitive-data` ディレクトリに移動し、`clear` コマンドを実行してください。**

`3-dropping-spans` ディレクトリから `*.yaml` を `4-sensitive-data` にコピーします。更新後のディレクトリ構造は次のようになります：

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
