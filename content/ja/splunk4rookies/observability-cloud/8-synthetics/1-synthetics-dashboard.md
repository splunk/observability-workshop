---
title: 1. Syntheticsダッシュボード
weight: 1
---

Splunk Observability Cloud のメインメニューから、**Synthetics**をクリックします。**All**または**Browser tests**をクリックして、アクティブなテストのリストを表示します。

RUM セクションでの調査中に、**Place order**トランザクションに問題があることがわかりました。Synthetics テストからもこれを確認できるか見てみましょう。テストの 4 ページ目の**First byte time**というメトリクスを使用します。これは**Place order**ステップです。

{{% notice title="演習" style="green" icon="running" %}}

- **Search**ボックスに **[ワークショップ名]** を入力し、あなたのワークショップのテストを選択します（インストラクターがどれを選択するか指示します）。
- **Performance KPIs**の下で、時間選択を**過去 1 時間**に設定して Enter キーを押します。
- **Location**をクリックし、ドロップダウンから**Page**を選択します。次のフィルターには、テストの一部であるページが表示されます。
- **Duration**をクリックし、**Duration**の選択を解除して**First byte time**を選択します。
  ![トランザクションフィルター](../images/synthetics-transaction-filter.png)
- 凡例を見て、**First byte time - Page 4**の色に注目してください。
- **First byte time - Page 4**の最も高いデータポイントを選択します。これで、この特定のテスト実行の**Run results**に移動します。
  {{% /notice %}}
