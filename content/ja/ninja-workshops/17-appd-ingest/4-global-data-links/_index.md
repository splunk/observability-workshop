---
title: "フェーズ 3: Global Data Links"
linkTitle: 4. Global Data Links
weight: 4
archetype: chapter
time: 10 minutes
description: appd.* スパン属性を使用して、対応する AppDynamics ティアビューに直接ナビゲートするグローバルデータリンクを Splunk Observability Cloud で作成します。
---

{{% notice title="注意" style="primary" icon="lightbulb" %}}
グループワークショップに参加している場合は、インストラクターの指示に従い、追加のグローバルデータリンクを作成しないでください。
このセクションを自分で完了する必要はありません。これらの手順は、学習および文書化の目的で含まれています。
ご協力ありがとうございます！
{{% /notice %}}

トレースに付与された `appd.*` 属性は単なるメタデータではありません。**グローバルデータリンク**を活用することで、Splunk Observability Cloud でトレースを表示しているユーザーがワンクリックで対応する AppDynamics ビューに直接ジャンプできるようになります。

## グローバルデータリンクとは？

グローバルデータリンクは、スパン属性、タグ値、またはメトリクスディメンションにクリック可能なリンクを作成する Splunk Observability Cloud の機能です。ユーザーがリンクされた値をクリックすると、定義した外部 URL に実際の属性値が代入された状態で遷移します。

### データリンクの前提条件

AppDynamics でアプリケーションの URL をコピーします。アプリケーションを識別する URL の重要な部分は、URL のクエリパラメータです（例: `&application=99999`）。
アプリケーションクエリパラメータを含む完全な URL を使用して、グローバルデータリンクを構築します。
![AppD Application ID](../_images/app-url.png)

## グローバルデータリンクの作成

1. Splunk Observability Cloud で、左側のナビゲーションパネルにある **Settings**（歯車アイコン）をクリックします。
2. **Global Data Links** をクリックします。
3. **New Link** をクリックします。
4. リンクを設定します:

| フィールド               | 値                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Link Label**      | `Open in AppDynamics`                                                                                                                        |
| **Link to**         | `Custom URL`                                                                                                                                 |
| **Show on**         | `Property:Value pair` - `appd.app.name:<YOUR APPLICATION NAME>` を選択します（例: `appd.app.name:Dual-Ingest-JRH`）                                                                                                                                 |
| **URL**             | `https://se-lab.saas.appdynamics.com/controller/#/location=APP_DASHBOARD&timeRange=Custom_Time_Range.BETWEEN_TIMES.{{ end_time }}.{{ start_time }}.6&application=<YOUR_APPLICATION_ID_NUMBER>&dashboardMode=force` |
| **Time format**         | `Unix time: epoch milliseconds`                                                                                                                                 |
| **Minimum trigger** | `appd.tier.name`                                                                                                                             |

{{% notice title="URL テンプレート構文" style="primary" icon="lightbulb" %}}
二重波括弧 `{{ end_time }}` と `{{ start_time }}` はテンプレート変数です。Splunk Observability Cloud がクリック時に実際の値に置き換えます。

`<YOUR_APPLICATION_ID_NUMBER>` は、特定のアプリケーションのクエリパラメータから取得した番号です。
{{% /notice %}}
![Global Datalink Config](../_images/global-datalink-config.png?width=50vw)

5. **Save** をクリックします。

## グローバルデータリンクのテスト

1. **APM** に戻り、**OrderService** サービスのトレースを開きます。
2. ルートスパンをクリックして属性を表示します。
3. 属性リストで `appd.app.name` を見つけます。**Open in AppDynamics** というラベルのクリック可能なリンクになっているはずです。
4. リンクをクリックします。新しいブラウザタブが開き、AppDynamics Controller の **OrderService** アプリケーションビューに直接遷移します。
![Global Datalink Config](../_images/datalink.png?width=20vw)

{{% notice title="注意" style="info" icon="info-circle" %}}
リンクが機能するためには、同じブラウザで AppDynamics Controller にログインしている必要があります。ログインを求められた場合は、Cisco の資格情報を使用してください。
{{% /notice %}}

## 逆方向のナビゲーション（AppD から Splunk へ）

逆方向のナビゲーションも可能です。デュアルモードでキャプチャされた AppDynamics スナップショットには、**Data Collectors** タブの下に OTel の `TraceId` が含まれています。

Splunk Observability Cloud で対応するトレースを見つけるには:

1. AppDynamics Controller で、ビジネストランザクションの **Transaction Snapshot** を開きます。
2. **Data Collectors** タブに移動します。
3. `TraceId` の値を見つけます。
4. Splunk Observability Cloud で、**APM → Traces** に移動し、そのトレース ID を検索します。

これにより、2つのプラットフォーム間の**双方向の関連付け**が実現されます。
![AppDynamics Trace ID](../_images/appd-traceid.png?width=30vw)
