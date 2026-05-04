---
title: Queries と Query Samples
linkTitle: 4. Queries と Query Samples
weight: 4
archetype: chapter
time: 15 minutes
description: インスタンス上で最も遅いクエリを特定し、個々のクエリサンプルと実行プランを調査します。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは **DBA** で、最もデータベース時間を消費しているインスタンスを特定しました。次に、*どのクエリ*が原因なのかを把握する必要があります。さらに、最も問題のあるクエリについては、*個々の実行が実際にどのように行われたか*を確認する必要があります。

> [!splunk] **Queries** タブには、待機時間、CPU 時間、または読み取り行数の順に並んだ上位の SQL ステートメントが表示されます。**Query samples** タブには、パラメータ、実行時間、データベースオプティマイザが選択した**実行プラン**を含む、それらのクエリの実際にキャプチャされた実行が表示されます。これらを組み合わせることで、「データベースが遅い」という状態から「このクエリが、これらのパラメータで、フルテーブルスキャンを実行している」という具体的な原因特定に至ることができます。

{{% /notice %}}

<!-- TODO screenshot: Queries tab with a list of top SQL statements ranked by duration -->
![上位クエリ](images/queries-tab.png?width=750px)
