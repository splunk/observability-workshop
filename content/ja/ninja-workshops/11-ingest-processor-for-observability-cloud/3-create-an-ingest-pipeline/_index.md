---
title: Ingest Pipeline の作成
linkTitle: 3. Ingest Pipeline の作成
weight: 1
---

## シナリオ概要

このシナリオでは、組織のSplunk Enterprise Cloud環境の管理を担当するSplunk管理者の役割を担います。最近、社内のアプリケーションチームと協力して、重要なマイクロサービスアプリケーションを監視するために、OpenTelemetryを使用してSplunk APMとInfrastructure MonitoringでKubernetes環境を計装しました。

Kubernetes環境からのログも収集され、Splunk Enterprise Cloudに送信されています。これらのログには以下が含まれます：

* Podログ（アプリケーションログ）
* Kubernetes Events
* Kubernetes Clusterログ
  * Control Plane Nodeログ
  * Worker Nodeログ
  * Auditログ

Splunk管理者として、収集しているデータが最適化されていることを確認し、可能な限り効率的な方法で分析できるようにしたいと考えています。このアプローチを採用することで、トラブルシューティングが加速され、ライセンスの効率的な利用が確保されます。

これを達成する1つの方法は、Ingest Processorを使用して充実したログをメトリクスに変換し、それらのメトリクスの宛先としてSplunk Observability Cloudを使用することです。これにより、ログの収集がより効率的になるだけでなく、新しく作成されたメトリクスをSplunk Observabilityで使用できるようになり、Splunk APMデータ（トレース）やSplunk Infrastructure Monitoringデータと相関させて、追加のトラブルシューティングコンテキストを提供できます。Splunk Observability Cloudはストリーミングメトリクスパイプラインを使用しているため、メトリクスに対してリアルタイムでアラートを設定でき、問題の特定を高速化できます。さらに、Metrics Pipeline Management機能を使用して、集約、不要なフィールドの削除、重要度の低いまたは不要なメトリクスのアーカイブによってデータをさらに最適化できます。

次のステップでは、Kubernetes AuditログをObservability Cloudに送信されるメトリクスに変換するIngest Processor Pipelineを作成します。
