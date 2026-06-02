---
title: 分散トレーシングと双方向ドリルダウン
linkTitle: 4. 分散トレーシング
weight: 4
time: 25 minutes
description: ThousandEyes と Splunk APM の間でサポートされているトレース相関を有効にし、チームが調査中に両製品間を移動できるようにします。
---

このセクションでは、ThousandEyes と Splunk の統合を真の調査ワークフローへと発展させます。前のセクションでは、ThousandEyes が Synthetic メトリクスを Splunk Observability Cloud にストリーミングしました。このセクションでは、サポートされている **ThousandEyes <-> Splunk APM 分散トレーシング統合** を有効化し、ネットワーク、プラットフォーム、アプリケーションの各チームが同じリクエストを見ながら両ツール間をピボットできるようにします。

{{% notice title="なぜこれが重要なのか" style="primary" icon="lightbulb" %}}
これは、2つの環境間で **双方向アクセス** を可能にする要素です。ThousandEyes から Splunk APM の関連トレースを開くことができ、Splunk APM から元の ThousandEyes テストへ戻ることができます。
{{% /notice %}}

## 学習内容

このセクションが終わると、以下のことができるようになります。

- 内部サービスを計装して Splunk APM にトレースを送信する
- ThousandEyes の **HTTP Server** または **API** テストで分散トレーシングを有効化する
- Splunk APM 用に ThousandEyes の **Generic Connector** を構成する
- ThousandEyes の **Service Map** を開き、対応する Splunk のトレースに直接ジャンプする
- Splunk APM 内の ThousandEyes メタデータを利用して、元の ThousandEyes テストへ戻る
