---
title: 1. 遅いクエリから APM トレースへ
weight: 1
---

遅いクエリを呼び出しているアプリケーションが **Splunk APM**（.NET または Java）でインストルメントされている場合、Database Monitoring にはそのクエリを実行した APM トレースに直接移動できる **Related Content** リンクが表示されます。クエリ ID を別のツールにコピーしたり、適切なトレース検索を推測したりする必要はありません。

これがループを閉じる瞬間です。「データベースが遅い気がする」から始まり、開発者が開いて修正できる特定のアプリケーショントレースにたどり着きます。

{{% notice title=".NET and Java" style="info" %}}
クエリからトレースへの相関には、呼び出し元のアプリケーションが Splunk distribution of OpenTelemetry for **.NET** または **Java** でインストルメントされており、データベースクエリの相関が有効になっている必要があります。Related Content リンクが表示されない場合、アプリケーションがインストルメントされていないか、相関機能が有効になっていない可能性があります。
{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

* Navigator の **Queries** タブに戻り、調査対象のクエリを再度選択します。
* 右側の詳細ペインで、ページ下部にある **Related Content** セクションを探します。
* **APM** リンクをクリックして、このクエリを実行したトレースの一覧に移動します **(1)**。
* トレースを1つ選択し、**Trace Waterfall** をクリックして、クエリに至るまでのバックエンドの呼び出しチェーン全体を確認します。

<!-- TODO screenshot: Database Monitoring query view with the Related Content → APM link annotated (1), and a follow-up screenshot of the resulting Trace Waterfall view -->
![Database to APM correlation](../images/db-to-apm-link.png)

{{< tabs >}}
{{% tab title="質問" %}}
**Trace Waterfall を見て、どのアプリケーションサービスがクエリを発行したか、またリクエストがデータベースに到達する前にどのような処理を行ったかを確認できますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**はい — Waterfall にはリクエスト内のすべての span が表示され、データベースコールはリーフ span として現れます。** これにより、アプリケーションチームは呼び出し元を修正するために必要な完全なコンテキストを得ることができます。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
