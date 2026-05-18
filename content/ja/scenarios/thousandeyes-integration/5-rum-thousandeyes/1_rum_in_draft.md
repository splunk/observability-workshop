---
title: ThousandEyes と Splunk RUM
linkTitle: 5.1 RUM
weight: 1
time: 10 minutes
description: ThousandEyes のネットワークメトリクスと Splunk RUM を相関させ、エンドユーザー体験とネットワークの問題を一緒に調査できるようにします。
draft: true
---

このコンテンツはレビューが必要です。現時点では削除しています。

ThousandEyes と Splunk RUM を統合して、ネットワークの問題がエンドユーザーの問題と相関しているかどうかを把握します。

## 要件

1. Splunk Observability Cloud と ThousandEyes の両方に対する管理者権限
1. Splunk RUM にデータを送信しているアプリケーションが少なくとも1つあること
1. Splunk RUM のアプリと**同じドメイン**で、ThousandEyes で以下のタイプのテストが少なくとも1つ実行されていること
    - [agent-to-server](https://docs.thousandeyes.com/product-documentation/tests/network-tests#agent-to-server-tests)
    - [HTTP server](https://docs.thousandeyes.com/product-documentation/tests/http-server-tests)
    - [page load](https://docs.thousandeyes.com/product-documentation/tests/web-layer-tests#page-load-test)
    - [transaction](https://docs.thousandeyes.com/product-documentation/tests/web-layer-tests#transaction-test)

## 統合手順

1. ThousandEyes で OAuth Bearer トークンを作成します
    - 右上隅のユーザー名を選択し、**Profile** を選択します。
    - User API Tokens の下にある **OAuth Bearer Token** の横の **Create** をクリックしてトークンを生成します。確認のためにメールからコードが必要になります。
    - Observability Cloud のデータ統合ウィザードで使用するトークンをコピーまたはメモしてください。このトークンは再度取得できません（取り消して再作成する必要があります）。
1. Splunk Observability Cloud で、**Data Management > Available Integrations > ThousandEyes Network Insights** を開きます
    - **Ingest** トークンを選択します。
    - ThousandEyes からの OAuth Bearer トークンを入力します。
    - テストの一致を確認し、必要に応じて選択を変更し、推定データ取り込み量を確認してから `Done` を選択します。

## 統合の確認

ThousandEyes テストが実行されている RUM アプリケーションに移動し、Map を表示します。
ThousandEyes テストも実行されているロケーションにカーソルを合わせると、ThousandEyes メトリクスのプレビューが表示されます
![Splunk RUM の Geo マップビュー、ThousandEyes からの Network Latency が表示されている](../images/rum-thousandeyes-map-preview.png?width=45vw)

ThousandEyes でアクティブなアラートがある場合、RUM の該当するロケーションバブルの上に ThousandEyes アイコンが表示されます
![Splunk RUM の Geo マップビュー](../images/rum-thousandeyes-map.png?width=45vw)

該当するリージョンをクリックすると、RUM の他のメトリクスと一緒にネットワークメトリクスが表示されます。`View ThousandEyes Tests` を開くと、ThousandEyes の関連テストに移動できます
![RUM メトリクスと ThousandEyes メトリクス、テストダイアログが開いている状態](../images/rum-thousandeyes-tests-dialog.png?width=45vw)

## カスタムダッシュボードで RUM と ThousandEyes のメトリクスを表示する

これで、Observability Cloud の他の KPI と関連する ThousandEyes テストからのシグナルを相関させることができます！

1. Dashboards に移動 > "RUM" を検索 > `RUM applications` グループ内のすぐに使える RUM ダッシュボードの1つをクリックします
1. 関心のある RUM KPI のチャートをコピーするか、右上のダッシュボードのアクションメニューを開いて `Save As` を選択し、自分のダッシュボードグループにコピーを作成します。
1. 新しいダッシュボードで、シグナル `network.latency` を使用して新しいチャートを作成します
    - 外挿ポリシーを `Last value` に変更します
    - 測定単位を Time > `Millisecond` に変更します
    - Chart Options で、値 `thousandeyes.source.agent.name` を使用して `Show on-chart legend` を選択します。これにより、ThousandEyes のエージェントロケーションごとにチャートがセグメント化されます。
1. 新しいチャートに名前を付けて保存し、コピーして `network.jitter` と `network.loss` の類似チャートを作成します。コピーしたチャートのシグナルでメトリクスを変更し、必要に応じて測定単位と可視化オプションを調整します。

カスタムダッシュボードとチャートの作成に関する詳細なガイダンスについては、[Dashboard Workshop](/ja/ninja-workshops/7-dashboards-detectors/) を参照してください。

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
Observability Cloud の他のメトリクスで、ThousandEyes テストメトリクスと並べて表示すると便利なものを考えてみてください。

例えば、Synthetics で API テストを実行している場合は、ロケーション別の API テスト成功率のヒートマップを追加することを検討してください。

  {{% /notice %}}
