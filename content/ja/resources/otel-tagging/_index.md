---
title: Naming Conventions for Tagging with OpenTelemetry and Splunk
linkTitle: OpenTelemetry Tagging
description: 大規模なデプロイメントにおける OpenTelemetry タグの命名規則とガバナンスパターンについて解説します。
weight: 4
---

## はじめに

大規模な組織で OpenTelemetry を導入する際は、タグ付けに関する標準化された命名規則を定義し、その規則が遵守されるようガバナンスプロセスを整備することが極めて重要です。

これにより、OpenTelemetry を通じて収集された MELT データを、アラート、ダッシュボード、トラブルシューティングの目的で効率的に活用できるようになります。また、Splunk Observability Cloud のユーザーが必要なデータを素早く見つけられるようにもなります。

命名規則は、データを効果的に集約することにも寄与します。たとえば、環境ごとに一意なホストの数をカウントしたい場合、ホスト名と環境名を取得するための標準化された規則を使う必要があります。

## Attributes と Tags

本題に入る前に、用語について整理しておきます。OpenTelemetry におけるタグは「attributes」（属性）と呼ばれます。Attributes は、手動計装または自動計装を通じて、メトリクス、ログ、トレースに付与できます。

Attributes は、[Resource Detection processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor) などのさまざまなプロセッサを使用して、OpenTelemetry collector のレベルでメトリクス、ログ、トレースに付与することもできます。

