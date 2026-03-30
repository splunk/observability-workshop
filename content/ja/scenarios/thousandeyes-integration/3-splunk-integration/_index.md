---
title: Splunk 連携
linkTitle: 3. Splunk 連携
weight: 3
time: 15 minutes
description: ThousandEyes から Splunk Observability Cloud への OpenTelemetry ベースのメトリクスストリームを設定します。
---

## Splunk Observability Cloud について

Splunk Observability Cloudは、メトリクス、トレース、ログを大規模に監視するために構築されたリアルタイムのオブザーバビリティプラットフォームです。OpenTelemetryデータを取り込み、高度なダッシュボードと分析機能を提供して、チームがパフォーマンスの問題を迅速に検出し解決できるよう支援します。このセクションでは、OpenTelemetryを使用してThousandEyesデータをSplunk Observability Cloudと統合する方法を説明します。

{{% notice title="このセクションの範囲" style="info" %}}
このセクションでは、ThousandEyesからSplunk Observability Cloudへの**メトリクスストリーミング**パスについて説明します。次のセクションでは、ThousandEyesとSplunk APM間の双方向リンクを作成する別の**分散トレーシング**ワークフローを追加します。
{{% /notice %}}

## ステップ 1: Splunk Observability Cloud アクセストークンを作成する

ThousandEyesメトリクスをSplunk Observability Cloudに送信するには、**Ingest** スコープを持つアクセストークンが必要です。以下の手順に従ってください：

1. Splunk Observability Cloudプラットフォームで、**Settings > Access Token** に移動します
2. **Create Token** をクリックします
3. **Name** を入力します
4. **Ingest** スコープを選択します
5. **Create** を選択してアクセストークンを生成します
6. アクセストークンをコピーし、安全に保管します

テレメトリデータをSplunk Observability Cloudに送信するには、アクセストークンが必要です。

## ステップ 2: 連携を作成する

この連携は、ThousandEyesメトリクスをSplunk Observability Cloudのダッシュボードとディテクターに送信する一方向のテレメトリストリームです。

### ThousandEyes UI を使用する

Splunk Observability CloudとThousandEyesを連携するには：

1. ThousandEyesプラットフォームでアカウントにログインし、**Manage > Integration > Integration 1.0** に移動します
2. **New Integration** をクリックし、**OpenTelemetry Integration** を選択します

   ![ThousandEyes Integration Setup](../images/te1.gif)

3. 連携の **Name** を入力します
4. **Target** を **HTTP** に設定します
5. **Endpoint URL** を入力します：`https://ingest.{REALM}.signalfx.com/v2/datapoint/otlp`
   - `{REALM}` をSplunk環境に置き換えます（例：`us1`、`eu0`）
6. **Preset Configuration** で **Splunk Observability Cloud** を選択します
7. **Auth Type** で **Custom** を選択します
8. 以下の **Custom Headers** を追加します：
   - `X-SF-Token: {TOKEN}`（ステップ1で作成したSplunk Observability Cloudアクセストークンを入力）
   - `Content-Type: application/x-protobuf`
9. **OpenTelemetry Signal** で **Metric** を選択します
10. **Data Model Version** で **v2** を選択します
11. テストを選択します
12. **Save** をクリックして連携の設定を完了します

   ![Integration Complete](../images/te2.gif)

これでThousandEyesデータとSplunk Observability Cloudの連携が正常に完了しました。

### ThousandEyes API を使用する

プログラムによる連携には、以下のAPIコマンドを使用します：

#### HTTP Protocol

```bash
curl -v -XPOST https://api.thousandeyes.com/v7/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "type": "opentelemetry",
    "testMatch": [{
      "id": "281474976717575",
      "domain": "cea"
    }],
    "endpointType": "http",
    "streamEndpointUrl": "https://ingest.{REALM}.signalfx.com:443/v2/datapoint/otlp",
    "customHeaders": {
      "X-SF-Token": "{TOKEN}",
      "Content-Type": "application/x-protobuf"
    }
  }'
```

#### gRPC Protocol

```bash
curl -v -XPOST https://api.thousandeyes.com/v7/stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "type": "opentelemetry",
    "testMatch": [{
      "id": "281474976717575",
      "domain": "cea"
    }],
    "endpointType": "grpc",
    "streamEndpointUrl": "https://ingest.{REALM}.signalfx.com:443",
    "customHeaders": {
      "X-SF-Token": "{TOKEN}",
      "Content-Type": "application/x-protobuf"
    }
  }'
```

`streamEndpointUrl` と `X-SF-Token` の値を、お使いのSplunk Observability Cloudインスタンスの正しい値に置き換えてください。

{{% notice title="注意" style="info" %}}
`{REALM}` をSplunk環境のRealm（例：`us1`、`us2`、`eu0`）に、`{TOKEN}` を実際のSplunkアクセストークンに置き換えてください。
{{% /notice %}}

{{% notice title="次のステップ" style="primary" icon="lightbulb" %}}
メトリクス連携が完了したら、**分散トレーシング**に進み、ThousandEyesからSplunk APMへの、そしてその逆の調査パスを追加します。
{{% /notice %}}

## ステップ 3: Splunk Observability Cloud の ThousandEyes ダッシュボード

連携が設定されると、Splunk Observability Cloud内のThousandEyes Network Monitoring Dashboardでリアルタイムの監視データを表示できます。ダッシュボードには以下が含まれます：

- **HTTP Server Availability (%)**：監視対象のHTTPサーバーの可用性を表示します
- **HTTP Throughput (bytes/s)**：時間の経過に伴うデータ転送速度を表示します
- **Client Request Duration (seconds)**：クライアントリクエストのレイテンシを測定します
- **Web Page Load Completion (%)**：ページ読み込み成功の割合を表示します
- **Page Load Duration (seconds)**：ページの読み込み時間を表示します

### ダッシュボードテンプレート

ダッシュボードテンプレートは以下のリンクからダウンロードできます：[ThousandEyes Splunk Observability Cloud ダッシュボードテンプレートをダウンロード (Google Drive)](https://drive.google.com/file/d/1xpdjr5CRBC-JBM9tGsNFcVYp3C-tJC8s/view?usp=sharing)。

{{% notice title="完了" style="success" icon="check" %}}
ThousandEyesデータがSplunk Observability Cloudにストリーミングされるようになりました。次に、分散トレーシングコネクタを追加して、トラブルシューティング中にThousandEyesとSplunk APMの間を移動できるようにします。
{{% /notice %}}
