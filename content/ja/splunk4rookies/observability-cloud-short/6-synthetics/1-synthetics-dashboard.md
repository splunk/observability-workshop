---
title: 1. Synthetics ダッシュボード
weight: 1
---

{{% exercise title="失敗した Synthetics 実行を探す" %}}

* Splunk Observability Cloud のメインメニューから、**Digital Experience → Synthetics tests** をクリックします。**All** または **Browser tests** をクリックして、アクティブなテストの一覧を表示します。

* RUM セクションでの調査中に、**Place Order** トランザクションに問題があることを確認しました。これを Synthetics テストからも確認できるか見てみましょう。

---

* **Search** ボックスに **[NAME OF WORKSHOP]** を入力して、このワークショップ用のテストをフィルタリングします。
* テストを選択します。
* **Go to all run results** をクリックします。
* **All** を **Failure** **(1)** に変更します。

  ![Transaction Filter](../images/failed-run-results.png)

* 失敗した結果のいずれかをクリックします。

{{% /exercise %}}
