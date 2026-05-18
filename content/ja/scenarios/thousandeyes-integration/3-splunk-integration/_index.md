---
title: Splunk Integration
linkTitle: 3. Splunk Integration
weight: 3
time: 10 minutes
description: ThousandEyes から Splunk Observability Cloud への OpenTelemetry ベースのメトリクスストリーミングを設定します。
---

## Splunk Observability Cloud について

Splunk Observability Cloud は、メトリクス、トレース、ログを大規模にモニタリングするために構築されたリアルタイムオブザーバビリティプラットフォームです。OpenTelemetry データを取り込み、高度なダッシュボードと分析機能を提供することで、チームがパフォーマンスの問題を迅速に検出し解決できるようにします。このセクションでは、OpenTelemetry を使用して ThousandEyes データを Splunk Observability Cloud と統合する方法を説明します。

{{% notice title="このセクションの範囲" style="info" %}}
このセクションでは、ThousandEyes から Splunk Observability Cloud への**メトリクスストリーミング**パスについて説明します。次のセクションでは、ThousandEyes と Splunk APM の間に双方向リンクを作成する別の**分散トレーシング**ワークフローを追加します。
{{% /notice %}}

{{% notice title="統合は1つだけ必要" style="warning" %}}
各ワークショップ参加者がこの設定を行うのではなく、インストラクターが以下の手順を実行するのを確認してください。

次のページから引き続き手順を実行します。
{{% /notice %}}

### ステップ 1: Splunk Observability Cloud アクセストークンの取得または作成

ThousandEyes メトリクスを Splunk Observability Cloud に送信するには、**Ingest** スコープを持つアクセストークンが必要です。

このワークショップでは、提供されたトークンを使用します。インスタンスから取得できます:

```bash
. ~/workshop/petclinic/scripts/check_env.sh | grep ACCESS_TOKEN
```

または、以下のクリップに示すように Splunk Observability Cloud UI から取得できます。

### ステップ 2: 統合の作成

この統合は、ThousandEyes メトリクスを Splunk Observability Cloud のダッシュボードとディテクターに送信する一方向のテレメトリストリームです。

#### ThousandEyes UI の使用

Splunk Observability Cloud と ThousandEyes を統合するには:

1. ThousandEyes プラットフォームのアカウントにログインし、**Manage > Integration > Integration 1.0** に移動します
2. **New Integration** をクリックし、**ThousandEyes for OpenTelemetry** を選択します
3. 統合の **Name** を入力します
4. **Target** を **HTTP** に設定します
5. **Endpoint URL** を入力します: `https://ingest.{REALM}.signalfx.com/v2/datapoint/otlp`
   - `{REALM}` を Splunk 環境に置き換えます（例: `us1`、`eu0`）
6. **Preset Configuration** で **Splunk Observability Cloud** を選択します
7. **Auth Type** で **Custom** を選択します
8. 以下の **Custom Headers** を追加します:
   - `X-SF-Token: {TOKEN}`（ステップ 1 で作成した Splunk Observability Cloud アクセストークンを入力します）
   - `Content-Type: application/x-protobuf`
9. **OpenTelemetry Signal** で **Metric** を選択します
10. **Data Model Version** で **v2** を選択します
11. 送信するテストを選択します。
{{% notice title="テストは後から追加可能" style="primary" icon="lightbulb" %}}
新しいテストを追加した場合、後でこの統合にテストを追加し直す必要があります
{{% /notice %}}
12. **Save** をクリックして統合のセットアップを完了します

![Integration Complete](../images/te2.gif?width=45vw)

これで ThousandEyes データと Splunk Observability Cloud の統合が正常に完了しました。

{{% notice title="Pending 状態" style="note" %}}
統合がしばらく **Pending** 状態のままになる場合があります。**Connected** に変わる前にリフレッシュが必要な場合があります。
{{% /notice %}}

{{% notice title="次のステップ" style="primary" icon="lightbulb" %}}
メトリクスの統合が完了したら、**Distributed Tracing** に進み、ThousandEyes から Splunk APM への逆方向の調査パスを追加します。
{{% /notice %}}

### ステップ 3: Splunk Observability Cloud の ThousandEyes ダッシュボード

統合のセットアップが完了すると、Splunk Observability Cloud 内の ThousandEyes Network Monitoring Dashboard でリアルタイムのモニタリングデータを確認できます。ダッシュボードには以下が含まれます:

- **HTTP Server Availability (%)**: 監視対象の HTTP サーバーの可用性を表示します
- **HTTP Throughput (bytes/s)**: 時間経過に伴うデータ転送速度を表示します
- **Client Request Duration (seconds)**: クライアントリクエストのレイテンシを測定します
- **Web Page Load Completion (%)**: ページロードの成功率を表示します
- **Page Load Duration (seconds)**: ページのロード時間を表示します

#### ダッシュボードテンプレートのデプロイ

以下のリンクからダッシュボードテンプレートをダウンロードできます: [Download ThousandEyes Splunk Observability Cloud dashboard template (Google Drive)](https://github.com/thousandeyes/thousandeyes-observability-dashboards/blob/main/splunk/ThousandEyesDashboard.json)。その後、Splunk Observability Cloud にインポートできます。（これはすでに完了しています。）

テストが実行されている場合は、すでにデータが表示されます。

![Splunk Observability Cloud Dashboard for ThousandEyes](../images/splunk-o11y-dashboard-te.png?width=45vw)

{{% notice title="成功" style="success" icon="check" %}}
ThousandEyes データが Splunk Observability Cloud にストリーミングされるようになりました。次に、分散トレーシングコネクターを追加して、トラブルシューティング中に ThousandEyes と Splunk APM の間をシームレスに移動できるようにします。
{{% /notice %}}
