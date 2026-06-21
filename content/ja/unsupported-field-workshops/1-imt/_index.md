---
title: Splunk IM
linkTitle: Splunk IM
description: Splunkは、完全な可視性によりインフラストラクチャのパフォーマンスを最大化するためのリアルタイム監視とトラブルシューティングを提供します。
weight: 1
---

この _**テクニカル**_ Splunk Observability Cloud Infrastructure Monitoring および APM ワークショップでは、[軽量な](https://k3s.io/) Kubernetes[^1] クラスターをベースとした環境を構築します。

ワークショップモジュールを簡素化するために、事前設定済みの AWS/EC2 インスタンスが提供されます。

このインスタンスには、Kubernetes に Splunk OpenTelemetry Connector[^2] をデプロイし、NGINX^3 ReplicaSet^4 をデプロイし、最終的にメトリクス、トレース、スパン、ログ[^5]を送信するために OpenTelemetry を使用して計装されたマイクロサービスベースのアプリケーションをデプロイするために必要なすべてのソフトウェアが事前設定されています。

また、このワークショップでは、ダッシュボード、チャートの編集と作成、アラートを発報するディテクターの作成、Monitoring as Code、Service Bureau[^6] についても紹介します。

これらのテクニカルワークショップを終了する頃には、Splunk Observability Cloud の主要な機能と能力についてよく理解できるようになります。

事前設定済みの [AWS](./initial-setup/)/[EC2 インスタンス](./initial-setup/)へのアクセス方法はこちらです。

![Splunk Architecture](images/architecture.png)

[^1]: [**Kubernetes**](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) は、コンテナ化されたワークロードとサービスを管理するための、ポータブルで拡張可能なオープンソースプラットフォームであり、宣言的な構成と自動化の両方を促進します。
[^2]: [**OpenTelemetry Collector**](https://opentelemetry.io/) は、テレメトリデータの受信、処理、エクスポートの方法について、ベンダーに依存しない実装を提供します。さらに、オープンソースのテレメトリデータ形式（例：Jaeger、Prometheus など）を複数のオープンソースまたは商用バックエンドに送信するために、複数のエージェント/コレクターを実行、運用、保守する必要がなくなります。
[^5]: [**Jaeger**](https://www.jaegertracing.io/) は、Dapper と OpenZipkin に触発され、Uber Technologies によってオープンソースとしてリリースされた分散トレーシングシステムです。マイクロサービスベースの分散システムの監視とトラブルシューティングに使用されます。
[^6]: [**Monitoring as Code and Service Bureau**](https://www.splunk.com/en_us/blog/it/monitoring-observability-enterprise-service.html)
