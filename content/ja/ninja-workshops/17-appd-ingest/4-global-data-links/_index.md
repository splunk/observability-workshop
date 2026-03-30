---
title: "フェーズ 3: グローバルデータリンク"
linkTitle: 4. グローバルデータリンク
weight: 4
archetype: chapter
time: 10 minutes
description: appd.* スパン属性を使用して、対応する AppDynamics ティアビューに直接ナビゲートするグローバルデータリンクを Splunk Observability Cloud で作成します。
---

トレースの `appd.*` 属性は単なるメタデータではありません。これらを使用して**グローバルデータリンク**を作成することで、Splunk Observability Cloudでトレースを表示しているユーザーが、ワンクリックで対応するAppDynamicsビューに直接ジャンプできるようになります。

## グローバルデータリンクとは？

グローバルデータリンクは、スパン属性、タグ値、またはメトリクスディメンションにクリック可能なリンクを作成するSplunk Observability Cloudの機能です。ユーザーがリンクされた値をクリックすると、定義した外部URLに移動します。その際、実際の属性値がURLテンプレートに代入されます。

### データリンクの前提条件

AppDynamicsでアプリケーションのURLをコピーしてください。アプリケーションを識別するURLの重要な部分は、URLのクエリパラメータです（例：`&application=99999`）。
アプリケーションクエリパラメータを含む完全なURLを使用して、グローバルデータリンクを構築します。
![AppD Application ID](../_images/app-url.png)

## グローバルデータリンクの作成

1. Splunk Observability Cloudで、左側のナビゲーションパネルにある **Settings**（歯車アイコン）をクリックします。
2. **Global Data Links** をクリックします。
3. **New Link** をクリックします。
4. リンクを設定します：

| フィールド               | 値                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Link Label**      | `Open in AppDynamics`                                                                                                                        |
| **Link to**         | `Custom URL`                                                                                                                                 |
| **Show on**         | `Property:Value pair` - `appd.app.name:<YOUR APPLICATION NAME>` を選択（例：`appd.app.name:Dual-Ingest-JRH`）                                                                                                                                 |
| **URL**             | `https://se-lab.saas.appdynamics.com/controller/#/location=APP_DASHBOARD&timeRange=Custom_Time_Range.BETWEEN_TIMES.{{ end_time }}.{{ start_time }}.6&application=<YOUR_APPLICATION_ID_NUMBER>&dashboardMode=force` |
| **Time format**         | `Unix time: epoch milliseconds`                                                                                                                                 |
| **Minimum trigger** | `appd.tier.name`                                                                                                                             |

{{% notice title="URLテンプレート構文" style="primary" icon="lightbulb" %}}
二重波括弧 `{{ end_time }}` と `{{ start_time }}` はテンプレート変数です。Splunk Observability Cloudは、クリック時に実際の値に置換します。

`<YOUR_APPLICATION_ID_NUMBER>` は、特定のアプリケーションのクエリパラメータに含まれる番号です。
{{% /notice %}}
![Global Datalink Config](../_images/global-datalink-config.png?width=50vw)

5. **Save** をクリックします。

## グローバルデータリンクのテスト

1. **APM** に戻り、**OrderService** サービスのトレースを開きます。
2. ルートスパンをクリックして、その属性を表示します。
3. 属性リストで `appd.app.name` を見つけます。これは **Open in AppDynamics** というラベルのクリック可能なリンクになっているはずです。
4. リンクをクリックします。新しいブラウザタブが開き、AppDynamics Controllerの **OrderService** アプリケーションビューに直接移動します。
![Global Datalink Config](../_images/datalink.png?width=20vw)

{{% notice title="注意" style="info" icon="info-circle" %}}
リンクが機能するには、同じブラウザでAppDynamics Controllerにログインしている必要があります。ログインを求められた場合は、Ciscoの認証情報を使用してください。
{{% /notice %}}

## 逆方向へのナビゲーション（AppD から Splunk へ）

逆方向へのナビゲーションも可能です。デュアルモードでキャプチャされたAppDynamicsスナップショットには、**Data Collectors** タブの下にOTelの `TraceId` が含まれています。

Splunk Observability Cloudで対応するトレースを見つけるには：

1. AppDynamics Controllerで、ビジネストランザクションの **Transaction Snapshot** を開きます。
2. **Data Collectors** タブに移動します。
3. `TraceId` の値を見つけます。
4. Splunk Observability Cloudで、**APM → Traces** に移動し、そのトレースIDを検索します。

これにより、2つのプラットフォーム間で**双方向の関連付け**が可能になります。
![AppDynamics Trace ID](../_images/appd-traceid.png?width=30vw)
