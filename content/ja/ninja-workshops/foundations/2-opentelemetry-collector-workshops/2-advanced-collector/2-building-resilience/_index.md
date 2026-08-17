---
title: 2. 耐障害性の構築
linkTitle: 2. Building Resilience
time: 10 minutes
weight: 4
---

OpenTelemetry Collector の [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) は、より耐障害性の高いテレメトリーパイプラインを構築するための重要なコンポーネントです。これにより、Collector は処理中のデータを確実にチェックポイントし、リトライを効率的に管理し、貴重なテレメトリーを失うことなく一時的な障害を適切に処理できます。

FileStorage を有効にすると、Collector は中間状態をディスクに永続化できるため、ネットワークの中断、バックエンドの停止、または Collector の再起動時にもトレース、メトリクス、ログが失われないことが保証されます。つまり、ネットワーク接続が切断されたり、バックエンドが一時的に利用できなくなったりしても、Collector はテレメトリーの受信とバッファリングを継続し、接続が復旧すると配信をシームレスに再開します。

FileStorage Extension をパイプラインに統合することで、オブザーバビリティスタックの耐久性を強化し、接続が不安定な環境でも高品質なテレメトリー取り込みを維持できます。
{{% notice note %}}

このソリューションは、接続ダウンタイムが短い場合（最大15分）のメトリクスに対して機能します。ダウンタイムがこれを超えると、Splunk Observability Cloud はデータポイントの順序が乱れないようにデータをドロップする可能性があります。

ログについては、今後の Splunk OpenTelemetry Collector リリースで完全なエンタープライズ対応ソリューションを実装する計画があります。

{{% /notice %}}
