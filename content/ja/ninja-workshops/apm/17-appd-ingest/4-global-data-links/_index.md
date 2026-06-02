---
title: "Phase 3: Global Data Links"
linkTitle: 4. Global Data Links
weight: 4
archetype: chapter
time: 10 minutes
description: appd.* スパン属性を使用して、対応する AppDynamics の tier ビューに直接遷移する global data link を Splunk Observability Cloud に作成します。
---

{{% notice title="NOTICE" style="primary" icon="lightbulb" %}}
グループワークショップに参加している場合は、インストラクターの操作を確認するだけにとどめ、追加の global data link を作成しないでください。
このセクションをご自身で完了する必要はありません。手順は学習目的とドキュメント目的で記載されています。
ご協力ありがとうございます。
{{% /notice %}}

トレース上の `appd.*` 属性は単なるメタデータではありません。これらは **global data links** を実現するための情報源となり、Splunk Observability Cloud でトレースを閲覧している人なら誰でも、対応する AppDynamics のビューにワンクリックで直接ジャンプできるようにします。

## Global Data Links とは

Global data links は Splunk Observability Cloud の機能で、スパン属性、タグ値、メトリクスのディメンションに対してクリック可能なリンクを作成します。ユーザーがリンクされた値をクリックすると、定義した外部 URL に遷移し、URL テンプレートには実際の属性値が代入されます。

### Data Link の前提条件

AppDynamics 内のアプリケーションへの URL をコピーします。アプリケーションを識別する URL の重要な部分は、URL のクエリパラメーターです（例： `&application=99999`）。
application クエリパラメーターを含む完全な URL を使用して global data link を構築します。
![AppD Application ID](../_images/app-url.png)

## Global Data Link の作成

1. Splunk Observability Cloud で、左側のナビゲーションパネルにある **Settings**（歯車アイコン）をクリックします。
2. **Global Data Links** をクリックします。
3. **New Link** をクリックします。
4. リンクを設定します。

| Field               | Value                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Link Label**      | `Open in AppDynamics`                                                                                                                        |
| **Link to**         | `Custom URL`                                                                                                                                 |
| **Show on**         | `Property:Value pair` - `appd.app.name:<YOUR APPLICATION NAME>` を選択（例： `appd.app.name:Dual-Ingest-JRH`）                                                                                                                                 |
| **URL**             | `https://se-lab.saas.appdynamics.com/controller/#/location=APP_DASHBOARD&timeRange=Custom_Time_Range.BETWEEN_TIMES.{{ end_time }}.{{ start_time }}.6&application=<YOUR_APPLICATION_ID_NUMBER>&dashboardMode=force` |
| **Time format**         | `Unix time: epoch milliseconds`                                                                                                                                 |
| **Minimum trigger** | `appd.tier.name`                                                                                                                             |

{{% notice title="URL Template Syntax" style="primary" icon="lightbulb" %}}
二重中括弧の `{{ end_time }}` および `{{ start_time }}` はテンプレート変数です。Splunk Observability Cloud は、クリック時にこれらを実際の値に置き換えます。

`<YOUR_APPLICATION_ID_NUMBER>` は、特定のアプリケーションのクエリパラメーターから取得した番号です。
{{% /notice %}}
![Global Datalink Config](../_images/global-datalink-config.png?width=50vw)

1. **Save** をクリックします。

## Global Data Link のテスト

1. **APM** に戻り、**OrderService** サービスのトレースを開きます。
2. ルートスパンをクリックして、その属性を表示します。
3. 属性リストから `appd.app.name` を見つけます。**Open in AppDynamics** とラベル付けされたクリック可能なリンクになっているはずです。
4. リンクをクリックします。新しいブラウザタブが開き、AppDynamics Controller の **OrderService** アプリケーションビューに直接遷移します。
![Global Datalink Config](../_images/datalink.png?width=20vw)

{{% notice title="Note" style="info" icon="info-circle" %}}
リンクが機能するためには、同じブラウザで AppDynamics Controller にログインしている必要があります。ログインを求められた場合は、Cisco の認証情報を使用してください。
{{% /notice %}}

## 逆方向のナビゲーション（AppD から Splunk へ）

逆方向のナビゲーションも可能です。dual モードでキャプチャされた AppDynamics スナップショットには、**Data Collectors** タブの下に OTel の `TraceId` が含まれます。

Splunk Observability Cloud で対応するトレースを見つけるには、以下を行います。

1. AppDynamics Controller で、ビジネストランザクションの **Transaction Snapshot** を開きます。
2. **Data Collectors** タブに移動します。
3. `TraceId` の値を見つけます。
4. Splunk Observability Cloud で **APM → Traces** に移動し、そのトレース ID を検索します。

これにより、両プラットフォーム間の **双方向の関連付け** が可能になります。
![AppDynamics Trace ID](../_images/appd-traceid.png?width=30vw)
