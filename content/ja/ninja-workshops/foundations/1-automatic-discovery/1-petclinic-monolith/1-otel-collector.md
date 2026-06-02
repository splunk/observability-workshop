---
title: OpenTelemetry Collector のインストール
linkTitle: 1. OpenTelemetry Collector
weight: 1
---

Splunk OpenTelemetry Collector は、インフラストラクチャとアプリケーションを計装するためのコアコンポーネントです。その役割は、以下のデータを収集して送信することです。

* インフラストラクチャメトリクス（disk、CPU、memory など）
* Application Performance Monitoring（APM）トレース
* プロファイリングデータ
* ホストおよびアプリケーションログ

{{% notice title="既存の OpenTelemetry Collector を削除する" style="warning" %}}
Splunk IM ワークショップを完了している場合は、続行する前に Kubernetes 上で動作している collector を削除しておいてください。以下のコマンドを実行することで削除できます。

``` bash
helm delete splunk-otel-collector
```

EC2 インスタンスには、すでに古いバージョンの collector がインストールされている可能性があります。collector をアンインストールするには、以下のコマンドを実行してください。

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

{{% /notice %}}

インスタンスが正しく構成されていることを確認するため、このワークショップで必要となる環境変数が正しく設定されているかを確認する必要があります。ターミナルで以下のコマンドを実行してください。

``` bash
. ~/workshop/petclinic/scripts/check_env.sh
```

出力結果で、以下のすべての環境変数が存在し、値が設定されていることを確認してください。不足しているものがある場合は、講師にお問い合わせください。

```text
ACCESS_TOKEN
REALM
RUM_TOKEN
HEC_TOKEN
HEC_URL
INSTANCE
```

確認できたら、Collector をインストールできます。インストールスクリプトには、いくつかの追加パラメーターが渡されます。

* `--with-instrumentation` - Splunk distribution of OpenTelemetry Java からエージェントをインストールします。これは PetClinic の Java アプリケーション起動時に自動的に読み込まれます。設定は不要です！
* `--deployment-environment` - リソース属性 `deployment.environment` に渡された値を設定します。これは UI でビューをフィルタリングするために使用されます。
* `--enable-profiler` - Java アプリケーション用のプロファイラーを有効化します。これにより、アプリケーションの CPU プロファイルが生成されます。
* `--enable-profiler-memory` - Java アプリケーション用のプロファイラーを有効化します。これにより、アプリケーションのメモリプロファイルが生成されます。
* `--enable-metrics` - Micrometer メトリクスのエクスポートを有効化します。
* `--hec-token` - collector が使用する HEC トークンを設定します。
* `--hec-url` - collector が使用する HEC URL を設定します。

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --realm $REALM -- $ACCESS_TOKEN --mode agent --with-instrumentation --deployment-environment $INSTANCE-petclinic --enable-profiler --enable-profiler-memory --enable-metrics --hec-token $HEC_TOKEN --hec-url $HEC_URL
```

次に、AWS インスタンス ID ではなくインスタンスのホスト名を公開するように、collector にパッチを当てます。これにより、UI でデータをフィルタリングしやすくなります。

``` bash
sudo sed -i 's/gcp, ecs, ec2, azure, system/system, gcp, ecs, ec2, azure/g' /etc/otel/collector/agent_config.yaml
```

`agent_config.yaml` にパッチを当てたら、collector を再起動する必要があります。

``` bash
sudo systemctl restart splunk-otel-collector
```

インストールが完了すると、**Hosts with agent installed** ダッシュボードに移動して、ホストからのデータを確認できます。**Dashboards → Hosts with agent installed** の順に進んでください。

フィルターパネルの「Host」フィールド内をクリックし、ワークショップインスタンスのホスト名を入力または選択します（ホスト名はターミナルセッションのコマンドプロンプトから取得できます）。ホストのデータが流れていることを確認できたら、APM コンポーネントを開始する準備が整いました。
