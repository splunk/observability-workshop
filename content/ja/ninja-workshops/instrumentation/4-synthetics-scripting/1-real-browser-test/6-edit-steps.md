---
title: 1.6 テストステップの編集
weight: 6
---

デフォルトでは、Chrome Recorder から出力されるステップは **"Go to URL"** や **"Click on `<button>`"** といった汎用的な名前になっています。テストを作成している間はそれでも構いませんが、ステップが失敗して同僚が午前3時にアラートを見つめているとき、**"Step 3 failed: Click on `<button>`"** では何の役にも立ちません。**"Step 3 failed: Add to Cart"** であれば、ユーザージャーニーのどこでリグレッションが発生したのかを正確に伝えられます。

ステップ名は以下の場所にも表示されます。

- Synthetic Monitoring の実行結果 UI（ステップごとのウォーターフォール、スクリーンショット）
- ディテクターのアラートメッセージや通知
- `synthetic.step` でフィルタリングする、リンクされた Observability Cloud のダッシュボード

読みやすい名前に変更するために、少しの時間を投資する価値があります。

ステップを編集するには、{{< button >}}+ Edit steps or synthetic transactions{{< /button >}} ボタンをクリックします。

![Edit steps](../../img/edit-steps.png)

4つのステップそれぞれに、意味のある名前を付けます。

- **Step 1** — **Go to URL** を **HomePage - Online Boutique** に置き換えます。
- **Step 2** — **Select Vintage Camera Lens** と入力します。
- **Step 3** — **Add to Cart** と入力します。
- **Step 4** — **Place Order** と入力します。

![Step names](../../img/step-names.png)

{{% notice title="ヒント — Synthetic Transactions" style="info" %}}
同じパネルから、複数のステップをまとめて **synthetic transaction**（ジャーニーの一部に名前を付け、単一のタイミングとして追跡したい部分集合。例えばカート、支払い、注文確認のステップをまとめた "Checkout" など）にグループ化できます。トランザクションは実行ウォーターフォールの独立した行として表示され、独立したメトリクスとしてチャートやアラートの対象にできます。ここでは作成しませんが、全体の実行時間とは独立して重要なサブフローを監視するための強力なパターンです。
{{% /notice %}}

{{% button style="blue" %}}< Return to test{{% /button %}} をクリックしてテスト設定ページに戻り、{{% button style="blue" %}}Save{{% /button %}} をクリックしてテストを保存します。

テストダッシュボードに戻ります。数分後、最初の結果が **Performance KPIs** の散布図に表示され始めます。

![Scatterplot](../../img/scatterplot.png)

## 散布図の読み方

散布図上の各ドットは1回のテスト実行を表します。

- **X 軸** は時間です。新しい実行ほど右側に表示されます。
- **Y 軸** は実行時間（秒）です。値が小さいほど高速です。
- **色** はロケーションを表します。このワークショップでは3系列（N. Virginia、London、Melbourne）が表示されます。

上部のコントロールでは、**time range**、**aggregation interval**（5分、1時間など）、**scale**（linear または logarithmic — 1つのロケーションが他より大幅に遅い場合は log が便利です）、**location filter**、プロットする **metric**（デフォルトは実行時間ですが、個別の web vital に切り替えることも可能）を変更できます。

時間経過に伴う2つのパターンに注目してください。実行時間における *step change*（サイトまたはその依存先で何かが変化した。通常はデプロイまたは CDN 設定の変更）と、ロケーション間の *spread* の拡大（リージョナルな問題。CDN エッジ、リージョナルな依存先、DNS の問題）です。

**おめでとうございます！** Splunk Synthetic Monitoring で Real Browser Test を作成できました。次は、1回の実行をクリックして、Synthetics がその実行についてキャプチャしたすべての情報を見ていきます。
