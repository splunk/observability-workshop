---
title: データの可視化
linkTitle: 7. Visualisation
weight: 7
---

## Splunk Observability Cloud

OpenTelemetry Collectorからメトリクスを Splunk Observability Cloudに送信する設定が完了したので、Splunk Observability Cloudでデータを確認しましょう。Splunk Observability Cloudへの招待を受け取っていない場合は、インストラクターがログイン資格情報を提供します。

その前に、インスタンスでストレステストを実行して、ダッシュボードを活性化させましょう。

``` bash
sudo apt install stress
while true; do stress -c 2 -t 40; stress -d 5 -t 40; stress -m 20 -t 40; done
```

Splunk Observability Cloudにログインしたら、左側のナビゲーションを使用してメインメニューから **Dashboards** に移動します。Teams ビューが表示されます。このビューの上部にある **All Dashboards** をクリックします。

![menu-dashboards](../images/menu-dashboards.png)

検索ボックスで **OTel Contrib** を検索します。

![search-dashboards](../images/search-dashboards.png)

{{% notice style="info" %}}
ダッシュボードが存在しない場合は、インストラクターがすぐに追加できます。Splunk主催のワークショップに参加していない場合は、インポートするDashboard Groupをこのページの下部で確認できます。
{{% /notice %}}

**OTel Contrib Dashboard** ダッシュボードをクリックして開き、次にダッシュボード上部の **Participant Name** ボックスをクリックして、`config.yaml` で `participant.name` に設定した名前をドロップダウンリストから選択するか、名前を入力して検索します。

![select-conf-attendee-name](../images/select-participant-name.png)

OpenTelemetry Collectorを設定したホストのホストメトリクスが表示されます。

![participant-dashboard](../images/participant-dashboard.png)

{{% resources sort="asc" style="info" title="Download Dashboard  Group JSON for importing" /%}}
