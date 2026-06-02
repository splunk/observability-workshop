---
title: 6. 機密データの編集
linkTitle: 6. 機密データ
time: 10 minutes
weight: 8
---

このセクションでは、OpenTelemetry Collector を設定して特定のタグを削除し、テレメトリー span から機密データを編集する方法を学びます。これは、クレジットカード番号、個人情報、またはその他のセキュリティ関連の詳細など、処理またはエクスポートされる前に匿名化する必要がある機密情報を保護するために重要です。

OpenTelemetry Collector の主要なプロセッサーの設定方法を説明します。具体的には次のものです。

- **[Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)**: 特定の span 属性を変更または削除します。
- [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md): 機密データが保存または送信される前にサニタイズされることを保証します。

{{% notice title="演習" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`6-sensitive-data` という名前の新しいサブディレクトリを作成します。
- 次に、`5-dropping-spans` ディレクトリから `*.yaml` を `6-sensitive-data` にコピーします。

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `[WORKSHOP]/6-sensitive-data` ディレクトリに変更してください。**

更新後のディレクトリ構造は次のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
