---
title: 1. Overview ページ
weight: 1
---

Database Monitoring の **Overview** ページは、すべての調査の出発点です。このページには2つの情報が同時に表示されます。

- 選択したメトリクスでランク付けされた、上位5インスタンスの**時系列チャート**
- チャートの下に表示される、すべての監視対象インスタンスの**リスト**（合計クエリ実行時間順にソート）

リスト内の主要な列は **Total duration** と **Total CPU time** です。この2つの差は重要な意味を持ちます。インスタンスの Total duration が高いにもかかわらず CPU time が比較的低い場合、クエリは有用な処理ではなく、ロック、I/O、ネットワークなどの*待機*に時間を費やしていることを意味します。

{{% notice title="演習" style="green" icon="running" %}}

- **Database Monitoring Overview** ページの上部にある時系列チャートを確認します **(1)**。
- チャートの下にあるインスタンスリストを確認します **(2)**。
- 右上のタイムピッカーが適切な時間枠に設定されていることを確認します — **Last 1 hour** がデフォルトとして適切です。

<!-- TODO screenshot: Database Monitoring overview page with the top-5 trend chart (1) and the instance list (2) annotated -->
![Database Monitoring Overview](../images/overview-page.png)

{{< tabs >}}
{{% tab title="質問" %}}
**インスタンスリストの中で、Total duration が最も高いインスタンスはどれですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**リストの最上位の行です** — テーブルはデフォルトで Total duration の降順でソートされるため、最も問題のあるインスタンスは常に最上位に表示されます。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
