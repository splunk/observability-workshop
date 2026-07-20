---
title: 4. 機密データの秘匿化
linkTitle: 4. 機密データ
time: 10 minutes
weight: 6
---

このセクションでは、OpenTelemetry Collectorを設定して、テレメトリSpanから特定のタグを削除し、機密データを秘匿化する方法を学びます。これは、クレジットカード番号、個人データ、その他のセキュリティ関連の情報など、処理やエクスポートの前に匿名化する必要がある機密情報を保護するために重要です。

OpenTelemetry Collectorの主要なProcessorの設定について説明します

- **[Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)**: 特定のSpan属性を変更または削除します。
- [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md): 機密データが保存または送信される前にサニタイズされることを保証します。

{{% exercise title="`4-sensitive-data` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `4-sensitive-data` ディレクトリに変更し、`clear` コマンドを実行してください。**

`3-dropping-spans` ディレクトリから `4-sensitive-data` に `*.yaml` をコピーします。更新後のディレクトリ構造は次のようになります

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}
