# サービスビューロー - ラボの概要

* 組織におけるObservability Cloudの利用状況を把握する
* Billing and Usage（課金と使用量）インターフェースを使って、使用量を追跡する
* チームを作成する
* チームへの通知ルールを管理する
* 使用量をコントロールする

---

## 1. エンゲージメントの理解

組織内のObservability Cloudのエンゲージメントを完全に理解するには、左上のハンバーガーをクリックして、**Organizations Settings → Organization Overview**　を選択すると、Observability Cloud の組織がどのように使用されているかを示す以下のダッシュボードが表示されます。

![Organization overview](/images/servicebureau/engagement.png)

左側のメニューには、メンバーのリストが表示され、右側には、ユーザー数、チーム数、チャート数、ダッシュボード数、ダッシュボードグループの作成数、様々な成長傾向を示すチャートが表示されます。

現在お使いのワークショップ組織では、ワークショップごとにデータが消去されるため、作業できるデータが少ないかもしれません。

このワークショップインスタンスの  Organization Overview にある様々なチャートをじっくりとご覧ください。

---

## 2. 使用状況と請求情報

契約に対する使用量を確認したい場合は、 **Organizations Settings → Billing and Usage** を選択します。

もしくは、左側のペインから **Billing and Usage** の項目を選択してもするのが早い方法です。

![Left pane](/images/servicebureau/billing-and-usage-menu.png)

この画面では、使用量を計算して取り込むため、読み込みに数秒かかることがあります。

---

## 3. 使用量の把握

下図のような画面が表示され、現在の使用量、平均使用量、およびホスト、コンテナ、カスタムメトリクス、高解像度メトリクスの各カテゴリごとの権利の概要が表示されます。

これらのカテゴリの詳細については、[Billing and Usage information](https://docs.splunk.com/Observability/admin/monitor-imm-billing-usage.html){: target=_blank} を参照してください。

![Billing and Usage](/images/servicebureau/usage-charts.png)

---

## 4. 使用状況を詳しく調べる

一番上のチャートには、カテゴリーごとの現在のサブスクリプションレベルが表示されます（下のスクリーンショットでは、上部の赤い矢印で表示されています）。

また、4つのカテゴリーの現在の使用状況も表示されます（チャート下部の赤い線で示されています）。

この例では、「ホスト」が25個、「コンテナ」が0個、「カスタムメトリクス」が100個、「高解像度メトリクス」が0個であることがわかります。

![Billing and Usage-top](/images/servicebureau/usage-detail.png)

下のグラフでは、現在の期間のカテゴリごとの使用量が表示されています（グラフの右上のドロップダウンボックスに表示されています）。

**Average Usage** と書かれた青い線は、Observability Cloudが現在の請求期間の平均使用量を計算するために使用するものを示しています。

![Billing and Usage-Bottom](/images/servicebureau/usage-trends.png)

!!! info

    スクリーンショットからわかるように、Observability Cloudはコスト計算にHigh Watermarkや95パーセンタイルを使用せず、実際の平均時間使用量を使用しています。これにより、超過料金のリスクなしに、パフォーマンステストやBlue/Greenスタイルのデプロイメントなどを行うことができます。

オプションを確認するには、左の **Usage Metric** ドロップダウンから異なるオプションを選択して表示するメトリックを変更するか、右のドロップダウンで **Billing Period** を変更します。

また、右側のドロップダウンで請求期間を変更することもできます。

最後に、右側のペインには、お客様のサブスクリプションに関する情報が表示されます。

![Billing and Usage-Pane](/images/servicebureau/subscription.png)
