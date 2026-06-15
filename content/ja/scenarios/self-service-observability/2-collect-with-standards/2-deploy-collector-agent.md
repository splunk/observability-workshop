---
title: Deploy Collector (Agent)
linkTitle: 2.2 Deploy Collector (Agent)
weight: 2
time: 10 minutes
---

## Collector (Agent)

ここではコレクターをデプロイします。最初はバックエンドに直接送信する設定にしますが、後で設定を変更してゲートウェイを使用するようにコレクターを再起動します。

手順:

* ツールバーの **Data Management** アイコンをクリックします
* **+ Add integration** ボタンをクリックします
* **Deploy the Splunk OpenTelemetry Collector** ボタンをクリックします
* **Next** をクリックします
* **Linux** を選択します
* モードは **Host monitoring (agent)** のままにします
* 環境を **prod** に設定します
* 残りはデフォルトのままにします
* このワークショップ用のアクセストークンを選択します
* **Next** をクリックします
* インストーラースクリプトをコピーし、提供された Linux 環境で実行します

このコレクターはホストメトリクスを送信しているため、一般的なナビゲーターで確認できます:

* ツールバーの **Infrastructure** アイコンをクリックします
* **Amazon Web Services** の下にある **EC2** パネルをクリックします
* `AWSUniqueId` が最も見つけやすい項目です。フィルターを追加し、ワイルドカードを使って検索します（例: `i-0ba6575181cb05226*`）

![Chart of agent](../images/collector_agent_chart.png)

`cpu.utilization` メトリクスを直接確認することもできます。AWSUniqueId でフィルタリングした新しいチャートを作成して表示します:

![Chart 2 of agent](../images/collector_agent_chart_2.png)

この作業を行った理由は、コレクターをゲートウェイ経由で送信した際に追加される新しいディメンションを簡単に確認できるようにするためです。**Data table** をクリックすると、現在送信されているディメンションを確認できます:

![Data Table](../images/collector_agent_data_table.png)

## 次のステップ

次に、コレクターをゲートウェイに送信するように再設定します。
