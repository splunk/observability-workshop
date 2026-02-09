---
title: Synthetics ホームページ
linkTitle: 5.1 Synthetics ホームページ
weight: 2
---

メインメニューで **Synthetics** をクリックします。Synthetics ホームページが表示されます。このページには、役立つ情報を提供したり、Synthetic テストを選択または作成したりできる 3 つの異なるセクションがあります。

![Synthetic main](../images/synthetics-main.png)

1. **Onboarding Pane:** Splunk Synthetics を使い始めるためのトレーニングビデオとドキュメントへのリンクです。
2. **Test Pane:** 設定されているすべてのテスト（**Browser**、**API**、**Uptime**）のリストです。
3. **Create Test Pane:** 新しい Synthetic テストを作成するためのドロップダウンです。

{{% notice title="Info" style="info" %}}
ワークショップの一環として、実行中のアプリケーションに対するデフォルトのブラウザテストを作成しました。Test Pane **(2)** で確認できます。テスト名は **Workshop Browser Test for** の後にワークショップ名が続きます（インストラクターから提供されているはずです）。
{{% /notice %}}
ツアーを続けるために、ワークショップの自動ブラウザテストの結果を見てみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* Test Pane で、ワークショップ名を含む行をクリックします。結果は次のようになります：

![Synthetics-overview](../images/synthetics-test-overview.png)

* Synthetic Tests ページでは、最初のペインにサイトの過去 1 日、8 日、30 日間のパフォーマンスが表示されます。上のスクリーンショットに示されているように、テストが十分に前に開始された場合にのみ、対応するチャートに有効なデータが含まれます。ワークショップの場合、これはいつ作成されたかによって異なります。
* Performance KPI ドロップダウンで、時間をデフォルトの 4 時間から過去 1 時間に変更します。
{{< tabs >}}
{{% tab title="Question" %}}
**テストはどのくらいの頻度で、どこから実行されますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**テストは Frankfurt、London、Paris から 1 分間隔のラウンドロビン方式で実行されます**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

次に、**Splunk Infrastructure Monitoring (IM)** を使用して、アプリケーションが実行されているインフラストラクチャを調べてみましょう。
