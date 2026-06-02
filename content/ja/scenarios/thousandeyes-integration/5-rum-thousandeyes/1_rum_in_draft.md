---
title: ThousandEyes and Splunk RUM
linkTitle: 5.1 RUM
weight: 1
time: 10 minutes
description: ThousandEyes のネットワークメトリクスを Splunk RUM と相関させ、エンドユーザー体験とネットワーク問題をまとめて調査できるようにします。
draft: true
---

このコンテンツはレビューが必要です。当面は削除します。

ThousandEyes を Splunk RUM と統合して、ネットワーク問題がエンドユーザーの問題と関連しているかどうかを把握しましょう。

## 要件

1. Splunk Observability Cloud と ThousandEyes の両方の管理者権限
1. Splunk RUM にデータを送信しているアプリケーションが少なくとも 1 つあること
1. Splunk RUM のアプリと **同じドメイン** で、ThousandEyes に以下のいずれかの種類のテストが少なくとも 1 つ実行されていること
    - [agent-to-server](https://docs.thousandeyes.com/product-documentation/tests/network-tests#agent-to-server-tests)
    - [HTTP server](https://docs.thousandeyes.com/product-documentation/tests/http-server-tests)
    - [page load](https://docs.thousandeyes.com/product-documentation/tests/web-layer-tests#page-load-test)
    - [transaction](https://docs.thousandeyes.com/product-documentation/tests/web-layer-tests#transaction-test)

## 統合手順

1. ThousandEyes で OAuth Bearer トークンを作成します
    - 右上のユーザー名を選択し、**Profile** を選択します。
    - User API Tokens の **OAuth Bearer Token** の横にある **Create** をクリックしてトークンを生成します。検証のためにメールで届くコードが必要です。
    - Observability Cloud のデータインテグレーションウィザードで使用するため、トークンをコピーまたは控えておきます。このトークンは再取得できません（再取得には失効と再作成が必要です）。
1. Splunk Observability Cloud で **Data Management > Available Integrations > ThousandEyes Network Insights** を開きます
    - **Ingest** トークンを選択します。
    - ThousandEyes で取得した OAuth Bearer トークンを入力します。
    - テストの一致状況を確認し、必要に応じて選択を変更し、データ取り込みの見積もりを確認してから `Done` を選択します。

## 統合の確認

ThousandEyes テストを実行している RUM アプリケーションに移動し、Map を表示します。
ThousandEyes テストも実行しているロケーションにマウスオーバーすると、ThousandEyes メトリクスのプレビューが表示されます:
![ThousandEyes のネットワーク遅延が表示された Splunk RUM の地図ビュー](../images/rum-thousandeyes-map-preview.png?width=45vw)

ThousandEyes でアクティブなアラートがある場合、RUM の該当ロケーションのバブルの上に ThousandEyes アイコンが表示されます:
![Splunk RUM の地図ビュー](../images/rum-thousandeyes-map.png?width=45vw)

該当のリージョンをクリックすると、RUM の他のメトリクスと並んでネットワークメトリクスが表示されます。`View ThousandEyes Tests` を開くと、ThousandEyes の該当テストに移動できます:
![RUM メトリクスと ThousandEyes メトリクスおよび Tests ダイアログが開いた状態](../images/rum-thousandeyes-tests-dialog.png?width=45vw)

## カスタムダッシュボードで RUM と ThousandEyes のメトリクスを表示する

これで Observability Cloud の他の KPI を、関連する ThousandEyes テストのシグナルと相関させることができます！

1. Dashboards に移動 > "RUM" を検索 > `RUM applications` グループにある既製の RUM ダッシュボードのいずれかをクリックします
1. 関心のある RUM KPI のチャートをコピーするか、右上のダッシュボードのアクションメニューを開いて `Save As` で自分のダッシュボードグループにコピーを作成します。
1. 新しいダッシュボードで、シグナル `network.latency` を使用した新しいチャートを作成します
    - 補間ポリシーを `Last value` に変更します
    - 単位を Time > `Millisecond` に変更します
    - Chart Options で `Show on-chart legend` を選択し、値に `thousandeyes.source.agent.name` を設定します。これにより、ThousandEyes のエージェントロケーションごとにチャートがセグメント化されます。
1. 新しいチャートに名前を付けて保存し、それをコピーして、コピーしたチャートのシグナルでメトリクスを変更し、必要に応じて単位や可視化オプションを調整することで、`network.jitter` と `network.loss` の同様のチャートを作成します。

カスタムダッシュボードとチャートの作成に関するより詳細なガイダンスについては、[Dashboard Workshop](/en/ninja-workshops/7-dashboards-detectors/) を参照してください。

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
ThousandEyes のテストメトリクスと並べて表示すると便利な、Observability Cloud の他のメトリクスについて検討してみましょう。

例えば、Synthetics で API テストを実行している場合は、ロケーション別の API テスト成功率のヒートマップを追加することを検討してください。

  {{% /notice %}}
