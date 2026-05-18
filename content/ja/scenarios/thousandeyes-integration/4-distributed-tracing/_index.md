---
title: 分散トレーシングと双方向ドリルダウン
linkTitle: 4. Distributed Tracing
weight: 4
time: 25 minutes
description: ThousandEyes と Splunk APM 間のトレース相関を有効にし、調査中にチームが両製品間をシームレスに移動できるようにします。
---

このセクションでは、ThousandEyes と Splunk の連携を本格的な調査ワークフローに変えます。前のセクションでは、ThousandEyes がシンセティックメトリクスを Splunk Observability Cloud にストリーミングしました。このセクションでは、サポートされている **ThousandEyes <-> Splunk APM 分散トレーシング連携** を有効にし、ネットワーク、プラットフォーム、アプリケーションの各チームが同じリクエストを確認しながら両方のツール間を行き来できるようにします。

{{% notice title="なぜこれが重要なのか" style="primary" icon="lightbulb" %}}
これは、2つの環境間の **双方向アクセス** を実現する重要な要素です。ThousandEyes から Splunk APM の関連トレースを開くことができ、Splunk APM から元の ThousandEyes テストに戻ることもできます。
{{% /notice %}}

## 学習内容

このセクションを完了すると、以下のことができるようになります

- 内部サービスをインストルメントして Splunk APM にトレースを送信する
- ThousandEyes の **HTTP Server** または **API** テストで分散トレーシングを有効にする
- Splunk APM 用の ThousandEyes **Generic Connector** を設定する
- ThousandEyes の **Service Map** を開き、対応する Splunk トレースに直接ジャンプする
- Splunk APM の ThousandEyes メタデータを使用して、元の ThousandEyes テストに戻る
