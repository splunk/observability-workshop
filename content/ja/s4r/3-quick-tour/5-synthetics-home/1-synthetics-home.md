---
title: Synthetics Home Page
linkTitle: 5.1 Synthetics Home Page
weight: 2
---

**Synthetics** をメインメニューでクリックしてみましょう。これにより Synthetics ホームページに移動します。このページには、役立つ情報を確認したり、Synthetic テストを選択または作成したりするための3つのセクションがあります。

![Synthetic main](../images/synthetics-main.png)

1. **オンボーディングパネル:** Splunk Synthetics を始めるためのトレーニングビデオとドキュメンテーションへのリンク。
2. **テストパネル:** 設定されているすべてのテストのリスト（**Browser**、**API**、および **Uptime**）
3. **Add new test:** 新しい Synthetic テストを作成するためのドロップダウン。

{{% notice title="Info" style="info" %}}
ワークショップの一環として、実行しているアプリケーションに対するデフォルトのブラウザーテストが作成されています。テストパネル（**2**）で見つけることができます。その名前はワークショップの名前に続いて **Workshop Browser Test for** となります（講師が名前をご連絡いたします）。
{{% /notice %}}

ツアーを続けましょう。ワークショップ用の自動ブラウザーテストの結果を見てみます。

{{% notice title="Exercise" style="green" icon="running" %}}

* テストパネルで、ワークショップの名前が含まれている行をクリックします。以下のように表示されるはずです。

![Synthetics-overview](../images/synthetics-test-overview.png)

* Synthetic Tests ページでは、最後の1日、8日、および30日の間にサイトのパフォーマンスが表示されます。上のスクリーンショットに示されているように、テストが過去に十分に開始された場合のみ、対応するチャートに有効なデータが含まれます。テストが作成された時点によっては、一部のデータが表示されない場合があります。
* Performance KPI のドロップダウンで、デフォルトの last 4 hours から last 1 hour に時間を変更してください。
{{< tabs >}}
{{% tab title="質問" %}}
**テストはどれくらいの頻度で実行され、どこから実行されていますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**テストはフランクフルト、ロンドン、およびパリから、1分間隔のラウンドロビンで実行されます**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

次に、**Splunk Infrastructure Monitoring (IM)** を使用してアプリケーションが実行されているインフラストラクチャを調査しましょう。
