---
title: 1. インスタンス上のトップクエリ
weight: 1
---

Navigator の **Queries** タブには、このインスタンスで実行されている SQL ステートメントが一覧表示され、最も問題のあるものが上位に表示されます。各クエリについて、選択した時間範囲における集計メトリクス（通常は実行回数、合計実行時間、合計 CPU 時間、読み取り行数と返却行数）が表示されます。

**rows read vs. rows returned**（読み取り行数と返却行数）の比率は、最も有用なカラムの1つです。10行を返すために100万行を読み取るクエリは、ほぼ確実にフルスキャンを実行しているか、インデックスが欠落しています。単独では高速に見えても、CPU と I/O の両方を消費しています。

{{% notice title="演習" style="green" icon="running" %}}

* **Queries** タブで、リストをスキャンし、最初のカラムに表示されるクエリテキストを確認します。
* **Total duration** でソートされていない場合は、そのカラムでソートします。
* **Rows read** が **Rows returned** よりもはるかに大きいクエリを探します。それらが非効率の疑いがあるクエリです。

<!-- TODO screenshot: Queries tab showing a list of SQL statements ranked by total duration, with a row where rows-read >> rows-returned highlighted -->
![トップクエリ](../images/top-queries.png)

{{< tabs >}}
{{% tab title="質問" %}}
**平均実行時間が妥当であっても、読み取り行数と返却行数の比率が高いクエリが問題である理由は何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**そのクエリは、結果に必要な量をはるかに超える処理を行っています。** 負荷がかかると遅くなり、同じインスタンス上の他のクエリも必要とする I/O を消費しています。
{{% /tab %}}
{{< /tabs >}}

* 最も問題のあるクエリの**クエリテキスト**をクリックして開きます。右側のペインに詳細が表示されます。次のページからそこを起点に進めていきます。

{{% /notice %}}
