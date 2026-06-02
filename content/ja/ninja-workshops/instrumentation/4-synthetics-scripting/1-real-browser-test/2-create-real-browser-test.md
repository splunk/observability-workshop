---
title: 1.2 Real Browser Test の作成
weight: 2
---

先ほど保存したレコーディングはローカルファイルにすぎません。アラートを発報することも、ロンドンから午前3時に実行することも、昨日のチェックアウトが遅かったかどうかを教えてくれることもできません。レコーディングから Splunk Synthetic Monitoring テストへ移行することで、これらすべてが可能になります。同じユーザージャーニーが、選択したクラウドロケーションから継続的に実行され、その結果はメトリクス、ログ、トレースと同じ Observability Cloud 組織に流れ込みます。

Splunk Observability Cloud で **Synthetics** に移動します。ランディングページには Synthetic Monitoring の3種類のチェックが表示されています:

- **Browser tests** — 本日構築する、完全な Chromium による実ユーザージャーニーチェックです。
- **Uptime tests** — 軽量なポートおよび HTTP の可用性チェックです。
- **API tests** — 複数ステップの HTTP トランザクションチェックです (Part 2 で構築します)。

{{% button style="blue" %}}Add new test{{% /button %}} をクリックし、ドロップダウンから **Browser test** を選択します。

![Add new test](../../img/add-new-test.png)

続いて **Browser test content** 設定ページが表示されます。ここで、先ほどエクスポートした JSON をインポートし、テストの実行場所と頻度を設定し、各ステップに名前を付けます。これにより、オンコールエンジニアが実行結果を一目で読み取れるようになります。

![New Test](../../img/new-test.png)
