---
title: OpenTelemetryとSplunkにおける、タグ付けのための命名規則
linkTitle: OpenTelemetryでのタグ付け
description: 大規模な組織で OpenTelemetry を展開する際には、タグ付けのための標準化された命名規則を定義し、規則が遵守されるようにガバナンスプロセスを確立することが重要です。
weight: 3
---

## はじめに

大規模な組織でOpenTelemetryを展開する際には、タグ付けのための標準化された命名規則を定義し、その規則が遵守されるようにガバナンスプロセスを設定することが非常に重要です。

これにより、OpenTelemetryを通じて収集されるMELTデータ（メトリクス、イベント、ログ、トレース）を、アラート、ダッシュボード作成、トラブルシューティングの目的で効率的に活用することが可能になります。また、Splunk Observability Cloudのユーザーが探しているデータを迅速に見つけることができます。

命名規則はまた、データを効果的に集約するためにも重要です。例えば、環境ごとのユニークなホストの数を数えたい場合、ホスト名と環境名を捉えるための標準化された規則を使用する必要があります。

## 属性 vs タグ

先に進む前に、用語についての注意をしておきましょう。OpenTelemetryの「タグ」は「属性（attribute）」と呼ばれます。属性は、手動または自動の計装を通じて、メトリクス、ログ、トレースに添付することができます。

属性はまた、[Resource Detection processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor)などのさまざまなプロセッサを使用して、OpenTelemetryコレクターレベルでメトリクス、ログ、トレースに添付することもできます。

