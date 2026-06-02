---
title: Splunk Integration
linkTitle: 3. Splunk Integration
weight: 3
time: 10 minutes
description: ThousandEyes から Splunk Observability Cloud への OpenTelemetry ベースのメトリクスストリームを構成します。
---

## Splunk Observability Cloud について

Splunk Observability Cloud は、メトリクス、トレース、ログを大規模に監視するために専用設計されたリアルタイムオブザーバビリティプラットフォームです。OpenTelemetry データを取り込み、高度なダッシュボードと分析機能を提供することで、チームがパフォーマンス問題を迅速に検出して解決できるよう支援します。本セクションでは、OpenTelemetry を使用して ThousandEyes データを Splunk Observability Cloud と統合する方法について説明します。

{{% notice title="本セクションのスコープ" style="info" %}}
本セクションでは、ThousandEyes から Splunk Observability Cloud への**メトリクスストリーミング**経路について説明します。次のセクションでは、ThousandEyes と Splunk APM の間で双方向のリンクを作成する別の**分散トレーシング**ワークフローを追加します。
{{% /notice %}}

{{< acknowledge "必要な統合は1つのみ" >}}
各受講者がこの設定を行うのではなく、講師が以下の手順を実演するのを見てください。

次のページから、皆さんは引き続き手順を実施します。
{{< /acknowledge >}}

{{< step "Splunk Observability Cloud アクセストークンの取得または作成" "1" >}}

ThousandEyes のメトリクスを Splunk Observability Cloud に送信するには、**Ingest** スコープを持つアクセストークンが必要です。

本ワークショップでは、用意されたトークンを使用します。インスタンスから以下のように取得できます:

```bash
. ~/workshop/petclinic/scripts/check_env.sh | grep ACCESS_TOKEN
```

または、以下のクリップで示すように、Splunk Observability Cloud の UI から取得することもできます。

{{< /step >}}

{{< step "統合の作成" "2" >}}

この統合は、ThousandEyes のメトリクスを Splunk Observability Cloud のダッシュボードや Detector に送り込む一方向のテレメトリーストリームです。

### ThousandEyes UI を使用する

Splunk Observability Cloud と ThousandEyes を統合するには:

1. ThousandEyes プラットフォームのアカウントにログインし、**Manage > Integration > Integration 1.0** に移動します
2. **New Integration** をクリックし、**ThousandEyes for OpenTelemetry** を選択します
3. 統合の **Name** を入力します
4. **Target** を **HTTP** に設定します
5. **Endpoint URL** に `https://ingest.{REALM}.signalfx.com/v2/datapoint/otlp` を入力します
   - `{REALM}` を Splunk 環境（例: `us1`、`eu0`）に置き換えてください
6. **Preset Configuration** で **Splunk Observability Cloud** を選択します
7. **Auth Type** で **Custom** を選択します
8. 以下の **Custom Headers** を追加します:
   - `X-SF-Token: {TOKEN}` (ステップ1で作成した Splunk Observability Cloud のアクセストークンを入力します)
   - `Content-Type: application/x-protobuf`
9. **OpenTelemetry Signal** で **Metric** を選択します
10. **Data Model Version** で **v2** を選択します
11. 送信したいテストを選択します。
      >[!IMPORTANT] テストの後からの追加について
      >新しいテストを追加した場合、後でこの統合に再度追加する必要があります
12. **Save** をクリックして統合の設定を完了します

![Integration Complete](../images/te2.gif?width=45vw)

これで ThousandEyes のデータを Splunk Observability Cloud に正常に統合できました。

{{% notice title="Pending 状態" style="note" %}}
統合はしばらくの間 **Pending** 状態のままになる場合があります。**Connected** に変わるまでに更新が必要な場合があります。
{{% /notice %}}

{{% notice title="次にやること" style="primary" icon="lightbulb" %}}
メトリクス統合が完了したら、**Distributed Tracing** に進み、ThousandEyes から Splunk APM へ、そして再び戻る逆方向の調査経路を追加してください。
{{% /notice %}}

{{< /step >}}

{{< step "Splunk Observability Cloud の ThousandEyes ダッシュボード" "3">}}

統合の設定が完了すると、Splunk Observability Cloud 内の ThousandEyes Network Monitoring Dashboard でリアルタイムの監視データを閲覧できるようになります。このダッシュボードには以下が含まれます:

- **HTTP Server Availability (%)**: 監視対象の HTTP サーバーの可用性を表示します
- **HTTP Throughput (bytes/s)**: 経時的なデータ転送レートを表示します
- **Client Request Duration (seconds)**: クライアントリクエストのレイテンシーを測定します
- **Web Page Load Completion (%)**: ページ読み込みの成功率をパーセンテージで示します
- **Page Load Duration (seconds)**: ページの読み込みにかかった時間を表示します

#### ダッシュボードテンプレートのデプロイ

ダッシュボードテンプレートは以下のリンクからダウンロードできます: [**ThousandEyes Splunk Observability Cloud ダッシュボードテンプレートをダウンロード**](https://github.com/thousandeyes/thousandeyes-observability-dashboards/blob/main/splunk/ThousandEyesDashboard.json)。その後、Splunk Observability Cloud にインポートできます（本ワークショップでは設定済みです）。

実行中のテストがある場合は、すでにデータが表示されているはずです。

![Splunk Observability Cloud Dashboard for ThousandEyes](../images/splunk-o11y-dashboard-te.png?width=45vw)

{{< /step >}}

{{< checkpoint "ThousandEyes のデータが Splunk Observability Cloud にストリーミングされるようになりました。次は、トラブルシューティング中に ThousandEyes と Splunk APM の間を行き来できるよう、分散トレーシングコネクターを追加します。" >}}
