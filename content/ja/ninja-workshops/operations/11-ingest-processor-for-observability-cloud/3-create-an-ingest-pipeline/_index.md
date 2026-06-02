---
title: Create an Ingest Pipeline
linkTitle: 3. Create an Ingest Pipeline
weight: 1
---

## シナリオ概要

このシナリオでは、組織の Splunk Enterprise Cloud 環境を管理する Splunk 管理者の役割を担います。最近、社内のアプリケーションチームと協力し、重要なマイクロサービスアプリケーションを監視するために、OpenTelemetry を使用して Kubernetes 環境を Splunk APM および Infrastructure Monitoring で計装しました。

Kubernetes 環境のログも収集され、Splunk Enterprise Cloud に送信されています。これらのログには次のものが含まれます。

* Pod ログ (アプリケーションログ)
* Kubernetes Events
* Kubernetes クラスターログ
  * Control Plane ノードログ
  * Worker ノードログ
  * 監査ログ (Audit Logs)

Splunk 管理者として、収集しているデータが最適化され、できるだけ効率的に分析できるようにしたいと考えています。このアプローチをとることで、トラブルシューティングが迅速化され、ライセンスの効率的な利用が確保されます。

これを実現する方法の 1 つは、Ingest Processor を使用して大量のログをメトリクスに変換し、それらのメトリクスの送信先として Splunk Observability Cloud を使用することです。これにより、ログ収集がより効率的になるだけでなく、新しく作成したメトリクスを Splunk Observability で利用できるようになり、Splunk APM データ (トレース) や Splunk Infrastructure Monitoring データと相関付けて、追加のトラブルシューティングコンテキストを提供できます。Splunk Observability Cloud はストリーミングメトリクスパイプラインを使用しているため、メトリクスに対してリアルタイムでアラートを発行でき、問題の特定が迅速化されます。さらに、Metrics Pipeline Management 機能を使用して、データを集約したり、不要なフィールドを削除したり、重要度の低いメトリクスや不要なメトリクスをアーカイブしたりすることで、データをさらに最適化できます。

次のステップでは、Kubernetes 監査ログをメトリクスに変換し、Observability Cloud に送信する Ingest Processor パイプラインを作成します。
