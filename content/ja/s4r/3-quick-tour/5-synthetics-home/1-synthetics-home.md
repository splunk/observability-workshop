---
title: Syntheticsホームページ
linkTitle: 5.1 Syntheticsホームページ
weight: 2
---

**Synthetics** をメインメニューでクリックしてみましょう。Synthetics ホームページに移動したはずです。このページには、役立つ情報を確認したり、Synthetic テストを選択または作成する3つのセクションがあります。

![Synthetic main](../images/synthetics-main.png)

1. **オンボーディングパネル:** Splunk Synthetics を始めるためのトレーニングビデオとドキュメンテーションへのリンク。
2. **テストパネル:** 設定されているすべてのテストのリスト（**Browser**、**API**、および **Uptime**）
3. **Add new test:** 新しい Synthetic テストを作成するためのドロップダウン。

{{% notice title="Info" style="info" %}}
ワークショップの一環として、実行中のアプリケーションに対するブラウザーテストを用意しています。テストパネル（**2**）で見つけることができるはずです。テストの名前は **Workshop Browser Test for** のあとにワークショップの名前を続けたものとなります（講師が名前をご連絡いたします）。
{{% /notice %}}

ツアーを続けましょう。ワークショップ用の Browser Test の結果を見てみます。

{{% notice title="Exercise" style="green" icon="running" %}}

* テストパネルで、ワークショップの名前が含まれている行をクリックします。以下のように表示されるはずです。

![Synthetics-overview](../images/synthetics-test-overview.png)

* Synthetic Tests ページでは、最後の1日、8日、および30日の間にサイトのパフォーマンスが表示されます。上のスクリーンショットに示されているように、テストがその期間より前に開始されていれば、対応するチャートにデータが表示されます。テストが作成された時点によっては、一部のデータが表示されない場合があります。
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

{{% notice title="Additional Exercise" style="red" icon="running" %}}

テスト結果に基づいて問題調査を行ったり、監視設定を行う方法は、**[8. Splunk Synthetics](https://splunk.github.io/observability-workshop/latest/ja/s4r/8-synthetics/index.html)** で取り組んでいただくことが可能です。

実行したテストの詳細をもうすこし確認してみましょう。

* 画面下部に、**Recent run results** という欄があるはずです。*Failed* になっている最新のテストをクリックしましょう
* テスト結果の詳細画面が表示されます。

![Synthetics-detail](../images/synthetic-detail.png)

* 画面最上部に赤くエラーが表示されていることを確認しましょう

![Synthetics-error](../images/synthetic-error.png)


* 1秒間隔のスクリーンショットが横並びに表示されています。*Every 1s* というプルダウンを変えると、スクリーンショットの表示間隔を変更できます
* また、その右側には、録画再生ウィンドウがあるはずです。再生してみましょう
* 録画再生ウィンドウの下部には、この処理に関するパフォーマンス情報が表示されます。Web Vitalなどに基づいてパフォーマンスが可視化されています
* *Business Transaction* は、テストで確認したい処理をグループ化して定義したものです。また、*Pages* は、テストの中で開かれた Web ページの URL を示しています
* それぞれクリックしてみると、それに該当する処理が画面下部に表示されます。どのような処理が順番に実施されたか、処理状況が示されています。
* *APM* というリンクが表示されているはずです
  * バックエンドアプリケーションを APM で計装している場合、Synthetic テストと APM のトレースを紐づけることができます

{{< tabs >}}
{{% tab title="質問" %}}
**このテストはなぜ *Failed* と判断されましたか**
{{% /tab %}}
{{% tab title="回答" %}}
***Place Order* 処理の後に *"Order Confirmation ID"* が表示されるまでに時間がかかり、タイムアウトしてしまった**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

次に、**Splunk Infrastructure Monitoring (IM)** を使用してアプリケーションが実行されているインフラストラクチャを調査しましょう。
