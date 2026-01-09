---
title: Ingest Pipeline の作成
linkTitle: 3. Ingest Pipeline の作成
weight: 1
---

## シナリオ概要

このシナリオでは、組織の Splunk Enterprise Cloud 環境の管理を担当する Splunk 管理者の役割を担います。最近、社内のアプリケーションチームと協力して、重要なマイクロサービスアプリケーションを監視するために、OpenTelemetry を使用して Splunk APM と Infrastructure Monitoring で Kubernetes 環境を計装しました。

Kubernetes 環境からのログも収集され、Splunk Enterprise Cloud に送信されています。これらのログには以下が含まれます：

* Pod ログ（アプリケーションログ）
* Kubernetes Events
* Kubernetes Cluster ログ
  * Control Plane Node ログ
  * Worker Node ログ
  * Audit ログ

Splunk 管理者として、収集しているデータが最適化されていることを確認し、可能な限り効率的な方法で分析できるようにしたいと考えています。このアプローチを採用することで、トラブルシューティングが加速され、ライセンスの効率的な利用が確保されます。

これを達成する1つの方法は、Ingest Processor を使用して充実したログをメトリクスに変換し、それらのメトリクスの宛先として Splunk Observability Cloud を使用することです。これにより、ログの収集がより効率的になるだけでなく、新しく作成されたメトリクスを Splunk Observability で使用できるようになり、Splunk APM データ（トレース）や Splunk Infrastructure Monitoring データと相関させて、追加のトラブルシューティングコンテキストを提供できます。Splunk Observability Cloud はストリーミングメトリクスパイプラインを使用しているため、メトリクスに対してリアルタイムでアラートを設定でき、問題の特定を高速化できます。さらに、Metrics Pipeline Management 機能を使用して、集約、不要なフィールドの削除、重要度の低いまたは不要なメトリクスのアーカイブによってデータをさらに最適化できます。

次のステップでは、Kubernetes Audit ログを Observability Cloud に送信されるメトリクスに変換する Ingest Processor Pipeline を作成します。
