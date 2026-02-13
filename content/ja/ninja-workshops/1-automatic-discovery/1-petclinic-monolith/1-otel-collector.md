---
title: OpenTelemetry Collector のインストール
linkTitle: 1. OpenTelemetry Collector
weight: 1
---

Splunk OpenTelemetry Collectorは、インフラストラクチャとアプリケーションの計装における中核コンポーネントです。その役割は以下のデータを収集して送信することです

* インフラストラクチャメトリクス（ディスク、CPU、メモリなど）
* Application Performance Monitoring (APM) トレース
* プロファイリングデータ
* ホストおよびアプリケーションのログ

{{% notice title="既存のOpenTelemetry Collectorの削除" style="warning" %}}
Splunk IMワークショップを完了している場合は、続行する前にKubernetesで実行中のCollectorを削除してください。以下のコマンドを実行して削除できます

``` bash
helm delete splunk-otel-collector
```

EC2インスタンスには、古いバージョンのCollectorがすでにインストールされている場合があります。Collectorをアンインストールするには、以下のコマンドを実行してください

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

{{% /notice %}}

インスタンスが正しく設定されていることを確認するために、このワークショップに必要な環境変数が正しく設定されているか確認する必要があります。ターミナルで以下のコマンドを実行してください

``` bash
. ~/workshop/petclinic/scripts/check_env.sh
```

出力で、以下のすべての環境変数が存在し、値が設定されていることを確認してください。不足している場合は、インストラクターに連絡してください

```text
ACCESS_TOKEN
REALM
RUM_TOKEN
HEC_TOKEN
HEC_URL
INSTANCE
```

これでCollectorのインストールに進むことができます。インストールスクリプトには、いくつかの追加パラメータが渡されます

* `--with-instrumentation` - SplunkディストリビューションのOpenTelemetry Javaからエージェントをインストールします。これにより、PetClinic Javaアプリケーションの起動時に自動的にロードされます。設定は不要です！
* `--deployment-environment` - リソース属性 `deployment.environment` を指定された値に設定します。これはUIでビューをフィルタリングするために使用されます。
* `--enable-profiler` - Javaアプリケーションのプロファイラを有効にします。これによりアプリケーションのCPUプロファイルが生成されます。
* `--enable-profiler-memory` - Javaアプリケーションのプロファイラを有効にします。これによりアプリケーションのメモリプロファイルが生成されます。
* `--enable-metrics` - Micrometerメトリクスのエクスポートを有効にします
* `--hec-token` - Collectorが使用するHECトークンを設定します
* `--hec-url` - Collectorが使用するHEC URLを設定します

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --realm $REALM -- $ACCESS_TOKEN --mode agent --without-fluentd --with-instrumentation --deployment-environment $INSTANCE-petclinic --enable-profiler --enable-profiler-memory --enable-metrics --hec-token $HEC_TOKEN --hec-url $HEC_URL
```

次に、Collectorにパッチを適用して、AWSインスタンスIDではなくインスタンスのホスト名を公開するようにします。これにより、UIでのデータのフィルタリングが容易になります

``` bash
sudo sed -i 's/gcp, ecs, ec2, azure, system/system, gcp, ecs, ec2, azure/g' /etc/otel/collector/agent_config.yaml
```

`agent_config.yaml` にパッチを適用したら、Collectorを再起動する必要があります

``` bash
sudo systemctl restart splunk-otel-collector
```

インストールが完了したら、**Hosts with agent installed** ダッシュボードに移動して、ホストからのデータを確認できます。**Dashboards → Hosts with agent installed** の順に移動してください。

ダッシュボードフィルタを使用して `host.name` を選択し、ワークショップインスタンスのホスト名を入力または選択してください（これはターミナルセッションのコマンドプロンプトから取得できます）。ホストのデータが流れていることを確認したら、APMコンポーネントの作業を開始する準備が整いました。
