---
title: 1.2 Real Browser Testの作成
weight: 2
---

先ほど保存したレコーディングはローカルファイルです。アラートを発報することも、午前3時にロンドンから実行することも、昨日チェックアウトが遅かったかどうかを教えてくれることもできません。レコーディングからSplunk Synthetic Monitoringテストに移行することで、これらすべてが可能になります。同じユーザージャーニーを、選択したクラウドロケーションから継続的に実行し、結果はメトリクス、ログ、トレースと同じObservability Cloud組織に流れ込みます。

Splunk Observability Cloudで **Synthetics** に移動します。ランディングページにはSynthetic Monitoringの3つのチェックタイプが表示されます

- **Browser tests** — 今日構築するフルChromiumのリアルユーザージャーニーチェック。
- **Uptime tests** — 軽量なポートおよびHTTP可用性チェック。
- **API tests** — マルチステップHTTPトランザクションチェック（パート2で構築します）。

{{% button style="blue" %}}Add new test{{% /button %}} をクリックし、ドロップダウンから **Browser test** を選択します。

![Add new test](../../img/add-new-test.png)

**Browser test content** 設定ページが表示されます。ここで、先ほどエクスポートしたJSONをインポートし、テストの実行場所と頻度を設定し、オンコールエンジニアが実行結果を一目で読めるように各ステップに名前を付けます。

![New Test](../../img/new-test.png)
