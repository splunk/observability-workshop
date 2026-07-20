---
title: 2. レジリエンスの組み込み
linkTitle: 2. レジリエンスの構築
time: 10 minutes
weight: 4
---

OpenTelemetry Collectorの [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) は、より耐障害性の高いテレメトリパイプラインを構築するための重要なコンポーネントです。Collectorが処理中のデータを確実にチェックポイントし、リトライを効率的に管理し、貴重なテレメトリを失うことなく一時的な障害を適切に処理できるようにします。

FileStorageを有効にすると、Collectorは中間状態をディスクに永続化できるため、ネットワークの中断、バックエンドの障害、またはCollectorの再起動時にTrace、Metric、ログが失われることがありません。ネットワーク接続が切断されたり、バックエンドが一時的に利用できなくなった場合でも、Collectorはテレメトリの受信とバッファリングを継続し、接続が復旧すると配信をシームレスに再開します。

FileStorage Extensionをパイプラインに統合することで、オブザーバビリティスタックの耐久性を強化し、接続が不安定な環境でも高品質なテレメトリの取り込みを維持できます。
{{% notice note %}}

このソリューションは、接続のダウンタイムが短い場合（最大15分）にMetricに対して機能します。ダウンタイムがこれを超える場合、Splunk Observability Cloudはデータポイントの順序が乱れないようにデータをドロップする可能性があります。

ログについては、今後のSplunk OpenTelemetry Collectorリリースで完全なエンタープライズ対応ソリューションを実装する計画があります。

{{% /notice %}}
