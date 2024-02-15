---
title: 1. Synthetics Dashboard
weight: 1
---

Splunk Observability Cloud のメインメニューから **Synthetics** をクリックします。**All** または **Browser tests** をクリックして、アクティブなテストの一覧を表示します。

RUM セクションでの調査中、**Place Order** トランザクションに問題があることを見つけました。Synthetics テストでもこれを確認できるかどうか見てみましょう。テストの4番目のページ、つまり **Place Order** ステップのメトリック **First byte time** を使用します。

{{% notice title="Exercise" style="green" icon="running" %}}

* **Search** ボックスに **[WORKSHOP NAME]** を入力し、ワークショップに対応するテストを選択します（インストラクターから指示します）。
* **Performance KPIs** の下部にある時間枠を **-30m** に設定し、Enter キーを押します。
* **Location** と表示されている箇所をクリックし、ドロップダウンから **Page** を選択します。隣の Filter 欄にはテストに含まれるページが表示されます。
* **Duration** と表示されている箇所をクリックして **Duration** の選択を解除し、**First byte time** を選択します。
  ![Transaction Filter](../images/synthetics-transaction-filter.png)
* 凡例を確認し、**First byte time - Page 4** の色に着目しましょう。
* **First byte time - Page 4** の値が最も大きくなるデータポイントを選択します。
* 右から新しいペインが表示されます。ペインの上部にある所要時間を確認してください。リスト内でこの所要時間が表示されている行を見つけ、クリックします。最も時間がかかったテスト結果を見つけられました。
  ![Multiple Runs](../images/synthetics-multiple-runs.png)
{{% /notice %}}

この特定のテスト実行に関して、**Run results** に移動して見てみましょう。
