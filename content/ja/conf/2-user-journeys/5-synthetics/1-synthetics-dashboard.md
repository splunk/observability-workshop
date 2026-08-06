---
title: 1. Synthetics Dashboard
weight: 1
---

{{% exercise title="失敗したSyntheticsの実行を見つける" %}}

* Splunk Observability Cloudのメインメニューから、**Digital Experience → Synthetics tests** をクリックします。**All** または **Browser tests** をクリックして、アクティブなテストの一覧を表示します。

* RUMセクションでの調査で、**Place Order** トランザクションに問題があることがわかりました。Syntheticsテストからもこれを確認できるか見てみましょう。

---

* **Search** ボックスに **[NAME OF WORKSHOP]** と入力して、このワークショップのテストをフィルタリングします。
* テストを選択します。
* **Go to all run results** をクリックします。
* **All** を **Failure** **(1)** に変更します。

  ![Transaction Filter](../images/failed-run-results.png)

* 失敗した結果のいずれかをクリックします。

{{% /exercise %}}
