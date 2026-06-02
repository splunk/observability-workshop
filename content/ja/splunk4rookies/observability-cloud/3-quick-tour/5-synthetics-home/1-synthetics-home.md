---
title: Synthetics ホームページ
linkTitle: 5.1 Synthetics ホームページ
weight: 2
---

メインメニューの **Digital Experience** をクリックし、Synthetic Monitoring の下にある **Synthetic Tests** をクリックします。これにより Synthetics ホームページが表示されます。このページには、有用な情報を提供するか、Synthetic Test を選択または作成できる 3 つの異なるセクションがあります。

![Synthetic main](../images/synthetics-main.png)

1. **Onboarding Pane:** Splunk Synthetics を使い始めるためのトレーニングビデオやドキュメントへのリンク。
2. **Test Pane:** 設定されているすべてのテスト（**Browser**、**API**、**HTTP**）のリスト。
3. **Create New Test:** 新しい Synthetic テストを作成するためのドロップダウン。

{{% notice title="情報" style="info" %}}
このワークショップの一環として、実行中のアプリケーションに対するデフォルトの Browser Test を作成しています。Test Pane **(2)** に表示されています。名前は **Workshop Browser Test for** に続いて、ワークショップ名（インストラクターから提供されているはずです）が付いています。
{{% /notice %}}
ツアーを続けるために、ワークショップの自動 Browser Test の結果を見てみましょう。

{{% exercise title="Synthetics 概要を開く" %}}

* Test Pane で、ワークショップ名が含まれる行をクリックします。結果は次のようになります：

![Synthetics-overview](../images/synthetics-test-overview.png)

* 注意：Synthetic Tests ページでは、最初のペインに過去 1 日、8 日、30 日のサイトのパフォーマンスが表示されます。上のスクリーンショットに示されているように、テストが十分過去に開始されている場合のみ、対応するチャートに有効なデータが含まれます。ワークショップでは、これは作成された時期によって異なります。
* Performance KPI ドロップダウンで、時間をデフォルトの 4 時間から過去 1 時間に変更します。
{{< tabs >}}
{{% tab title="質問" %}}
**テストはどのくらいの頻度で、どこから実行されますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**テストは** Frankfurt、London、Paris **から** 1 分間隔の **ラウンドロビン** で実行されます。
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

次に、**Splunk Infrastructure Monitoring (IM)** を使用して、アプリケーションが実行されているインフラストラクチャーを調べましょう。
