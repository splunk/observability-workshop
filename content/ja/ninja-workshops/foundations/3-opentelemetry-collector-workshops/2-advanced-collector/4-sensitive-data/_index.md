---
title: 4. 機密データの編集
linkTitle: 4. 機密データ
time: 10 minutes
weight: 6
---

このセクションでは、OpenTelemetry Collector を設定して特定のタグを削除し、テレメトリスパンから機密データを編集する方法を学びます。これは、クレジットカード番号、個人データ、その他セキュリティ関連の詳細など、処理または送信される前に匿名化する必要がある機密情報を保護するために重要です。

OpenTelemetry Collector の主要なプロセッサーの設定方法を確認していきます。具体的には次のとおりです。

- **[Attributes Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)**: 特定のスパン属性を変更または削除します。
- [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md): 機密データが保存または送信される前にサニタイズされていることを保証します。

{{% exercise title="`4-sensitive-data` ディレクトリのセットアップ" %}}

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `4-sensitive-data` ディレクトリに移動し、`clear` コマンドを実行してください。**

`3-dropping-spans` ディレクトリから `*.yaml` を `4-sensitive-data` にコピーします。更新されたディレクトリ構造は次のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /exercise %}}
