---
title: 3. フィルタリングとグループ化
weight: 3
---

Log Observer を開き、環境フィルターを設定した状態では、すべてのサービスからのすべてのログが表示されています。これでは情報が多すぎます。絞り込んでいきましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

**ステップ 1: 重大度でグループ化する**

* **Group By** ドロップダウンボックス **(1)** をクリックします。
* 検索を使用して `severity` を見つけて選択します。
* {{% button style="blue" %}}Apply{{% /button %}} ボタンをクリックします。

タイムラインチャートの凡例に、ログレベルの分布（**debug**、**info**、**warn**、**error**）が表示されるようになります。

<!-- TODO screenshot: Timeline chart grouped by severity showing legend -->

**ステップ 2: エラーのみにフィルタリングする**

* タイムラインチャートの凡例で、**error** **(2)** という文字をクリックします。
* **Add to filter** を選択します。
* ページ上部の {{% button style="blue" %}}Run Search{{% /button %}} をクリックします。

これで、お使いの環境からのエラーレベルのログのみが表示されています。

<!-- TODO screenshot: Log Observer filtered to errors only -->

**ステップ 3: ノイズの多いサービスを特定する**

* 下のテーブルにあるログエントリを確認します。`service.name` カラムをスキャンしてください。

{{< tabs >}}
{{% tab title="Question" %}}
**最も多くのエラーログを生成しているサービスはどれですか？**
{{% /tab %}}
{{% tab title="Answer" %}}
<!-- TODO: Update with actual service name from OTel Demo v2.0.1 -->
エラーログエントリに最も頻繁に表示されるサービス名を探してください。それが主要な疑わしいサービスです。
{{% /tab %}}
{{< /tabs >}}

**ステップ 4: サービスでフィルタリングする**

* ログエントリの中にあるサービス名をクリックします。
* **Add to filter** を選択します。
* {{% button style="blue" %}}Run Search{{% /button %}} をクリックします。

これで、単一のサービスからのエラーログのみが表示されています。ノイズがなくなりました。

<!-- TODO screenshot: Log Observer filtered to errors from a single service -->

{{% /notice %}}

{{% notice title="Info" style="info" %}}
わずか4回のクリックで、すべてのサービスにわたる数千行のログから、単一の疑わしいサービスのエラーに焦点を絞ったビューに到達しました。これが Log Observer のノーコードフィルタリングの力です — クエリを書かずに素早くトリアージできます。
{{% /notice %}}
