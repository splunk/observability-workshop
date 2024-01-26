---
title: 1. Synthetics Dashboard
weight: 1
---

Splunk Observability Cloudのメインメニューから **Synthetics** をクリックします。**All** または **Browser tests** をクリックして、アクティブなテストの一覧を表示します。

RUMセクションでの調査中、**Place Order** トランザクションに問題があることが判明しました。Synthetics テストでもこれを確認できるかどうか見てみましょう。テストの4番目のページ、つまり **Place Order** ステップのメトリック **First byte time** を使用します。

{{% notice title="実習" style="green" icon="running" %}}

* **Search** ボックスに **[WORKSHOP NAME]** と入力し、ワークショップに対応するテストを選択します（インストラクターからの指示があります）。
* **Performance KPIs** でタイムピッカーを **-30m** に設定し、Enter キーを押します。
* **Location** をクリックし、ドロップダウンから **Page** を選択します。次のフィルタにはテストの一部であるページが表示されます。
* **Duration** をクリックして **Duration** の選択を解除し、**First byte time** を選択します。
  ![Transaction Filter](../images/synthetics-transaction-filter.png)
* 凡例を確認し、**First byte time - Page 4** の色をメモします。
* **First byte time - Page 4** の最高のデータポイントを選択します。
* 右から新しいペインが表示されます。ペインの上部にある時間をメモします。リスト内でこの時間を見つけ、クリックします。これは最も遅いテスト結果です。
  ![Multiple Runs](../images/synthetics-multiple-runs.png)
{{% /notice %}}

これで、この特定のテストランの **Run results** に移動します。
