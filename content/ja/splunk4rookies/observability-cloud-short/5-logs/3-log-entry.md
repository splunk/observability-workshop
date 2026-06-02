---
title: 3. ログエントリの確認
weight: 3
---

{{% exercise title="エラーログを開く" %}}

* ログテーブル内のエラーエントリをクリックしてください（リストに別サービスからの稀なエラーが含まれている場合もあるため、`hostname: "paymentservice-xxxx"` と表示されていることを確認してください）。
{{< tabs >}}
{{% tab title="Question" %}}
**メッセージの内容から、この問題を解決するために開発チームに何をするよう伝えますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**開発チームは、有効な API Token を使用してコンテナを再ビルドおよび再デプロイするか、`v350.9` にロールバックする必要があります**。
{{% /tab %}}
{{< /tabs >}}

  ![Log Message](../images/log-observer-log-message.png)
* ログメッセージペインの **X** をクリックして閉じます。

{{% /exercise %}}

{{% notice style="blue" title="おめでとうございます" icon="wine-bottle" %}}

Splunk Observability Cloud を使い、Online Boutique でのショッピング中に発生したユーザー体験の悪化の原因を**首尾よく**把握できました。RUM、APM、ログを活用してサービス全体で何が起きていたのかを理解し、その上で根本原因を特定するに至りました。すべて、オブザーバビリティの 3 本柱である **metrics**、**traces**、**logs** に基づいた取り組みです。

また、**Tag Spotlight** による Splunk の **intelligent tagging and analysis** を使ってアプリケーションの挙動パターンを検出する方法と、**Related Content** の **full stack correlation** 機能を活用して問題のコンテキストを保ったまま異なるコンポーネント間を素早く行き来する方法も学習しました。

{{% /notice %}}

ワークショップの次のパートでは、**問題発見モード**から**緩和**、**予防**、そして**プロセス改善モード**へと移行します。
