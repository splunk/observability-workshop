---
title: 2. Building In Resilience
linkTitle: 2. Building Resilience
time: 10 minutes
weight: 4
---

OpenTelemetry Collector の [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) は、より回復力のあるテレメトリーパイプラインを構築するための重要なコンポーネントです。この機能により、Collector は処理中のデータを確実にチェックポイントし、リトライを効率的に管理し、一時的な障害発生時にも貴重なテレメトリーを失うことなく適切に対処できます。

FileStorage を有効にすると、Collector は中間状態をディスクに永続化できるため、ネットワークの中断、バックエンドの停止、または Collector の再起動が発生しても、トレース、メトリクス、ログが失われないことが保証されます。つまり、ネットワーク接続が切断されたり、バックエンドが一時的に利用不可になったりしても、Collector はテレメトリーの受信とバッファリングを継続し、接続が復旧次第シームレスに配信を再開します。

FileStorage Extension をパイプラインに統合することで、オブザーバビリティスタックの耐久性を強化し、接続が不安定になりがちな環境においても、高品質なテレメトリーの取り込みを維持できます。
{{% notice note %}}

このソリューションは、メトリクスについては接続のダウンタイムが短時間（最大 15 分）であれば機能します。ダウンタイムがこれを超えると、Splunk Observability Cloud はデータポイントの順序が乱れないようにするため、データを破棄する可能性があります。

ログについては、今後の Splunk OpenTelemetry Collector のリリースで、エンタープライズ対応の完全なソリューションを実装する計画があります。

{{% /notice %}}
