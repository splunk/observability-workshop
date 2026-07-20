---
title: 6. 機密データのリダクション
linkTitle: 6. 機密データ
time: 10 minutes
weight: 8
---

このセクションでは、OpenTelemetry Collectorを設定して、テレメトリSpanから特定のタグを削除し、機密データをリダクションする方法を学びます。これは、クレジットカード番号、個人データ、その他のセキュリティ関連の詳細情報など、処理またはエクスポートされる前に匿名化する必要がある機密情報を保護するために不可欠です。

OpenTelemetry Collectorの主要なProcessorの設定について説明します

- **[Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)**: 特定のSpan属性を変更または削除します。
- [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md): 機密データが保存または送信される前にサニタイズされることを保証します。

{{% notice title="Exercise" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`6-sensitive-data` という名前の新しいサブディレクトリを作成します。
- 次に、`5-dropping-spans` ディレクトリから `*.yaml` を `6-sensitive-data` にコピーします。

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `[WORKSHOP]/6-sensitive-data` ディレクトリに変更してください。**

更新後のディレクトリ構造は次のようになります

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
