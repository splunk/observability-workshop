---
title: 1.6 テストステップの編集
weight: 6
---

デフォルトでは、Chrome Recorderから出力されるステップには **"Go to URL"** や **"Click on `<button>`"** のような汎用的な名前が付いています。テストを作成している間はそれで問題ありませんが、ステップが失敗して同僚が午前3時にアラートを見ているとき、 **"Step 3 failed: Click on `<button>`"** では何の役にも立ちません。 **"Step 3 failed: Add to Cart"** であれば、ユーザージャーニーのどこでリグレッションが発生したかが正確にわかります。

ステップ名は以下の場所にも表示されます。

- Synthetic Monitoringの実行結果UI（ステップごとのウォーターフォール、スクリーンショット）
- Detectorのアラートメッセージと通知
- `synthetic.step` でフィルタリングするリンクされたObservability Cloudダッシュボード

少し時間をかけて読みやすい名前にする価値があります。

ステップを編集するには、 {{< button >}}+ Edit steps or synthetic transactions{{< /button >}} ボタンをクリックします。

![Edit steps](../../img/edit-steps.png)

4つのステップそれぞれに、意味のある名前を付けます。

- **Step 1** — **Go to URL** を **HomePage - Online Boutique** に変更します。
- **Step 2** — **Select Vintage Camera Lens** と入力します。
- **Step 3** — **Add to Cart** と入力します。
- **Step 4** — **Place Order** と入力します。

![Step names](../../img/step-names.png)

{{% notice title="ヒント — Synthetic Transactions" style="info" %}}
同じパネルで、複数のステップを **synthetic transaction** にグループ化できます。これは、単一のタイミングとして追跡したいジャーニーの名前付きサブセットです（例: カート、支払い、注文確認のステップをまとめた「Checkout」）。Transactionは実行ウォーターフォールで独自の行として表示され、チャートやアラートに使用できる独自のメトリクスとしても表示されます。ここでは作成しませんが、合計実行時間とは独立して重要なサブフローをモニタリングするための強力なパターンです。
{{% /notice %}}

{{% button style="blue" %}}< Return to test{{% /button %}} をクリックしてテスト設定ページに戻り、 {{% button style="blue" %}}Save{{% /button %}} をクリックしてテストを保存します。

テストダッシュボードに戻ります。数分後、最初の結果が **Performance KPIs** の散布図に表示され始めます。

![Scatterplot](../../img/scatterplot.png)

## 散布図の読み方

散布図の各ドットは1回のテスト実行を表します。

- **X軸** は時間で、最新の実行が右側に表示されます。
- **Y軸** は実行時間（秒）で、低いほど高速です。
- **色** はロケーションで、このワークショップでは3つのシリーズ（N. Virginia、London、Melbourne）が表示されます。

上部のコントロールで、 **時間範囲** 、 **集約間隔** （5m、1hなど）、 **スケール** （線形または対数 — 対数は1つのロケーションが他よりもはるかに遅い場合に便利です）、 **ロケーションフィルター** 、およびプロットする **メトリクス** （デフォルトは実行時間ですが、個別のWeb Vitalに切り替えることもできます）を変更できます。

時間の経過とともに2つのパターンに注目してください。1つは実行時間の *ステップ変化* （サイトまたはその依存関係に何かが変わった — 通常はデプロイまたはCDN設定）、もう1つはロケーション間の *ばらつき* が広がること（リージョンの問題 — CDNエッジ、リージョンの依存関係、DNS問題）です。

**おめでとうございます！** Splunk Synthetic MonitoringでReal Browser Testを正常に作成できました。次に、単一の実行をクリックして、Syntheticsがキャプチャしたすべての情報を確認します。
