---
title: 1. Synthetics Dashboard
weight: 1
---

{{% exercise title="失敗した Synthetics 実行を見つける" %}}

* Splunk Observability Cloud のメインメニューから、**Digital Experience → Synthetics tests** をクリックします。**All** または **Browser tests** をクリックして、アクティブなテストの一覧を表示します。

* RUM セクションでの調査で、**Place Order** トランザクションに問題があることがわかりました。Synthetics テストからも同じことが確認できるか見ていきましょう。

---

* **Search** ボックスに **[NAME OF WORKSHOP]** と入力して、このワークショップのテストを絞り込みます。
* テストを選択します。
* **Go to all run results** をクリックします。
* **All** を **Failure** **(1)** に変更します。

  ![Transaction Filter](../images/failed-run-results.png)

* 失敗した結果のいずれかをクリックします。

{{% /exercise %}}
