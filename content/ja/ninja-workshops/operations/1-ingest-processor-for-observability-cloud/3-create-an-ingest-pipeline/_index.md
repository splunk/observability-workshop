---
title: Ingest Pipelineの作成
linkTitle: 3. Ingest Pipelineの作成
weight: 1
---

## シナリオ概要

このシナリオでは、組織のSplunk Enterprise Cloud環境を管理するSplunk Adminの役割を担います。最近、社内のアプリケーションチームと協力し、OpenTelemetryを使用してKubernetes環境にSplunk APMとInfrastructure Monitoringを導入し、重要なマイクロサービスアプリケーションのモニタリングを行いました。

Kubernetes環境からのログも収集され、Splunk Enterprise Cloudに送信されています。これらのログには以下が含まれます

* Podログ（アプリケーションログ）
* Kubernetes Events
* Kubernetes Cluster Logs
  * Control Plane Nodeログ
  * Worker Nodeログ
  * Audit Logs

Splunk Adminとして、収集しているデータが最適化され、可能な限り効率的に分析できるようにする必要があります。このアプローチにより、トラブルシューティングが迅速化され、ライセンスの効率的な利用が確保されます。

これを実現する方法の1つは、Ingest Processorを使用してリッチなログをメトリクスに変換し、Splunk Observability Cloudをそのメトリクスの送信先として使用することです。これによりログの収集が効率化されるだけでなく、新しく作成されたメトリクスをSplunk Observabilityで使用できるようになり、Splunk APMデータ（トレース）やSplunk Infrastructure Monitoringデータと相関させることで、追加のトラブルシューティングコンテキストを提供できます。Splunk Observability Cloudはストリーミングメトリクスパイプラインを使用しているため、メトリクスに対してリアルタイムでアラートを設定でき、問題の特定が迅速化されます。さらに、Metrics Pipeline Management機能を使用して、集約、不要なフィールドの削除、重要度の低いメトリクスや不要なメトリクスのアーカイブにより、データをさらに最適化できます。

次のステップでは、Kubernetes Audit Logsをメトリクスに変換してObservability Cloudに送信するIngest Processor Pipelineを作成します。
