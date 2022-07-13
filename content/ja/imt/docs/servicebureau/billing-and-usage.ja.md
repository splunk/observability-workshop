---
title: サブスクリプション使用量
linkTitle: サブスクリプション使用量
weight: 50
isCJKLanguage: true
---

* 組織におけるObservability Cloudの利用状況を把握する
* Subscription Usage（サブスクリプション使用量）インターフェースを使って、使用量を追跡する
* チームを作成する
* チームへの通知ルールを管理する
* 使用量をコントロールする

---

## 1. 利用状況を把握する

組織内のObservability Cloudのエンゲージメントを完全に把握するには、左下 **>>** を開き、**Settings → Organization Overview** を選択すると、Observability Cloud の組織がどのように使用されているかを示す以下のダッシュボードが表示されます。

![Organization overview](../../../images/engagement.png)

左側のメニューには、メンバーのリストが表示され、右側には、ユーザー数、チーム数、チャート数、ダッシュボード数、ダッシュボードグループの作成数、様々な成長傾向を示すチャートが表示されます。

現在お使いのワークショップ組織では、ワークショップごとにデータが消去されるため、作業できるデータが少ないかもしれません。

このワークショップインスタンスの  Organization Overview にある様々なチャートをじっくりとご覧ください。

## 2. Subscription Usage

契約に対する使用量を確認したい場合は、 **Subscription Usage** を選択します。

![Left pane](../../../images/billing-and-usage-menu.png)

この画面では、使用量を計算して取り込むため、読み込みに数秒かかることがあります。

## 3. 使用量を理解する

下図のような画面が表示され、現在の使用量、平均使用量、およびホスト、コンテナ、カスタムメトリクス、高解像度メトリクスの各カテゴリごとの権利の概要が表示されます。

これらのカテゴリの詳細については、[Monitor Splunk Infrastructure Monitoring subscription usage](https://docs.splunk.com/Observability/admin/imm-billing-usage/monitor-imm-billing-usage.html) を参照してください。

![Billing and Usage](../../../images/usage-charts.png)

---

## 4. 使用状況を詳しく調べる

一番上のチャートには、カテゴリーごとの現在のサブスクリプションレベルが表示されます（下のスクリーンショットでは、上部の赤い矢印で表示されています）。

また、4つのカテゴリーの現在の使用状況も表示されます（チャート下部の赤い線で示されています）。

この例では、「ホスト」が25個、「コンテナ」が0個、「カスタムメトリクス」が100個、「高解像度メトリクス」が0個であることがわかります。

![Billing and Usage-top](../../../images/usage-detail.png)

下のグラフでは、現在の期間のカテゴリごとの使用量が表示されています（グラフの右上のドロップダウンボックスに表示されています）。

**Average Usage** と書かれた青い線は、Observability Cloudが現在のサブスクリプション期間の平均使用量を計算するために使用するものを示しています。

![Billing and Usage-Bottom](../../../images/usage-trends.png)

{{% alert title="Info" color="primary" %}}
スクリーンショットからわかるように、Observability Cloudはコスト計算には最大値や95パーセンタイル値ではなく、実際の平均時間使用量を使用しています。これにより、超過料金のリスクなしに、パフォーマンステストやBlue/Greenスタイルのデプロイメントなどを行うことができます。
{{% /alert %}}

オプションを確認するには、左の **Usage Metric** ドロップダウンから異なるオプションを選択して表示するメトリックを変更するか、右のドロップダウンで **Billing Period** を変更します。

また、右側のドロップダウンでサブスクリプション期間を変更することもできます。

最後に、右側のペインには、お客様のサブスクリプションに関する情報が表示されます。

![Billing and Usage-Pane](../../../images/subscription.png)
