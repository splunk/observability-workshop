---
title: 1. Synthetics ダッシュボード
weight: 1
---

Splunk Observability Cloud のメインメニューから **Synthetics** をクリックします。**All** または **Browser tests** をクリックして、アクティブなテストの一覧を表示します。

RUM セクションでの調査中に、**Place Order** トランザクションに問題があることがわかりました。Synthetics テストからもこれを確認できるか見てみましょう。テストの4ページ目、つまり **Place Order** ステップの **First byte time** メトリクスを使用します。

{{% exercise title="テストのパフォーマンスを詳しく確認する" %}}

* **Search** ボックスに **[WORKSHOP NAME]** と入力し、ワークショップ用のテストを選択します（どれを選択するかはインストラクターが案内します）。
* **Performance KPIs** の下で、Time Picker を **Last 1 hour** に設定し、Enter を押します。
* **Location** をクリックし、ドロップダウンから **Page** を選択します。次のフィルターにテストに含まれるページが表示されます。
* **Duration** をクリックし、**Duration** の選択を解除して **First byte time** を選択します。
  ![Transaction Filter](../images/synthetics-transaction-filter.png)
* 凡例を確認し、**First byte time - Page 4** の色を確認します。
* **First byte time - Page 4** の最も高いデータポイントを選択します。この特定のテスト実行の **Run results** に移動します。
{{% /exercise %}}
