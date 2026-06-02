---
title: 2. ログエントリの確認
weight: 2
---

特定のログ行を確認する前に、Observability の3つの柱に基づいて、これまでに行ったことと、なぜここに到達したのかを簡単に振り返ります:

| Metrics | Traces | Logs |
|:-------:|:------:|:----:|
| _**問題があるか?**_ | _**問題はどこにあるか?**_ | _**問題は何か?**_ |

* メトリクスを使用して、アプリケーションに **問題がある** ことを特定しました。これは Service Dashboards のエラー率が想定よりも高かったため明らかでした。
* トレースと span tags を使用して、**問題がどこにあるか** を見つけました。**paymentservice** には `v350.9` と `v350.10` の2つのバージョンがあり、`v350.10` のエラー率は **100%** でした。
* この **paymentservice** `v350.10` のエラーが複数回のリトライを引き起こし、Online Boutique の checkout からの応答に長い遅延を発生させていることを確認しました。
* トレースから **Related Content** の機能を使って、失敗している **paymentservice** バージョンのログエントリにたどり着きました。これで **問題が何か** を判断できます。

{{% exercise title="エラーログを開く" %}}

* ログテーブル内のエラーエントリをクリックします (リスト内に他のサービスからの稀なエラーが含まれている場合に備えて、`hostname: "paymentservice-xxxx"` と表示されていることを確認してください)。
{{< tabs >}}
{{% tab title="Question" %}}
**メッセージに基づいて、開発チームに問題を解決するために何をするように伝えますか?**
{{% /tab %}}
{{% tab title="Answer" %}}
**開発チームは、有効な API Token でコンテナを再ビルドしてデプロイするか、`v350.9` にロールバックする必要があります**。
{{% /tab %}}
{{< /tabs >}}

  ![Log Message](../images/log-observer-log-message.png)
* ログメッセージペインの **X** をクリックして閉じます。

{{% /exercise %}}

{{% notice style="blue" title="Congratulations" icon="wine-bottle" %}}

Splunk Observability Cloud を使用して、Online Boutique でのショッピング中に発生した不快なユーザー体験の理由を **正常に** 理解しました。RUM、APM、ログを使用してサービスランドスケープで何が起きたかを理解し、その後、Observability の3つの柱である **metrics**、**traces**、**logs** に基づいて根本原因を発見しました。

また、**Tag Spotlight** による Splunk の **intelligent tagging and analysis** を使用してアプリケーションの挙動からパターンを検出する方法、および問題のコンテキストを保ったまま異なるコンポーネント間を素早く移動するために **Related Content** の **full stack correlation** の機能を使用する方法も学びました。

{{% /notice %}}

ワークショップの次のパートでは、**problem-finding mode** から **mitigation**、**prevention**、**process improvement mode** へと移行します。

次は、カスタムダッシュボードでのログチャートの作成です。
