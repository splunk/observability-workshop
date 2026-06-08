---
title: "Phase 3: Global Data Links"
linkTitle: 4. Global Data Links
weight: 4
archetype: chapter
time: 10 minutes
description: appd.* スパン属性を使用して、対応する AppDynamics ティアビューに直接ナビゲートするグローバルデータリンクを Splunk Observability Cloud で作成します。
---

{{% notice title="注意" style="primary" icon="lightbulb" %}}
グループワークショップに参加している場合は、インストラクターの指示に従い、グローバルデータリンクを追加で作成しないでください。
このセクションをご自身で完了する必要はありません。手順はイネーブルメントおよびドキュメントの目的で記載されています。
ご協力ありがとうございます！
{{% /notice %}}

トレース上の `appd.*` 属性は単なるメタデータではありません。Splunk Observability Cloud でトレースを表示している誰もが、ワンクリックで対応する AppDynamics ビューに直接ジャンプできる**グローバルデータリンク**を実現します。

## グローバルデータリンクとは？

グローバルデータリンクは、スパン属性、タグ値、またはメトリクスディメンションにクリック可能なリンクを作成する Splunk Observability Cloud の機能です。ユーザーがリンクされた値をクリックすると、実際の属性値が URL テンプレートに代入された外部 URL に移動します。

### データリンクの前提条件

AppDynamics でアプリケーションの URL をコピーします。アプリケーションを識別する URL の重要な部分は、URL のクエリパラメータです（例: `&application=99999`）。
アプリケーションクエリパラメータを含む完全な URL を使用してグローバルデータリンクを構築します。
![AppD Application ID](../_images/app-url.png)

## グローバルデータリンクの作成

1. Splunk Observability Cloud で、左側のナビゲーションパネルの **Settings**（歯車アイコン）をクリックします。
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
二重中括弧 `{{ end_time }}` と `{{ start_time }}` はテンプレート変数です。Splunk Observability Cloud がクリック時に実際の値に置換します。

`<YOUR_APPLICATION_ID_NUMBER>` は、ご自身のアプリケーションのクエリパラメータから取得した番号です。
{{% /notice %}}
![Global Datalink Config](../_images/global-datalink-config.png?width=50vw)

5. **Save** をクリックします。

## グローバルデータリンクのテスト

1. **APM** に戻り、**OrderService** サービスのトレースを開きます。
2. ルートスパンをクリックして属性を表示します。
3. 属性リストで `appd.app.name` を探します。**Open in AppDynamics** というラベルのクリック可能なリンクになっているはずです。
4. リンクをクリックします。新しいブラウザタブが開き、AppDynamics Controller の **OrderService** アプリケーションビューに直接移動します。
![Global Datalink Config](../_images/datalink.png?width=20vw)

{{% notice title="注意" style="info" icon="info-circle" %}}
リンクが機能するには、同じブラウザで AppDynamics Controller にログインしている必要があります。ログインを求められた場合は、Cisco の認証情報を使用してください。
{{% /notice %}}

## 逆方向のナビゲーション（AppDynamics から Splunk へ）

逆方向のナビゲーションも可能です。デュアルモードでキャプチャされた AppDynamics スナップショットには、**Data Collectors** タブの下に OTel の `TraceId` が含まれています。

Splunk Observability Cloud で対応するトレースを見つけるには:

1. AppDynamics Controller で、ビジネストランザクションの **Transaction Snapshot** を開きます。
2. **Data Collectors** タブに移動します。
3. `TraceId` の値を見つけます。
4. Splunk Observability Cloud で、**APM → Traces** に移動し、そのトレース ID を検索します。

これにより、2つのプラットフォーム間の**双方向の関連付け**が実現します。
![AppDynamics Trace ID](../_images/appd-traceid.png?width=30vw)
