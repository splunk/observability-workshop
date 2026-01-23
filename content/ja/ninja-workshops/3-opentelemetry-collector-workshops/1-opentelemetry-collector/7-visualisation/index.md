---
title: データの可視化
linkTitle: 7. 可視化
weight: 7
---

## Splunk Observability Cloud

OpenTelemetry Collector からメトリクスを Splunk Observability Cloud に送信する設定が完了したので、Splunk Observability Cloud でデータを確認してみましょう。Splunk Observability Cloud への招待を受け取っていない場合は、インストラクターがログイン資格情報を提供します。

その前に、少し面白くするためにインスタンスでストレステストを実行してみましょう。これによりダッシュボードが活性化されます。

``` bash
sudo apt install stress
while true; do stress -c 2 -t 40; stress -d 5 -t 40; stress -m 20 -t 40; done
```

Splunk Observability Cloud にログインしたら、左側のナビゲーションを使用してメインメニューから **Dashboards** に移動します。これによりチームビューが表示されます。このビューの上部にある **All Dashboards** をクリックします

![menu-dashboards](../images/menu-dashboards.png)

検索ボックスで **OTel Contrib** を検索します

![search-dashboards](../images/search-dashboards.png)

{{% notice style="info" %}}
ダッシュボードが存在しない場合は、インストラクターがすぐに追加できます。Splunk 主催のワークショップに参加していない場合は、インポートするダッシュボードグループをこのページの下部で見つけることができます。
{{% /notice %}}

**OTel Contrib Dashboard** ダッシュボードをクリックして開き、次にダッシュボード上部の **Participant Name** ボックスをクリックして、`config.yaml` で `participant.name` に設定した名前をドロップダウンリストから選択するか、名前を入力して検索します

![select-conf-attendee-name](../images/select-participant-name.png)

これで、OpenTelemetry Collector を設定したホストのホストメトリクスを確認できます。

![participant-dashboard](../images/participant-dashboard.png)

{{% resources sort="asc" style="info" title="Download Dashboard  Group JSON for importing" /%}}
