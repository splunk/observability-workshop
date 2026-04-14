---
title: "フェーズ 3: Global Data Links"
linkTitle: 4. Global Data Links
weight: 4
archetype: chapter
time: 10 minutes
description: appd.* スパン属性を使用して、対応する AppDynamics ティアビューに直接移動する Global Data Link を Splunk Observability Cloud で作成します。
---

トレースの `appd.*` 属性は単なるメタデータではありません。**Global Data Links** を活用することで、Splunk Observability Cloud でトレースを閲覧している誰もが、ワンクリックで対応する AppDynamics ビューに直接ジャンプできるようになります。

## Global Data Links とは

Global Data Links は、スパン属性、タグ値、またはメトリクスディメンションにクリック可能なリンクを作成する Splunk Observability Cloud の機能です。ユーザーがリンクされた値をクリックすると、実際の属性値が URL テンプレートに代入された、定義済みの外部 URL に移動します。

### Data Link の前提条件

AppDynamics のアプリケーションへの URL をコピーします。アプリケーションを識別する URL の重要な部分は、URL 上のクエリパラメータです（例`&application=99999`）。
アプリケーションのクエリパラメータを含む完全な URL を使用して、Global Data Link を構築します。
![AppD Application ID](../_images/app-url.png)

## Global Data Link の作成

1. Splunk Observability Cloud で、左側のナビゲーションパネルの **Settings**（歯車アイコン）をクリックします。
2. **Global Data Links** をクリックします。
3. **New Link** をクリックします。
4. リンクを設定します

| フィールド               | 値                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Link Label**      | `Open in AppDynamics`                                                                                                                        |
| **Link to**         | `Custom URL`                                                                                                                                 |
| **Show on**         | `Property:Value pair` - `appd.app.name:<YOUR APPLICATION NAME>` を選択（例`appd.app.name:Dual-Ingest-JRH`）                                                                                                                                 |
| **URL**             | `https://se-lab.saas.appdynamics.com/controller/#/location=APP_DASHBOARD&timeRange=Custom_Time_Range.BETWEEN_TIMES.{{ end_time }}.{{ start_time }}.6&application=<YOUR_APPLICATION_ID_NUMBER>&dashboardMode=force` |
| **Time format**         | `Unix time: epoch milliseconds`                                                                                                                                 |
| **Minimum trigger** | `appd.tier.name`                                                                                                                             |

{{% notice title="URL テンプレート構文" style="primary" icon="lightbulb" %}}
二重中括弧 `{{ end_time }}` と `{{ start_time }}` はテンプレート変数です。Splunk Observability Cloud はクリック時に実際の値に置換します。

`<YOUR_APPLICATION_ID_NUMBER>` は、特定のアプリケーションのクエリパラメータからの番号です。
{{% /notice %}}
![Global Datalink Config](../_images/global-datalink-config.png?width=50vw)

5. **Save** をクリックします。

## Global Data Link のテスト

1. **APM** に戻り、**OrderService** サービスのトレースを開きます。
2. ルートスパンをクリックして属性を表示します。
3. 属性リストで `appd.app.name` を見つけます。**Open in AppDynamics** というラベルのクリック可能なリンクになっているはずです。
4. リンクをクリックします。新しいブラウザタブが開き、AppDynamics Controller の **OrderService** アプリケーションビューに直接移動します。
![Global Datalink Config](../_images/datalink.png?width=20vw)

{{% notice title="注意" style="info" icon="info-circle" %}}
リンクが機能するには、同じブラウザで AppDynamics Controller にログインしている必要があります。ログインを求められた場合は、Cisco の認証情報を使用してください。
{{% /notice %}}

## 逆方向へのナビゲーション（AppD から Splunk へ）

逆方向へのナビゲーションも可能です。デュアルモードでキャプチャされた AppDynamics スナップショットには、**Data Collectors** タブの下に OTel `TraceId` が含まれています。

Splunk Observability Cloud で対応するトレースを見つけるには

1. AppDynamics Controller で、ビジネストランザクションの **Transaction Snapshot** を開きます。
2. **Data Collectors** タブに移動します。
3. `TraceId` の値を見つけます。
4. Splunk Observability Cloud で、**APM → Traces** に移動し、そのトレース ID を検索します。

これにより、2 つのプラットフォーム間の**双方向の関連付け**が可能になります。
![AppDynamics Trace ID](../_images/appd-traceid.png?width=30vw)
