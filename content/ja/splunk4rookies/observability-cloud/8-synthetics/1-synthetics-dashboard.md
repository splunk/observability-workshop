---
title: 1. Synthetics ダッシュボード
weight: 1
---

Splunk Observability Cloud のメインメニューから、**Synthetics** をクリックします。**All** または **Browser tests** をクリックすると、有効なテストの一覧が表示されます。

RUM セクションでの調査中に、**Place Order** トランザクションに問題があることがわかりました。Synthetics テストからもこれを確認できるか見てみましょう。テストの 4 ページ目（**Place Order** ステップ）に対する **First byte time** メトリクスを使用します。

{{% exercise title="テストのパフォーマンスをドリルダウンする" %}}

* **Search** ボックスに **[WORKSHOP NAME]** と入力し、ワークショップ用のテストを選択します（どのテストを選択するかはインストラクターから案内があります）。
* **Performance KPIs** で Time Picker を **Last 1 hour** に設定し、Enter キーを押します。
* **Location** をクリックし、ドロップダウンから **Page** を選択します。次のフィルターには、テストに含まれるページが表示されます。
* **Duration** をクリックし、**Duration** の選択を解除して **First byte time** を選択します。
  ![Transaction Filter](../images/synthetics-transaction-filter.png)
* 凡例を確認し、**First byte time - Page 4** の色をメモします。
* **First byte time - Page 4** で最も高いデータポイントを選択します。これにより、この特定のテスト実行の **Run results** に移動します。
{{% /exercise %}}
