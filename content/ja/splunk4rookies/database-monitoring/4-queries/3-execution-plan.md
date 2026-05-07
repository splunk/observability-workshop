---
title: 3. 実行プラン
weight: 3
---

**実行プラン（execution plan）**は、クエリを実行するためにデータベースオプティマイザーが選択した戦略です。どのインデックスを使用するか、どの結合アルゴリズムを適用するか、どの順序で実行するかなどが含まれます。クエリが遅い場合、プランを見れば通常その理由がわかります。

Splunk Database Monitoring は各クエリサンプルに使用されたプランをキャプチャするため、SQL から推測するのではなく、エンジンが実際に何を行ったかを確認できます。

{{% notice title="プランで確認すべきポイント" style="info" %}}
最も一般的な警告サインは、**table scans**（使用可能なインデックスが存在しないためにエンジンがテーブル全体を読み取ること）、より適切なインデックスがあれば回避できる **expensive sorts**、および大量の行に対する **nested loop joins** です。これらを見つけるためにクエリチューニングの専門家である必要はありません。プランの可視化によって明示されます。
{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

* 遅いサンプルが選択された状態で、右側のペインの **Execution plan** セクションまでスクロールします。
* プランを確認し、主要な操作を記録します。**Index Seek**、**Index Scan**、**Table Scan** のいずれですか？

<!-- TODO screenshot: Execution plan view for a query sample, ideally showing a Table Scan or other expensive operation -->
![実行プラン](../images/execution-plan.png)

{{< tabs >}}
{{% tab title="質問" %}}
**プランが大きなテーブルで Table Scan を示している場合、考えられる修正方法は何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**WHERE 句のカラムにカバリングインデックスを追加します。** その後、オプティマイザーが実際にそのインデックスを使用していることを確認します。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