Attributes が付与されたトレースが Splunk Observability Cloud に取り込まれると、それらは「tags」として利用できるようになります。オプションとして、トレースの一部として収集された attributes を [Troubleshooting Metric Sets](https://docs.splunk.com/Observability/apm/span-tags/metricsets.html#troubleshooting-metricsets) の作成に利用でき、それを [Tag Spotlight](https://docs.splunk.com/Observability/apm/span-tags/tag-spotlight.html) などのさまざまな機能で活用できます。

あるいは、attributes を [Monitoring Metric Sets](https://docs.splunk.com/Observability/apm/span-tags/metricsets.html#monitoring-metricsets) の作成に利用して、アラート機能を駆動することもできます。

## Resource Semantic Conventions

組織がどの attributes を標準化すべきかを判断する際の出発点として、[OpenTelemetry resource semantic conventions](https://github.com/open-telemetry/semantic-conventions/tree/main) を参照することをお勧めします。以下のセクションでは、よく利用される attributes の一部を見ていきます。

### Service Attributes

サービスを記述するための attributes がいくつかあります。

`service.name` はサービスの論理名を定義する必須の attribute です。OpenTelemetry SDK によって自動的に追加されますが、カスタマイズも可能です。これはシンプルに保つのが望ましく（たとえば `inventoryservice-prod-hostxyz` よりも `inventoryservice` の方が望ましい）、サービスの他の側面を表現するためには別の attributes を活用できます。

以下のサービス attributes の利用が推奨されます。

- `service.namespace` この attribute は、サービスを所有するチームを識別するために利用できます
- `service.instance.id` はサービスの一意なインスタンスを識別するために使用されます
- `service.version` はサービスのバージョンを識別するために使用されます

### Telemetry SDK

これらの attributes は、利用されている計装ライブラリに関する情報を記録するため、SDK によって自動的に設定されます。

- `telemetry.sdk.name` は通常 `opentelemetry` に設定されます
- `telemetry.sdk.language` は SDK の言語を表します（例：`java`）
- `telemetry.sdk.version` は利用されている SDK のバージョンを識別します

### Containers

コンテナ上で実行されるサービスについては、コンテナランタイムを記述する `container.id`、`container.name`、`container.image.name` といった多くの attributes があります。完全な一覧は[こちら](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/resource/container.md)で確認できます。

### Hosts

これらの attributes は、サービスが実行されているホストを記述するもので、`host.id`、`host.name`、`host.arch` といった attributes が含まれます。完全な一覧は[こちら](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/resource/host.md)で確認できます。

### Deployment Environment

`deployment.environment` attribute は、サービスがデプロイされている環境（**staging** や **production** など）を識別するために使用されます。

Splunk Observability Cloud は、関連コンテンツ機能（[こちら](https://docs.splunk.com/observability/metrics-and-metadata/enablerelatedcontent.html)を参照）を有効化するためにこの attribute を使用するため、必ず含めることが重要です。

### Cloud

AWS などのパブリッククラウド環境で実行されるサービスの情報を取得するための attributes もあります。`cloud.provider`、`cloud.account.id`、`cloud.region` といった attributes が含まれます。

attributes の完全な一覧は[こちら](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/resource/cloud.md)で確認できます。

[GCP](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/resource/cloud-provider/gcp) のように、独自のサービス向けに固有の semantic conventions を定義しているクラウドプロバイダーもあります。

### Kubernetes

Kubernetes 上で実行されるアプリケーション向けにも、標準化された attributes が多数存在します。これらの多くは、Splunk が提供する OpenTelemetry collector ディストリビューションによって自動的に追加されます。詳細は[こちら](https://docs.splunk.com/observability/metrics-and-metadata/enablerelatedcontent.html#splunk-infrastructure-monitoring)を参照してください。

これらの attributes には、`k8s.cluster.name`、`k8s.node.name`、`k8s.pod.name`、`k8s.namespace.name`、`kubernetes.workload.name` などがあります。

## カスタム Attributes 作成のベストプラクティス

多くの組織では、OpenTelemetry の resource semantic conventions で定義されているもの以外の attributes が必要になります。

このような場合、semantic conventions にすでに含まれている attribute 名との競合を避けることが重要です。そのため、命名規則の attribute 名を決定する前に semantic conventions を確認しておくことをお勧めします。

attribute 名の命名規則に加えて、attribute の値についても考慮する必要があります。たとえば、アプリケーションが属する特定のビジネスユニットを取得したい場合、効果的なフィルタリングを実現するために、選択可能なビジネスユニット値の標準化されたリストも用意する必要があります。

OpenTelemetry コミュニティは、attributes の命名時に従うべきガイドラインも提供しています。詳細は[こちら](https://opentelemetry.io/docs/specs/otel/common/attribute-naming/)で確認できます。

[Recommendations for Application Developers](https://opentelemetry.io/docs/specs/otel/common/attribute-naming/#recommendations-for-application-developers) のセクションが本議論に最も関連します。

そこでは以下が推奨されています。

- attribute 名に自社のドメイン名をプレフィックスとして付与する（例：`com.acme.shopname`）。これは、attribute が社内だけでなく社外でも使用される可能性がある場合に当てはまります。
- attribute が特定のアプリケーション固有で、組織内でのみ使用される場合は、attribute 名にアプリケーション名をプレフィックスとして付与する。
- 既存の OpenTelemetry semantic convention 名を attribute 名のプレフィックスとして使用しない。
- 異なる組織や業界で広く必要とされる attribute であれば、その attribute 名を OpenTelemetry 仕様に追加する提案を行うことを検討する。
- attribute 名が `otel.*` で始まらないようにする。これは OpenTelemetry 仕様での使用のために予約されているためです。

## メトリクスカーディナリティに関する考慮事項

attribute 名と値の命名標準を決定する際に最後に留意すべき点は、メトリクスのカーディナリティに関するものです。

メトリクスカーディナリティは、**メトリクス名と関連するディメンションの組み合わせによって生成される一意なメトリクス時系列（MTS）の数**として定義されます。

ディメンションキーの数が多く、それらのディメンションキーが取り得る一意な値の数も多い場合、メトリクスは高カーディナリティとなります。

たとえば、アプリケーションが `custom.metric` という名前のメトリクスのデータを送信するとします。attributes が一切ない場合、`custom.metric` は単一のメトリクス時系列（MTS）を生成します。

一方、`custom.metric` に `customer.id` という attribute が含まれており、数千の顧客 ID 値が存在する場合、これは数千のメトリクス時系列を生成することになり、コストやクエリパフォーマンスに影響を与える可能性があります。

Splunk Observability Cloud は、メトリクス使用量を管理するための[レポート](https://docs.splunk.com/Observability/infrastructure/metrics-pipeline/metrics-usage-report.html)を提供しています。また、不要なディメンションを削除するための[ルール](https://docs.splunk.com/Observability/infrastructure/metrics-pipeline/use-metrics-pipeline.html)も作成できます。とはいえ、第一の防衛線は、attribute 名と値の組み合わせがどのようにメトリクスカーディナリティの増加を引き起こすかを理解することです。

## まとめ

このドキュメントでは、OpenTelemetry の大規模な計装展開を始める前に、OpenTelemetry タグの命名規則を定義することの重要性について取り上げました。

OpenTelemetry の resource semantic conventions が複数の attributes に対する命名規則を定義していること、そしてその多くが OpenTelemetry SDK や OpenTelemetry collector 内で動作するプロセッサによって自動的に収集されることについて説明しました。

最後に、resource semantic conventions だけでは組織のニーズを満たせない場合に備えて、attribute 名を作成する際のベストプラクティスをいくつか共有しました。
