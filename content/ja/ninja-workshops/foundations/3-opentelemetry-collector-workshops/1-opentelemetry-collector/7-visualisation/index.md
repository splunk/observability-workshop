---
title: Data Visualisations
linkTitle: 7. Visualisation
weight: 7
---

## Splunk Observability Cloud

OpenTelemetry Collector が Splunk Observability Cloud にメトリクスを送信するように設定できたので、Splunk Observability Cloud でデータを確認してみましょう。Splunk Observability Cloud への招待を受け取っていない場合は、講師がログイン認証情報を提供します。

その前に、もう少し面白くするために、インスタンスに対してストレステストを実行します。これによりダッシュボードが活性化されます。

``` bash
sudo apt install stress
while true; do stress -c 2 -t 40; stress -d 5 -t 40; stress -m 20 -t 40; done
```

Splunk Observability Cloud にログインしたら、左側のナビゲーションを使用して、メインメニューから **Dashboards** に移動します。これにより Teams ビューが表示されます。このビューの上部で **All Dashboards** をクリックします。

![menu-dashboards](../images/menu-dashboards.png)

検索ボックスで **OTel Contrib** を検索します。

![search-dashboards](../images/search-dashboards.png)

{{% notice style="info" %}}
ダッシュボードが存在しない場合、講師が素早く追加できます。Splunk がホストするバージョンのワークショップに参加していない場合、インポートする Dashboard Group はこのページの下部にあります。
{{% /notice %}}

**OTel Contrib Dashboard** ダッシュボードをクリックして開き、次にダッシュボード上部の **Participant Name** ボックスをクリックし、`config.yaml` で `participant.name` に設定した名前をドロップダウンリストから選択するか、検索のために名前を入力し始めます。

![select-conf-attendee-name](../images/select-participant-name.png)

これで、OpenTelemetry Collector を設定したホストのホストメトリクスを確認できるようになります。

![participant-dashboard](../images/participant-dashboard.png)

{{% resources sort="asc" style="info" title="Download Dashboard  Group JSON for importing" /%}}
