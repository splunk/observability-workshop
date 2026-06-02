---
title: 3. フィルタリングとグルーピング
weight: 3
---

Log Observer を開いて環境フィルターを設定すると、すべてのサービスのすべてのログが表示されます。これでは情報が多すぎます。絞り込んでいきましょう。

{{% notice title="演習" style="green" icon="running" %}}

**ステップ 1: Severity でグルーピングする**

* **Group By** ドロップダウンボックス **(1)** をクリックします。
* 検索を使って `severity` を見つけて選択します。
* {{% button style="blue" %}}Apply{{% /button %}} ボタンをクリックします。

タイムラインチャートの凡例に、ログレベルの分布 — **debug**、**info**、**warn**、**error** が表示されることを確認してください。

<!-- TODO screenshot: Timeline chart grouped by severity showing legend -->

**ステップ 2: エラーのみにフィルターする**

* タイムラインチャートの凡例で **error** **(2)** という文字をクリックします。
* **Add to filter** を選択します。
* ページ上部の {{% button style="blue" %}}Run Search{{% /button %}} をクリックします。

これで環境内の error レベルのログのみが表示されます。

<!-- TODO screenshot: Log Observer filtered to errors only -->

**ステップ 3: ノイズの多いサービスを特定する**

* 下のテーブルのログエントリーを確認します。`service.name` カラムをスキャンしてください。

{{< tabs >}}
{{% tab title="質問" %}}
**最も多くのエラーログを生成しているサービスはどれですか？**
{{% /tab %}}
{{% tab title="回答" %}}
<!-- TODO: Update with actual service name from OTel Demo v2.0.1 -->
エラーログのエントリーで最も頻繁に出現するサービス名を探します。それが主な容疑者です。
{{% /tab %}}
{{< /tabs >}}

**ステップ 4: サービスでフィルターする**

* ログエントリーの 1 つでサービス名をクリックします。
* **Add to filter** を選択します。
* {{% button style="blue" %}}Run Search{{% /button %}} をクリックします。

これで単一のサービスからのエラーログのみが表示されます。ノイズはなくなりました。

<!-- TODO screenshot: Log Observer filtered to errors from a single service -->

{{% /notice %}}

{{% notice title="Info" style="info" %}}
わずか 4 クリックで、すべてのサービスから何千行ものログが流れる状態から、単一の容疑者サービスのエラーに絞り込んだビューへと辿り着きました。これがクエリを書かずに高速にトリアージできる Log Observer のノーコードフィルタリングの威力です。
{{% /notice %}}
