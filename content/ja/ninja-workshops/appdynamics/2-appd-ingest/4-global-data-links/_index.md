---
title: "フェーズ3: Global Data Links"
linkTitle: 4. Global Data Links
weight: 4
archetype: chapter
time: 10 minutes
description: appd.* Span属性を使用して、対応するAppDynamicsのティアビューに直接移動するGlobal Data LinkをSplunk Observability Cloudで作成します。
---

{{% notice title="注意" style="primary" icon="lightbulb" %}}
グループワークショップに参加している場合は、インストラクターの指示に従い、Global Data Linksの追加作成は控えてください。
このセクションを自分で完了する必要はありません。手順は学習およびドキュメント目的で記載されています。
ご理解ありがとうございます。
{{% /notice %}}

トレースの `appd.*` 属性は単なるメタデータではありません。Splunk Observability Cloudでトレースを表示しているユーザーが、ワンクリックで対応するAppDynamicsビューに直接ジャンプできる **Global Data Links** を構成できます。

## Global Data Linksとは

Global Data Linksは、Span属性、タグ値、またはメトリクスディメンションにクリック可能なリンクを作成するSplunk Observability Cloudの機能です。ユーザーがリンクされた値をクリックすると、実際の属性値がURLテンプレートに代入された外部URLに移動します。

### Data Linkの前提条件

AppDynamicsでアプリケーションのURLをコピーします。アプリケーションを識別するURLの重要な部分は、URLのクエリパラメータです（例: `&application=99999`）。
applicationクエリパラメータを含む完全なURLを使用してGlobal Data Linkを構築します。
![AppD Application ID](../_images/app-url.png)

## Global Data Linkの作成

1. Splunk Observability Cloudで、左側のナビゲーションパネルの **Settings**（歯車アイコン）をクリックします。
2. **Global Data Links** をクリックします。
3. **New Link** をクリックします。
4. リンクを設定します。

| フィールド               | 値                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Link Label**      | `Open in AppDynamics`                                                                                                                        |
| **Link to**         | `Custom URL`                                                                                                                                 |
| **Show on**         | `Property:Value pair` - `appd.app.name:<YOUR APPLICATION NAME>` を選択（例: `appd.app.name:Dual-Ingest-JRH`）                                                                                                                                 |
| **URL**             | `https://se-lab.saas.appdynamics.com/controller/#/location=APP_DASHBOARD&timeRange=Custom_Time_Range.BETWEEN_TIMES.{{ end_time }}.{{ start_time }}.6&application=<YOUR_APPLICATION_ID_NUMBER>&dashboardMode=force` |
| **Time format**         | `Unix time: epoch milliseconds`                                                                                                                                 |
| **Minimum trigger** | `appd.tier.name`                                                                                                                             |

{{% notice title="URLテンプレート構文" style="primary" icon="lightbulb" %}}
二重中括弧 `{{ end_time }}` と `{{ start_time }}` はテンプレート変数です。Splunk Observability Cloudがクリック時に実際の値に置換します。

`<YOUR_APPLICATION_ID_NUMBER>` は、対象アプリケーションのクエリパラメータから取得した番号です。
{{% /notice %}}
![Global Datalink Config](../_images/global-datalink-config.png?width=50vw)

1. **Save** をクリックします。

## Global Data Linkのテスト

1. **APM** に戻り、 **OrderService** サービスのトレースを開きます。
2. ルートSpanをクリックして属性を表示します。
3. 属性リストで `appd.app.name` を見つけます。 **Open in AppDynamics** というラベルのクリック可能なリンクになっているはずです。
4. リンクをクリックします。新しいブラウザタブが開き、AppDynamics Controllerの **OrderService** アプリケーションビューに直接移動します。
![Global Datalink Config](../_images/datalink.png?width=20vw)

{{% notice title="注意" style="info" icon="info-circle" %}}
リンクが機能するには、同じブラウザでAppDynamics Controllerにログインしている必要があります。ログインを求められた場合は、Ciscoの資格情報を使用してください。
{{% /notice %}}

## 逆方向のナビゲーション（AppDからSplunkへ）

逆方向のナビゲーションも可能です。デュアルモードでキャプチャされたAppDynamicsスナップショットには、 **Data Collectors** タブにOTelの `TraceId` が含まれています。

Splunk Observability Cloudで対応するトレースを見つけるには、以下の手順を実行します。

1. AppDynamics Controllerで、ビジネストランザクションの **Transaction Snapshot** を開きます。
2. **Data Collectors** タブに移動します。
3. `TraceId` の値を見つけます。
4. Splunk Observability Cloudで **APM → Traces** に移動し、そのトレースIDを検索します。

これにより、2つのプラットフォーム間の **双方向の関連付け** が実現します。
![AppDynamics Trace ID](../_images/appd-traceid.png?width=30vw)
