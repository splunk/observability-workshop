---
title: OpenTelemetry Collectorをインストールする
linkTitle: 1. OpenTelemetry Collector
weight: 1
---

## 1. はじめに

OpenTelemetry Collectorは、インフラストラクチャーとアプリケーションを計装するためのコアコンポーネントです。 その役割は収集と送信です

- インフラストラクチャーのメトリクス（ディスク、CPU、メモリなど）
- Application Performance Monitoring（APM）のトレース情報
- プロファイリングに関するデータ
- ホストおよびアプリケーションのログ

Splunk Observability Cloudでは、インフラストラクチャーとアプリケーションの両方でCollectorのセットアップを案内するウィザードを提供しています。デフォルトでは、ウィザードはコレクターのインストールのみを行うコマンドのみを提供します。

## 2. 環境変数を設定する

すでに **Splunk IM** ワークショップを終了している場合は、既存の環境変数を利用することができます。そうでない場合は、`ACCESS_TOKEN` と `REALM` の環境変数を設定して、OpenTelemetry Collectorのインストールコマンドを実行していきます。

例えば、Realmが `us1` の場合、`export REALM=us1` と入力し、`eu0` の場合は `export REALM=eu0` と入力します。

{{< tabs >}}
{{% tab title="ACCESS TOKENを環境変数に設定する" %}}

```bash
export ACCESS_TOKEN="<replace_with_O11y-Workshop-ACCESS_TOKEN>"
```

{{% /tab %}}
{{< /tabs >}}

{{< tabs >}}
{{% tab title="REALMを環境変数に設定する" %}}

```bash
export REALM="<replace_with_REALM>"
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="既存のOpenTelemetryコレクターをすべて削除する" style="warning" %}}
同じVMインスタンスにSplunk IMワークショップのセットアップをしている場合、Otel Collectorをインストールする前にKubernetesで実行中のCollectorを削除していることを確認してください。これは、以下のコマンドを実行することで行うことができます

```bash
helm delete splunk-otel-collector
```

{{% /notice %}}

## 3. OpenTelemetry Collector をインストールする

次に、Collectorをインストールします。インストールスクリプトに渡される追加のパラメータは `--deployment-environment` です。

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
sudo sh /tmp/splunk-otel-collector.sh --deployment-environment $(hostname)-petclinic --realm $REALM -- $ACCESS_TOKEN
```

{{% notice style="info" title="AWS/EC2インスタンスの場合" %}}。
AWS/EC2インスタンス上でこのワークショップを行う場合、インスタンスのホスト名を公開するためにコレクターにパッチを適用する必要があります

```bash
sudo sed -i 's/gcp, ecs, ec2, azure, system/system, gcp, ecs, ec2, azure/g' /etc/otel/collector/agent_config.yaml
```

`agent_config.yaml` にパッチを適用したあと、Collectorを再起動してください

```bash
sudo systemctl restart splunk-otel-collector
```

{{% /notice %}}

インストールが完了したら、Splunk Observabilityの **Hosts with agent installed** ダッシュボードに移動して、**Dashboards → Hosts with agent installed** からホストのデータを確認してみましょう。

ダッシュボードのフィルタを使用して `host.name` を選択し、仮想マシンのホスト名を入力または選択します。ホストのデータが表示されたら、APMコンポーネントを使用する準備が整いました。