Splunk Observability Cloudに属性付きのトレースが取り込まれると、それらは「タグ」として利用可能になります。オプションとして、トレースの一部として収集された属性は、[Troubleshooting Metric Sets](https://docs.splunk.com/Observability/apm/span-tags/metricsets.html#troubleshooting-metricsets)の作成に使用され、[Tag Spotlight](https://docs.splunk.com/Observability/apm/span-tags/tag-spotlight.html)などのさまざまな機能と共に使用することができます。

また、属性は[Monitoring Metric Sets](https://docs.splunk.com/Observability/apm/span-tags/metricsets.html#monitoring-metricsets)の作成に使用され、アラートのトリガーとして使用することもできます。

## リソースに関するセマンティック規約

[OpenTelemetry リソースセマンティック規約](https://github.com/open-telemetry/opentelemetry-specification/tree/main/specification/resource/semantic_conventions#resource-semantic-conventions)は、組織が標準化すべき属性を決定する際の出発点として使用できます。以下のセクションでは、よく使用される属性のいくつか見ていきましょう。

### サービス属性

監視されるサービスを記述するために多くの属性が使用されます。

`service.name` はサービスの論理名を定義する必須の属性です。OpenTelemetry SDKによって自動的に追加されますが、カスタマイズすることができます。これはシンプルに保つことが最善です（例えば、`inventoryservice` は `inventoryservice-prod-hostxyz` よりも良いでしょう。他の属性を使用してサービスの他の側面を捉えることができます）。

以下のサービス属性が推奨されます：

- `service.namespace` はサービスを所有するチームを識別するために使用されます
- `service.instance.id` はサービスのユニークなインスタンスを識別するために使用されます
- `service.version` はサービスのバージョンを識別するために使用されます

### テレメトリSDK

これらの属性はSDKによって自動的に設定され、使用されている計測ライブラリに関する情報を記録します：

- `telemetry.sdk.name` は通常 `opentelemetry` に設定されます。
- `telemetry.sdk.language` はSDKの言語で、例えば `java` です。
- `telemetry.sdk.version` は使用されているSDKのバージョンを識別します。

### コンテナ


コンテナで実行されるサービスには、`container.id`、`container.name`、`container.image.name` など、コンテナのランタイムを記述するための多くの属性が使用されます。完全なリストは[こちら](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/resource/semantic_conventions/container.md)で確認できます。

### ホスト

これらの属性は、サービスが実行されているホストを記述し、`host.id`、`host.name`、`host.arch` などの属性を含みます。完全なリストは[こちら](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/resource/semantic_conventions/host.md)で確認できます。

### デプロイ環境

`deployment.environment` 属性は、サービスがデプロイされている環境（**staging** や **production** など）を識別するために使用されます。

Splunk Observability Cloudは、この属性を使用して関連コンテンツを有効する（詳細は[こちら](https://docs.splunk.com/observability/metrics-and-metadata/enablerelatedcontent.html)）ため、この属性を含めることが重要です。

### クラウド

AWSなどのパブリッククラウド環境で実行されるサービスに関する情報を捉えるための属性もあります。これには、`cloud.provider`、`cloud.account.id`、`cloud.region` が含まれます。

属性の完全なリストは[こちら](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/resource/semantic_conventions/cloud.md)で確認できます。

一部のクラウドプロバイダー、例えば [GCP](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/resource/semantic_conventions/cloud_provider/gcp/README.md) は、独自のセマンティック規則を定義しています。

### Kubernetes


Kubernetesで実行されるアプリケーションにも、いくつかの標準化された属性があります。これらの多くは、SplunkのOpenTelemetryコレクター配布によって自動的に追加されます（詳細は[こちら](https://docs.splunk.com/observability/metrics-and-metadata/enablerelatedcontent.html#splunk-infrastructure-monitoring)）。

属性は、例えば `k8s.cluster.name`、`k8s.node.name`、`k8s.pod.name`、`k8s.namespace.name`、`kubernetes.workload.name` などがあります。

## カスタム属性のベストプラクティス

多くの組織では、OpenTelemetryのリソースセマンティック規約で定義されているもの以上の属性が欲しくなります。

この場合、セマンティック規約にすでに含まれている属性名との命名競合を避けることが重要です。つまり、特定の属性名を命名規則に決定する前に、セマンティック規約をチェックすると良いでしょう。

属性名の命名規則に加えて、属性値も考慮する必要があります。例えば、アプリケーションが属する特定のビジネスユニットをキャプチャしたい場合、簡単にかつ効果的にフィルタリングするために、標準化されたビジネスユニット値のリストも持ちたいでしょう。

OpenTelemetryコミュニティでは、属性の命名に従うべきガイドラインも提供しています。[こちら](https://opentelemetry.io/docs/specs/otel/common/attribute-naming/)で見つけることができます。

[Recommendations for Application Developers](https://opentelemetry.io/docs/specs/otel/common/attribute-naming/#recommendations-for-application-developers)は、私たちの議論に最も関連しています。

そこでは、以下を推奨しています：

* `com.acme.shopname` のように、会社のドメイン名で属性名を接頭辞として付けること（属性が社内だけでなく外部で使用される可能性がある場合）
* 属性が特定のアプリケーションに固有であり、組織内でのみ使用される場合は、アプリケーション名で属性名に接頭辞を付けること
* 既存のOpenTelemetryセマンティック規約の名前を属性名の接頭辞として使用しないこと
* 異なる組織や業界全体で一般的なニーズがある場合は、あなたの属性名をOpenTelemetry仕様に追加する提案を検討すること
* `otel.*` で始まる属性名は避けること。これはOpenTelemetry仕様の使用に予約されています

## カーディナリティに関する考慮事項

属性名と値の命名基準を決定する際に考慮すべき最後の点は、メトリクスのカーディナリティに関連しています。

のカーディナリティは、メトリクス名とそれに関連する次元の組み合わせによって生成されるユニークなメトリクス時系列（MTS: Metric Time Series）の数として定義されます。

メトリクスは、ディメンションの数とそれらのディメンションが持つユニークな値の数が多い場合に、高いカーディナリティを持つことになります。

例えば、あなたのアプリケーションが `custom.metric` という名前のメトリクスのデータを送信するとします。属性がない場合、`custom.metric` は単一のメトリクス時系列（MTS）を生成します。

一方で、`custom.metric` が `customer.id` という属性を含み、数千の顧客ID値がある場合、これは数千のメトリクス時系列を生成し、コストやクエリ性能に影響を与える可能性があります。

Splunk Observability Cloudは、メトリクスの使用量を管理するための[レポート](https://docs.splunk.com/Observability/infrastructure/metrics-pipeline/metrics-usage-report.html)を提供しています。そして、望ましくないディメンションを削除する[ルール](https://docs.splunk.com/Observability/infrastructure/metrics-pipeline/use-metrics-pipeline.html)を作成することができます。しかし、最初の防衛線は、属性名と値の組み合わせがどのようにメトリクスのカーディナリティを増加させるかを理解することです。

## まとめ

このドキュメントでは、大規模なOpenTelemetry計装の展開を開始する前に、OpenTelemetryタグの命名規則を定義することの重要性を強調しました。

OpenTelemetryのリソースセマンティック規約がいくつかの属性の命名規則を定義し、多くの属性がOpenTelemetry SDKやOpenTelemetryコレクター内で動作するプロセッサーを通じて自動的に収集される方法について説明しました。

最後に、リソースセマンティック規約が組織のニーズに十分でない場合に、属性名を作成するためのベストプラクティスを共有しました。
